import asyncio

from arbitrage_interface.ramzinex_mexc_arbitrage import RamzinexMexcArbitrage
from arbitrage_interface.ramzinex_nobitex_arbitrage import RamzinexNobitexArbitrage
from exhchanges.mexc_api import MexcApi
from exhchanges.nobitex_api import NobitexApi
from exhchanges.ramizenx_api import RamzinexApi


def main():
    # ramzinex_nobitex_arbitrage = RamzinexNobitexArbitrage(RamzinexApi(), NobitexApi())
    # asyncio.run(ramzinex_nobitex_arbitrage.find_arbitrage_opportunity())

    mexc_symbols = ['BTCUSDT', 'ETHUSDT', 'AAVEUSDT', 'DOTUSDT', 'BCHUSDT', 'TRXUSDT', 'LTCUSDT', 'BNBUSDT', 'ETCUSDT',
                    'LINKUSDT', 'UNIUSDT', 'ATOMUSDT', 'FTTUSDT', 'MATICUSDT', 'MASKUSDT', 'LDOUSDT', 'USTCUSDT',
                    'ADAUSDT', 'FILUSDT', 'COMPUSDT', 'MKRUSDT', 'BSVUSDT', 'KSMUSDT', 'CAKEUSDT', 'BURGERUSDT',
                    'ICPUSDT', 'SOLUSDT', 'EOSUSDT', '1INCHUSDT', 'SXPUSDT', 'FTMUSDT', 'DAIUSDT', 'MANAUSDT',
                    'AXSUSDT']

    ramzinex_mexc_arbitrage = RamzinexMexcArbitrage(RamzinexApi(), MexcApi(mexc_symbols))
    asyncio.run(ramzinex_mexc_arbitrage.find_arbitrage_opportunity())


if __name__ == '__main__':
    main()
