from typing import List
from enum import Enum


class OrderType(Enum):
    ASK = "ask"
    BID = "bid"


class Order:

    def __init__(self, order_type: OrderType, price: float, volume: float):
        self.order_type = order_type
        self.price = price
        self.volume = volume


class OrderBook:

    def __init__(self, bids: List[Order], asks: List[Order], symbol: str = "", last_update_time: int = 0,
                 pair_id: int = -1):
        self.symbol = symbol
        self.last_update_time = last_update_time
        self.pair_id = pair_id
        self.bids = bids
        self.asks = asks

    def get_highest_bid_order(self):
        return max(self.bids, key=lambda x: x.price)

    def get_lowest_ask_order(self):
        return min(self.asks, key=lambda x: x.price)
