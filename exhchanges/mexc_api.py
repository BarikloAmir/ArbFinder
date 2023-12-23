from data_storage.models import OrderBook, Order, OrderType
import requests
from .exchange_api import ExchangeApi
from typing import List, Dict
import aiohttp
import asyncio


class MexcApi(ExchangeApi):
    BASE_URL = "https://api.mexc.com/api/v3/depth/?symbol={}&limit=2"

    def __init__(self, symbols: List[str]):
        self.all_order_book = None
        self.symbols = symbols

    async def fetch_depth_data(self, session, symbol):
        async with session.get(self.BASE_URL.format(symbol)) as response:
            if response.status == 200:
                return symbol, await response.json()
            else:
                return symbol, f"Error {response.status}: {await response.text()}"

    async def get_all_responses(self):
        results = {}
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_depth_data(session, symbol) for symbol in self.symbols]
            responses = await asyncio.gather(*tasks)
            for symbol, data in responses:
                results[symbol] = data
        return results

    async def update_all_order_book(self):
        """this method get order_books of all symbol and return all orderbook from nobitex """
        try:
            all_symbol_data = await self.get_all_responses()
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
                        symbol_data.get('bids', [])]
                asks = [Order(OrderType.ASK, float(price), float(volume)) for price, volume in
                        symbol_data.get('asks', [])]
                all_order_book[symbol] = OrderBook(bids, asks, symbol=symbol, last_update_time=last_update_time)
            except Exception as e:
                print("unexpected error in reading order book of " + symbol + " symbol : ", e)

        self.all_order_book = all_order_book
        return 1



