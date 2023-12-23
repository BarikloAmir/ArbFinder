import csv
from datetime import datetime


def save_ramzinex_nobitex_arbitrage_to_csv(nobitex_order_book, ramzinex_order_book, nobitex_lowest_ask,
                                           nobitex_highest_bid,
                                           ramzinex_lowest_ask, ramzinex_highest_bid, benefit, percent, action,
                                           nobitex_to_ramzinex_unit_ratio, buy_price, sell_price, buy_side, sell_side,
                                           volume):
    """
    this function saving information to csv file and update that
    :param buy_side:
    :param sell_side:
    :param sell_price:
    :param buy_price:
    :param percent:
    :param nobitex_order_book:
    :param ramzinex_order_book:
    :param nobitex_lowest_ask:
    :param nobitex_highest_bid:
    :param ramzinex_lowest_ask:
    :param ramzinex_highest_bid:
    :param benefit:
    :param action:
    :param nobitex_to_ramzinex_unit_ratio:
    :return:
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('arbitrage_data_v2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            # Write header if the file is empty
            writer.writerow(
                ['Timestamp', 'NOBITEX Last Update Time ', 'RAMZINEX Last Update Time', 'Exchange',
                 'Symbol (NOBITEX)', 'Pair ID (RAMZINEX)', 'Lowest Ask Price (NOBITEX)',
                 'Highest Bid Price (NOBITEX)', 'Lowest Ask Price (RAMZINEX)', 'Highest Bid Price (RAMZINEX)',
                 'Lowest Ask Volume(NOBITEX)',
                 'Highest Bid Volume (NOBITEX)', 'Lowest Ask Volume (RAMZINEX)', 'Highest Bid Volume (RAMZINEX)',
                 'Benefit', 'Percent', 'Action', "Nobitex To Ramzinex Unit Ratio", "Buy Price", "Sell Price",
                 "Buy Side", "Sell Side", "Our trading volume"])

        writer.writerow([timestamp, nobitex_order_book.last_update_time,
                         ramzinex_order_book.last_update_time, 'NOBITEX-RAMZINEX', nobitex_order_book.symbol,
                         ramzinex_order_book.pair_id,
                         nobitex_lowest_ask.price, nobitex_highest_bid.price,
                         ramzinex_lowest_ask.price, ramzinex_highest_bid.price, nobitex_lowest_ask.volume,
                         nobitex_highest_bid.volume,
                         ramzinex_lowest_ask.volume, ramzinex_highest_bid.volume, benefit, percent, action,
                         nobitex_to_ramzinex_unit_ratio, buy_price, sell_price, buy_side, sell_side, volume])


def get_symbol_pair_id(csv_file_address, symbol_key, id_key, ratio_key):
    with open(csv_file_address, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row[symbol_key], int(row[id_key]), int(row[ratio_key])) for row in reader]


def get_symbol_pair_id_in_nobitex_and_ramzinex(csv_file_address):
    return get_symbol_pair_id(csv_file_address, 'nobitex_symbol', 'ramzinex_pair_id', 'nobitex/ramzinex')


def get_symbol_pair_id_in_mexc_and_ramzinex(csv_file_address):
    return get_symbol_pair_id(csv_file_address, 'mexc_symbol', 'ramzinex_pair_id', 'mexc/ramzinex')


