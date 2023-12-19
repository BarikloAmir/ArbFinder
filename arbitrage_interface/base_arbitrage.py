from data_storage.models import OrderBook


class Arbitrage:

    def check_latest_orders(self, exchange1_order_book: OrderBook, exchange2_order_book: OrderBook,
                            exchanges="ramzinex-nobitex"):
        """this method getting latest orders in order book and checking them for finding arbitrage opportunity"""
        exchange1_highest_bid = exchange1_order_book.get_highest_bid_order()
        exchange1_lowest_ask = exchange1_order_book.get_lowest_ask_order()

        exchange2_highest_bid = exchange2_order_book.get_highest_bid_order()
        exchange2_lowest_ask = exchange2_order_book.get_lowest_ask_order()

        symbol_exchange1 = exchange1_order_book.symbol
        symbol_exchange2 = exchange2_order_book.symbol

        benefit = 0
        if exchange1_lowest_ask.price < exchange2_highest_bid.price:
            benefit = exchange1_lowest_ask.volume * (exchange2_highest_bid.price - exchange1_lowest_ask.price)

        if exchange1_highest_bid.price > exchange2_lowest_ask.price:
            benefit = exchange2_lowest_ask.volume * (exchange1_highest_bid.price - exchange2_lowest_ask.price)

        if benefit > 0:
            self.save_opportunity(exchanges=exchanges, symbol_exchange1=str(symbol_exchange1),
                                  symbol_exchange2=str(symbol_exchange2), benefit=benefit)


    def save_opportunity(self, exchanges="ramzinex-nobitex", symbol_exchange1="btcirt", symbol_exchange2="2",
                         benefit=0):
        print(exchanges, ". symbol in exchange1 = ", symbol_exchange1, "symbol in exchange2 = ", symbol_exchange2,
              ". benefit = ", str(benefit))

