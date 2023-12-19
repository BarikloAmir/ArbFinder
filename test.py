import csv

import requests

nobitex_symbols = ['BTCIRT', 'BTCUSDT', 'ETHIRT', 'ETHUSDT', 'LTCIRT', 'LTCUSDT', 'USDTIRT', 'XRPIRT', 'XRPUSDT',
                   'BCHIRT', 'BCHUSDT', 'BNBIRT', 'BNBUSDT', 'EOSIRT', 'EOSUSDT', 'DOGEIRT', 'DOGEUSDT', 'XLMIRT',
                   'XLMUSDT', 'TRXIRT', 'TRXUSDT', 'ADAIRT', 'ADAUSDT', 'XMRIRT', 'XMRUSDT', 'ETCIRT', 'ETCUSDT',
                   'XTZIRT', 'XTZUSDT', 'PMNUSDT', 'LINKIRT', 'LINKUSDT', 'DAIIRT', 'DAIUSDT', 'DOTIRT', 'DOTUSDT',
                   'UNIIRT', 'UNIUSDT', 'AAVEIRT', 'AAVEUSDT', 'SOLIRT', 'SOLUSDT', 'MATICIRT', 'MATICUSDT', 'FILIRT',
                   'FILUSDT', 'GRTIRT', 'GRTUSDT', 'SHIBIRT', 'SHIBUSDT', '1INCHIRT', '1INCHUSDT', 'ATOMIRT',
                   'ATOMUSDT', 'AVAXIRT', 'AVAXUSDT', 'AXSIRT', 'AXSUSDT', 'BALIRT', 'BALUSDT', 'BANDIRT', 'BANDUSDT',
                   'BATIRT', 'BATUSDT', '1M_BTTIRT', '1M_BTTUSDT', 'CELRIRT', 'CELRUSDT', 'COMPIRT', 'COMPUSDT',
                   'EGLDIRT', 'EGLDUSDT', 'FTMIRT', 'FTMUSDT', 'GALAIRT', 'GALAUSDT', 'MASKIRT', 'MASKUSDT', 'MKRIRT',
                   'MKRUSDT', 'NEARIRT', 'NEARUSDT', 'SNXIRT', 'SNXUSDT', 'SUSHIIRT', 'SUSHIUSDT', 'YFIIRT', 'YFIUSDT',
                   'MANAIRT', 'MANAUSDT', 'SANDIRT', 'SANDUSDT', 'APEIRT', 'APEUSDT', 'ONEIRT', 'ONEUSDT', 'WBTCIRT',
                   'WBTCUSDT', 'USDCIRT', 'USDCUSDT', 'ALGOIRT', 'ALGOUSDT', 'GMTIRT', 'GMTUSDT', 'CHZIRT', 'CHZUSDT',
                   'QNTIRT', 'QNTUSDT', 'BUSDIRT', 'BUSDUSDT', 'FLOWIRT', 'FLOWUSDT', 'HBARIRT', 'HBARUSDT', 'EGALAIRT',
                   'EGALAUSDT', 'ENJIRT', 'ENJUSDT', 'CRVIRT', 'CRVUSDT', 'LDOIRT', 'LDOUSDT', 'DYDXIRT', 'DYDXUSDT',
                   'APTIRT', 'APTUSDT', 'FLRIRT', 'FLRUSDT', 'LRCIRT', 'LRCUSDT', 'ENSIRT', 'ENSUSDT', 'LPTIRT',
                   'LPTUSDT', 'GLMIRT', 'GLMUSDT', 'API3IRT', 'API3USDT', 'DAOIRT', 'DAOUSDT', 'CVCIRT', 'CVCUSDT',
                   'NMRIRT', 'NMRUSDT', 'STORJIRT', 'STORJUSDT', 'CVXIRT', 'CVXUSDT', 'SNTIRT', 'SNTUSDT', 'SLPIRT',
                   'SLPUSDT', '1M_NFTIRT', '1M_NFTUSDT', 'ANTIRT', 'ANTUSDT', 'ILVIRT', 'ILVUSDT', 'TIRT', 'TUSDT',
                   '1B_BABYDOGEIRT', '1B_BABYDOGEUSDT', 'TONIRT', 'TONUSDT', '100K_FLOKIIRT', '100K_FLOKIUSDT',
                   'ZRXIRT', 'ZRXUSDT', 'IMXIRT', 'IMXUSDT', 'MDTIRT', 'MDTUSDT', 'BLURIRT', 'BLURUSDT', 'MAGICIRT',
                   'MAGICUSDT', 'ARBIRT', 'ARBUSDT', 'GMXIRT', 'GMXUSDT', 'SSVIRT', 'SSVUSDT', 'WLDIRT', 'WLDUSDT',
                   'OMGIRT', 'OMGUSDT', 'RDNTIRT', 'RDNTUSDT', 'JSTIRT', 'JSTUSDT', 'RNDRIRT', 'RNDRUSDT', 'BICOIRT',
                   'BICOUSDT', 'WOOIRT', 'WOOUSDT', 'SKLIRT', 'SKLUSDT', 'GALIRT', 'GALUSDT']

irt_counter = 0
usdt_counter = 0

for item in nobitex_symbols:
    if "IRT" in item:
        irt_counter += 1
    elif "USDT" in item:
        usdt_counter += 1
    else:
        print("not usual : " + item)

print("original nobitex irt = ", irt_counter)
print("original nobitex usdt = ", usdt_counter)

response = requests.get('https://publicapi.ramzinex.com/exchange/api/v1.0/exchange/pairs')
response.raise_for_status()
data_json = response.json()
pair_id_dict = {entry["tv_symbol"]["ramzinex"]: entry["pair_id"] for entry in data_json["data"]}


print("pair id dict in ramzinex: ", pair_id_dict)
nobitex_symbol_pair_id_ramzinex = {}

for key in pair_id_dict.keys():
    irt_key = key.replace("irr", "irt")
    if irt_key.upper() in nobitex_symbols:
        print(key + " : " + str(pair_id_dict[key]))
        nobitex_symbol_pair_id_ramzinex[irt_key.upper()] = pair_id_dict[key]
    else:
        print(key + " : " + str(-1))

print(nobitex_symbol_pair_id_ramzinex)
print(len(nobitex_symbol_pair_id_ramzinex))

new_irt_counter = 0
new_usdt_counter = 0
for item in nobitex_symbol_pair_id_ramzinex.keys():
    if "IRT" in item:
        new_irt_counter += 1
    elif "USDT" in item:
        new_usdt_counter += 1
    else:
        print("not usual : " + item)
print("final irt : ", new_irt_counter)
print("final usdt : ", new_usdt_counter)

irt_symbol_that_not_in_ramzinex = []
usdt_symbol_that_not_in_ramzinex = []
for item in nobitex_symbols:
    if not item in nobitex_symbol_pair_id_ramzinex.keys():
        if "IRT" in item:
            irt_symbol_that_not_in_ramzinex.append(item)
        if 'USDT' in item:
            usdt_symbol_that_not_in_ramzinex.append(item)

print("irt_symbol_that_not_in_ramzinex: ",irt_symbol_that_not_in_ramzinex)
print("usdt_symbol_that_not_in_ramzinex: ", usdt_symbol_that_not_in_ramzinex)

