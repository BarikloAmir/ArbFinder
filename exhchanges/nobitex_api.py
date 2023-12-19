from data_storage.models import OrderBook, Order, OrderType
import requests
from .exchange_api import ExchangeApi
from typing import List, Dict


class NobitexApi(ExchangeApi):
    NOBITEX_ORDER_BOOK_ENDPOINT = "https://api.nobitex.ir/v2/orderbook/"

    def __init__(self):
        self.all_order_book = None

    def get_symbol_order_book_endpoint(self, symbol: str) -> str:
        return self.NOBITEX_ORDER_BOOK_ENDPOINT + symbol

    def get_all_order_book_endpoint(self) -> str:
        return self.NOBITEX_ORDER_BOOK_ENDPOINT + "all"

    def get_symbol_order_book(self, symbol: str) -> OrderBook | None:
        """ this method get order book of input symbol and return orderbook of that from nobitex"""
        symbol_order_book_endpoint = self.get_symbol_order_book_endpoint(symbol)
        try:
            response = requests.get(symbol_order_book_endpoint)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            data = response.json()

        except requests.RequestException as e:
            print(f"Error making API request: {e}")
            return None

        last_update_time = data.get('lastUpdate', 0)
        bids = [Order(OrderType.BID, float(price), float(volume)) for price, volume in data.get('asks', [])]
        asks = [Order(OrderType.ASK, float(price), float(volume)) for price, volume in data.get('bids', [])]
        return OrderBook(bids, asks, symbol=symbol, last_update_time=last_update_time)

    async def update_all_order_book(self):
        """this method get order_books of all symbol and return all orderbook from nobitex """
        all_symbol_order_book_endpoint = self.get_all_order_book_endpoint()
        try:
            response = requests.get(all_symbol_order_book_endpoint)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            all_symbol_data = response.json()
        except requests.RequestException as e:
            print(f"Error making API request: {e}")
            return None

        all_order_book = {}  # this dictionary saving all orderbooks with symbol key
        for symbol, symbol_data in all_symbol_data.items():
            if symbol == "status":
                continue
            try:
                last_update_time = symbol_data.get('lastUpdate', 0)
                bids = [Order(OrderType.BID, float(price), float(volume)) for price, volume in
                        symbol_data.get('asks', [])]
                asks = [Order(OrderType.ASK, float(price), float(volume)) for price, volume in
                        symbol_data.get('bids', [])]
                all_order_book[symbol] = OrderBook(bids, asks, symbol=symbol, last_update_time=last_update_time)
            except Exception as e:
                print("unexpected error in reading order book of " + symbol + " symbol : ", e)

        self.all_order_book = all_order_book
        return 1
