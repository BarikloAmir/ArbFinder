import asyncio
import time
from termcolor import colored
from data_storage.logs_interface import save_errors_to_log_file
from data_storage.models import OrderBook
from exhchanges.mexc_api import MexcApi
from exhchanges.ramizenx_api import RamzinexApi
from .base_arbitrage import Arbitrage
from data_storage.csv_interface import save_ramzinex_nobitex_arbitrage_to_csv, get_symbol_pair_id_in_mexc_and_ramzinex


class RamzinexMexcArbitrage(Arbitrage):

    def __init__(self, ramzinex_api: RamzinexApi, mexc_api: MexcApi):
        self.ramzinex_api = ramzinex_api
        self.mexc_api = mexc_api
        self.ramzinex_mexc_symbol_id_equivalent_pair = get_symbol_pair_id_in_mexc_and_ramzinex(
            "symbol_pair_id_mapping_ramzinex_mexc.csv")  # todo : getting this from csv config file
        self.last_opportunity = {item[0]: (0, 0) for item in self.ramzinex_mexc_symbol_id_equivalent_pair}

    async def find_arbitrage_opportunity(self):
        """this method find all opportunity for getting arbitrage from ramzinex and mexc"""
        while True:
            # Run both functions asynchronously
            task1 = asyncio.create_task(self.ramzinex_api.update_all_order_book())
            task2 = asyncio.create_task(self.mexc_api.update_all_order_book())

            # Wait for both tasks to complete
            results = await asyncio.gather(task1, task2)

            if results[0] is None or results[1] is None:
                print(colored("Error in update order book ", "red"))
                time.sleep(1)
                continue

            ramzinex_all_order_book = self.ramzinex_api.all_order_book
            mexc_all_order_book = self.mexc_api.all_order_book

            for symbol_id_equivalent in self.ramzinex_mexc_symbol_id_equivalent_pair:
                mexc_symbol, ramzinex_pair_id, mexc_to_ramzinex_unit_ratio = symbol_id_equivalent
                try:
                    mexc_symbol_order_book = mexc_all_order_book[mexc_symbol]
                    ramzinex_pair_id_order_book = ramzinex_all_order_book[ramzinex_pair_id]

                    self.check_latest_orders(mexc_symbol_order_book, ramzinex_pair_id_order_book,
                                             mexc_to_ramzinex_unit_ratio)

                except Exception as e:
                    print("error in getting and process " + str(mexc_symbol) + " orderbooks : " + str(e))

            # time.sleep(1)

    def check_latest_orders(self, mexc_order_book: OrderBook, ramzinex_order_book: OrderBook,
                            mexc_to_ramzinex_unit_ratio: float, exchanges="ramzinex-mexc"):
        """this method getting latest orders in order book and checking them for finding arbitrage opportunity"""
        mexc_highest_bid = mexc_order_book.get_highest_bid_order()
        mexc_lowest_ask = mexc_order_book.get_lowest_ask_order()

        mexc_lowest_ask_price, mexc_highest_bid_price = mexc_lowest_ask.price, mexc_highest_bid.price
        mexc_lowest_ask_volume, mexc_highest_bid_volume = mexc_lowest_ask.volume, mexc_highest_bid.volume

        ramzinex_highest_bid = ramzinex_order_book.get_highest_bid_order()
        ramzinex_lowest_ask = ramzinex_order_book.get_lowest_ask_order()

        ramzinex_lowest_ask_price, ramzinex_highest_bid_price = ramzinex_lowest_ask.price, ramzinex_highest_bid.price
        ramzinex_lowest_ask_volume, ramzinex_highest_bid_volume = ramzinex_lowest_ask.volume, ramzinex_highest_bid.volume

        if mexc_highest_bid_price > mexc_lowest_ask_price:
            error_message = "ERROR IN MEXC ORDER BOOK :" + mexc_order_book.symbol
            save_errors_to_log_file(str(error_message))
            return
        if ramzinex_highest_bid_price > ramzinex_lowest_ask_price:
            error_message = "ERROR IN RAMZINEX ORDER BOOK :" + str(ramzinex_order_book.pair_id)
            print(error_message)
            save_errors_to_log_file(str(error_message))
            return

        # apply The ratio of mexc unit to Ramzinex
        ramzinex_highest_bid_price *= mexc_to_ramzinex_unit_ratio
        ramzinex_lowest_ask_price *= mexc_to_ramzinex_unit_ratio
        ramzinex_highest_bid_volume /= mexc_to_ramzinex_unit_ratio
        ramzinex_lowest_ask_volume /= mexc_to_ramzinex_unit_ratio

        print("Exchange      Lowest Ask     Highest Bid")
        print(f"MEXC       {mexc_lowest_ask.price:<14} {mexc_highest_bid.price}")
        print(f"RAMZINEX      {ramzinex_lowest_ask.price:<14} {ramzinex_highest_bid.price}")

        action = 0
        benefit = 0
        percent = 0
        if mexc_lowest_ask_price < ramzinex_highest_bid_price:
            volume = min(mexc_lowest_ask_volume, ramzinex_highest_bid_volume)
            benefit = volume * (ramzinex_highest_bid_price - mexc_lowest_ask_price)
            percent = ramzinex_highest_bid_price / mexc_lowest_ask_price
            opportunity = (ramzinex_highest_bid_price, mexc_lowest_ask_price)
            buy_price = mexc_lowest_ask_price
            sell_price = ramzinex_highest_bid_price
            buy_side = "mexc"
            sell_side = "ramzinex"
            print("percent=", percent, " ramzinex_highest_bid=",
                  ramzinex_highest_bid_price, "nobitex_lowest_ask=", mexc_lowest_ask_price, "volume=", volume,
                  end=" ")

        if ramzinex_lowest_ask_price < mexc_highest_bid_price:
            volume = min(mexc_highest_bid_volume, ramzinex_lowest_ask_volume)
            benefit = volume * (mexc_highest_bid_price - ramzinex_lowest_ask_price)
            percent = mexc_highest_bid_price / ramzinex_lowest_ask_price
            opportunity = (mexc_highest_bid_price, ramzinex_lowest_ask_price)
            buy_price = ramzinex_lowest_ask_price
            sell_price = mexc_highest_bid_price
            buy_side = "ramzinex"
            sell_side = "mexc"
            print("percent=", percent, " nobitex_highest_bid=",
                  mexc_highest_bid_price, " ramzinex_lowest_ask=", ramzinex_lowest_ask_price, " volume=", volume,
                  end=" ")

        if benefit > 0:
            print(exchanges, " symbol in mexc=", mexc_order_book.symbol, " pair_id in ramzinex=",
                  ramzinex_order_book.pair_id, " benefit = ", benefit, "\n")
            if self.last_opportunity[mexc_order_book.symbol][0] != opportunity[0] and \
                    self.last_opportunity[mexc_order_book.symbol][1] != opportunity[1]:
                action = 1
                self.last_opportunity[mexc_order_book.symbol] = opportunity
            save_ramzinex_nobitex_arbitrage_to_csv("MEXC",mexc_order_book, ramzinex_order_book, mexc_lowest_ask,
                                                   mexc_highest_bid,
                                                   ramzinex_lowest_ask, ramzinex_highest_bid, benefit, percent, action,
                                                   mexc_to_ramzinex_unit_ratio, buy_price, sell_price, buy_side,
                                                   sell_side, volume)
        else:
            print("no opportunity :(")
