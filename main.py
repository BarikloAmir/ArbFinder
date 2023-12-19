import asyncio

from arbitrage_interface.ramzinex_nobitex_arbitrage import RamzinexNobitexArbitrage
from exhchanges.nobitex_api import NobitexApi
from exhchanges.ramizenx_api import RamzinexApi


def main():

    ramzinex_nobitex_arbitrage = RamzinexNobitexArbitrage(RamzinexApi(), NobitexApi())
    asyncio.run(ramzinex_nobitex_arbitrage.find_arbitrage_opportunity())


if __name__ == '__main__':
    main()
