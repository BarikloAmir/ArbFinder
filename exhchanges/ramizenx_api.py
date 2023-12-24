from typing import Dict

from data_storage.models import OrderBook, Order, OrderType
import requests
from .exchange_api import ExchangeApi


class RamzinexApi(ExchangeApi):
    RAMZINEX_ORDER_BOOK_ENDPOINT = "https://publicapi.ramzinex.com/exchange/api/v1.0/exchange/orderbooks/pair_id/buys_sells"

    def __init__(self):
        self.all_order_book = None

    def get_symbol_order_book_endpoint(self, pair_id: int) -> str:
        return self.RAMZINEX_ORDER_BOOK_ENDPOINT.replace("pair_id", str(pair_id))

    def get_all_order_book_endpoint(self):
        return self.RAMZINEX_ORDER_BOOK_ENDPOINT.replace("pair_id/", "")

    def get_symbol_order_book(self, pair_id: int) -> OrderBook | None:
        """ this method get order book of input pair id  and return orderbook of that from ramzinex"""
        symbol_order_book_endpoint = self.get_symbol_order_book_endpoint(pair_id)
        try:
            response = requests.get(symbol_order_book_endpoint)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            data = response.json()

        except requests.RequestException as e:
            print(f"Error making API request: {e}")
            return None

        last_update_time = data.get('lastUpdate', 0)
        bids = [Order(OrderType.BID, bid[0], bid[1]) for bid in data['data']['buys']]
        asks = [Order(OrderType.ASK, ask[0], ask[1]) for ask in data['data']['sells']]
        return OrderBook(bids, asks, pair_id=pair_id, last_update_time=last_update_time)

    async def update_all_order_book(self):
        """
        this method get order_books of all symbol and return all orderbook from nobitex
        :return
        """
        all_symbol_order_book_endpoint = self.get_all_order_book_endpoint()
        try:
            response = requests.get(all_symbol_order_book_endpoint)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            all_symbol_data = response.json()
        except requests.RequestException as e:
            print(f"Error making API request: {e}")
            return None

        all_order_book = {}  # this dictionary saving all orderbooks with pair_id key
        for pair_id, symbol_data in all_symbol_data.items():
            try:
                rial_to_tether = 1
                if pair_id == "260":
                    rial_to_tether = self.get_tether_price()

                last_update_time = symbol_data.get('lastUpdate', 0)
                bids = [Order(OrderType.BID, bid[0] / rial_to_tether, bid[1]) for bid in
                        symbol_data['buys']]

                asks = [Order(OrderType.ASK, ask[0] / rial_to_tether, ask[1]) for ask in
                        symbol_data['sells']]

                all_order_book[int(pair_id)] = OrderBook(bids, asks, pair_id=int(pair_id),
                                                         last_update_time=last_update_time)
            except Exception as e:
                print("unexpected error in reading order book of " + pair_id + " symbol : ", e)

        self.all_order_book = all_order_book
        return 1

    def get_tether_price(self):
        tether_order_book = self.get_symbol_order_book(11)
        return tether_order_book.get_lowest_ask_order().price
