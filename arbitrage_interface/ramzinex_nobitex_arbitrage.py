import asyncio
import time
from termcolor import colored
from data_storage.logs_interface import save_errors_to_log_file
from data_storage.models import OrderBook
from exhchanges.nobitex_api import NobitexApi
from exhchanges.ramizenx_api import RamzinexApi
from .base_arbitrage import Arbitrage
from data_storage.csv_interface import save_ramzinex_nobitex_arbitrage_to_csv, \
    get_symbol_pair_id_in_nobitex_and_ramzinex


class RamzinexNobitexArbitrage(Arbitrage):

    def __init__(self, ramzinex_api: RamzinexApi, nobitex_api: NobitexApi):
        self.ramzinex_api = ramzinex_api
        self.nobitex_api = nobitex_api
        self.ramzinex_nobitex_symbol_id_equivalent_pair = get_symbol_pair_id_in_nobitex_and_ramzinex(
            "symbol_pair_id_mapping2.csv")  # todo : getting this from csv config file
        self.last_opportunity = {item[0]: (0, 0) for item in self.ramzinex_nobitex_symbol_id_equivalent_pair}

    async def find_arbitrage_opportunity(self):
        """this method find all opportunity for getting arbitrage from ramzinex and nobitex"""
        while True:
            # Run both functions asynchronously
            task1 = asyncio.create_task(self.ramzinex_api.update_all_order_book())
            task2 = asyncio.create_task(self.nobitex_api.update_all_order_book())

            # Wait for both tasks to complete
            results = await asyncio.gather(task1, task2)

            if results[0] is None or results[1] is None:
                print(colored("Error in update order book ", "red"))
                time.sleep(1)
                continue

            ramzinex_all_order_book = self.ramzinex_api.all_order_book
            nobitex_all_order_book = self.nobitex_api.all_order_book

            for symbol_id_equivalent in self.ramzinex_nobitex_symbol_id_equivalent_pair:
                nobitex_symbol, ramzinex_pair_id, nobitex_to_ramzinex_unit_ratio = symbol_id_equivalent
                try:
                    nobitex_symbol_order_book = nobitex_all_order_book[nobitex_symbol]
                    ramzinex_pair_id_order_book = ramzinex_all_order_book[ramzinex_pair_id]

                    self.check_latest_orders(nobitex_symbol_order_book, ramzinex_pair_id_order_book,
                                             nobitex_to_ramzinex_unit_ratio)

                except Exception as e:
                    print("error in getting and process " + str(nobitex_symbol) + " orderbooks : " + str(e))

            time.sleep(1)

    def check_latest_orders(self, nobitex_order_book: OrderBook, ramzinex_order_book: OrderBook,
                            nobitex_to_ramzinex_unit_ratio: int, exchanges="ramzinex-nobitex"):
        """this method getting latest orders in order book and checking them for finding arbitrage opportunity"""
        nobitex_highest_bid = nobitex_order_book.get_highest_bid_order()
        nobitex_lowest_ask = nobitex_order_book.get_lowest_ask_order()

        nobitex_lowest_ask_price, nobitex_highest_bid_price = nobitex_lowest_ask.price, nobitex_highest_bid.price
        nobitex_lowest_ask_volume, nobitex_highest_bid_volume = nobitex_lowest_ask.volume, nobitex_highest_bid.volume

        ramzinex_highest_bid = ramzinex_order_book.get_highest_bid_order()
        ramzinex_lowest_ask = ramzinex_order_book.get_lowest_ask_order()

        ramzinex_lowest_ask_price, ramzinex_highest_bid_price = ramzinex_lowest_ask.price, ramzinex_highest_bid.price
        ramzinex_lowest_ask_volume, ramzinex_highest_bid_volume = ramzinex_lowest_ask.volume, ramzinex_highest_bid.volume

        if nobitex_highest_bid_price > nobitex_lowest_ask_price:
            error_message = "ERROR IN NOBITEX ORDER BOOK :" + nobitex_order_book.symbol
            save_errors_to_log_file(str(error_message))
            return
        if ramzinex_highest_bid_price > ramzinex_lowest_ask_price:
            error_message = "ERROR IN RAMZINEX ORDER BOOK :" + ramzinex_order_book.pair_id
            print(error_message)
            save_errors_to_log_file(str(error_message))
            return

        # apply The ratio of Nobitex unit to Ramzinex
        ramzinex_highest_bid_price *= nobitex_to_ramzinex_unit_ratio
        ramzinex_lowest_ask_price *= nobitex_to_ramzinex_unit_ratio
        ramzinex_highest_bid_volume /= nobitex_to_ramzinex_unit_ratio
        ramzinex_lowest_ask_volume /= nobitex_to_ramzinex_unit_ratio

        print("Exchange      Lowest Ask     Highest Bid")
        print(f"NOBITEX       {nobitex_lowest_ask.price:<14} {nobitex_highest_bid.price}")
        print(f"RAMZINEX      {ramzinex_lowest_ask.price:<14} {ramzinex_highest_bid.price}")

        action = 0
        benefit = 0
        percent = 0
        if nobitex_lowest_ask_price < ramzinex_highest_bid_price:
            volume = min(nobitex_lowest_ask_volume, ramzinex_highest_bid_volume)
            benefit = volume * (ramzinex_highest_bid_price - nobitex_lowest_ask_price)
            percent = ramzinex_highest_bid_price / nobitex_lowest_ask_price
            opportunity = (ramzinex_highest_bid_price, nobitex_lowest_ask_price)
            buy_price = nobitex_lowest_ask_price
            sell_price = ramzinex_highest_bid_price
            buy_side = "nobitex"
            sell_side = "ramzinex"
            print("percent=", percent, " ramzinex_highest_bid=",
                  ramzinex_highest_bid_price, "nobitex_lowest_ask=", nobitex_lowest_ask_price, "volume=", volume,
                  end=" ")

        if ramzinex_lowest_ask_price < nobitex_highest_bid_price:
            volume = min(nobitex_highest_bid_volume, ramzinex_lowest_ask_volume)
            benefit = volume * (nobitex_highest_bid_price - ramzinex_lowest_ask_price)
            percent = nobitex_highest_bid_price / ramzinex_lowest_ask_price
            opportunity = (nobitex_highest_bid_price, ramzinex_lowest_ask_price)
            buy_price = ramzinex_lowest_ask_price
            sell_price = nobitex_highest_bid_price
            buy_side = "ramzinex"
            sell_side = "nobitex"
            print("percent=", percent, " nobitex_highest_bid=",
                  nobitex_highest_bid_price, " ramzinex_lowest_ask=", ramzinex_lowest_ask_price, " volume=", volume,
                  end=" ")

        if benefit > 0:
            print(exchanges, " symbol in nobitex=", nobitex_order_book.symbol, " pair_id in ramzinex=",
                  ramzinex_order_book.pair_id, " benefit = ", benefit, "\n")
            if self.last_opportunity[nobitex_order_book.symbol][0] != opportunity[0] and \
                    self.last_opportunity[nobitex_order_book.symbol][1] != opportunity[1]:
                action = 1
                self.last_opportunity[nobitex_order_book.symbol] = opportunity
            save_ramzinex_nobitex_arbitrage_to_csv(nobitex_order_book, ramzinex_order_book, nobitex_lowest_ask,
                                                   nobitex_highest_bid,
                                                   ramzinex_lowest_ask, ramzinex_highest_bid, benefit, percent, action,
                                                   nobitex_to_ramzinex_unit_ratio, buy_price, sell_price, buy_side,
                                                   sell_side, volume)
        else:
            print("no opportunity :(")
