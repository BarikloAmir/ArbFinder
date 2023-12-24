import csv
from time import sleep

import requests

symbol_in_ramzinex_and_pair_id_in_ramzinex = {
    "rb10irr": 309,
    "btcirr": 2,
    "usdtirr": 11,
    "100shibirr": 61,
    "dogeirr": 10,
    "solirr": 96,
    "adairr": 33,
    "winirr": 48,
    "revirr": 91,
    "filirr": 51,
    "telirr": 126,
    "compirr": 136,
    "1000bttirr": 39,
    "vetirr": 46,
    "thetairr": 44,
    "atomirr": 42,
    "chzirr": 40,
    "AAVEirr": 36,
    "uniirr": 34,
    "ethirr": 3,
    "hotirr": 52,
    "dotirr": 29,
    "xrpirr": 4,
    "bchirr": 23,
    "trxirr": 25,
    "ltcirr": 5,
    "bnbirr": 17,
    "xlmirr": 19,
    "etcirr": 21,
    "linkirr": 26,
    "btcusdt": 12,
    "ethusdt": 13,
    "AAVEusdt": 37,
    "dotusdt": 31,
    "bchusdt": 24,
    "trxusdt": 27,
    "ltcusdt": 15,
    "bnbusdt": 18,
    "etcusdt": 22,
    "linkusdt": 38,
    "uniusdt": 35,
    "atomusdt": 43,
    "thetausdt": 45,
    "1m-babydogeirr": 256,
    "egldirr": 257,
    "lrcirr": 258,
    "mboxirr": 259,
    "100starlirr": 260,
    "1000elonirr": 261,
    "safemoonirr": 262,
    "arvirr": 263,
    "vrairr": 264,
    "1000nftirr": 265,
    "nwcirr": 266,
    "nearirr": 267,
    "cotiirr": 268,
    "celrirr": 269,
    "zilirr": 270,
    "dentirr": 271,
    "toncoinirr": 272,
    "100flokiirr": 273,
    "fegirr": 274,
    "ampirr": 275,
    "kavairr": 276,
    "portoirr": 277,
    "lazioirr": 278,
    "juvirr": 279,
    "runeirr": 280,
    "fttirr": 281,
    "grtirr": 282,
    "xtzirr": 283,
    "iotairr": 284,
    "crvirr": 285,
    "kcsirr": 286,
    "okbirr": 287,
    "roseirr": 288,
    "htirr": 289,
    "omgirr": 290,
    "zecirr": 291,
    "ontirr": 292,
    "c98irr": 293,
    "racairr": 294,
    "1m-kishuirr": 295,
    "paxgirr": 296,
    "psgirr": 297,
    "apeirr": 298,
    "gmtirr": 299,
    "hegicirr": 300,
    "lokairr": 301,
    "ookiirr": 303,
    "bswirr": 305,
    "100xecirr": 306,
    "lunairr": 307,
    "100luncirr": 308,
    "usdcirr": 310,
    "flowirr": 311,
    "achirr": 312,
    "leverirr": 313,
    "qntirr": 314,
    "blzirr": 315,
    "fluxirr": 316,
    "tlmirr": 317,
    "jstirr": 318,
    "tfuelirr": 319,
    "galirr": 320,
    "api3irr": 321,
    "ankrirr": 66,
    "ensirr": 322,
    "srmirr": 323,
    "sushiirr": 324,
    "dexeirr": 325,
    "wavesirr": 326,
    "maticirr": 71,
    "duskirr": 327,
    "nexoirr": 328,
    "stgirr": 329,
    "badgerirr": 330,
    "bntirr": 331,
    "eosirr": 76,
    "titanirr": 332,
    "keyirr": 334,
    "jasmyirr": 335,
    "wooirr": 336,
    "sxpirr": 81,
    "ldoirr": 337,
    "chrirr": 338,
    "ancirr": 339,
    "vgxirr": 340,
    "1inchirr": 86,
    "fetirr": 342,
    "agixirr": 343,
    "bitirr": 344,
    "fxsirr": 345,
    "imxirr": 346,
    "dcirr": 347,
    "reefirr": 348,
    "storjirr": 349,
    "tirr": 350,
    "boneirr": 351,
    "blurirr": 352,
    "gftirr": 353,
    "bicoirr": 354,
    "rndrirr": 355,
    "1000briseirr": 356,
    "icpirr": 101,
    "hifiirr": 357,
    "maskirr": 358,
    "1000voltirr": 359,
    "arbirr": 360,
    "burgerirr": 106,
    "fttusdt": 362,
    "maticusdt": 363,
    "maskusdt": 364,
    "ldousdt": 365,
    "100pepeirr": 366,
    "1m-aidogeirr": 367,
    "1m-ladysirr": 368,
    "injirr": 369,
    "gmxirr": 370,
    "magicirr": 371,
    "cakeirr": 116,
    "100bobirr": 372,
    "arpairr": 373,
    "snxirr": 374,
    "100rfdirr": 375,
    "wldirr": 376,
    "ksmirr": 121,
    "cyberirr": 377,
    "pendleirr": 378,
    "mavirr": 379,
    "spairr": 380,
    "arkmirr": 381,
    "bigtimeirr": 382,
    "akroirr": 383,
    "sntirr": 384,
    "memeirr": 385,
    "ognirr": 386,
    "bsvirr": 131,
    "mtlirr": 387,
    "sukuirr": 388,
    "lqtyirr": 389,
    "glmirr": 390,
    "sklirr": 391,
    "ustcirr": 392,
    "ustcusdt": 393,
    "100luncusdt": 394,
    "polirr": 395,
    "atorirr": 396,
    "mkrirr": 141,
    "manairr": 146,
    "oneirr": 152,
    "adausdt": 158,
    "filusdt": 164,
    "compusdt": 170,
    "mkrusdt": 176,
    "bsvusdt": 182,
    "ksmusdt": 188,
    "cakeusdt": 194,
    "burgerusdt": 206,
    "icpusdt": 212,
    "solusdt": 218,
    "eosusdt": 224,
    "1inchusdt": 230,
    "sxpusdt": 236,
    "ftmirr": 237,
    "ftmusdt": 238,
    "daiirr": 239,
    "daiusdt": 240,
    "hexirr": 241,
    "manausdt": 242,
    "axsirr": 243,
    "blokirr": 244,
    "axsusdt": 245,
    "slpirr": 246,
    "enjirr": 247,
    "sandirr": 248,
    "galairr": 249,
    "aliceirr": 250,
    "dydxirr": 251,
    "audioirr": 252,
    "batirr": 253,
    "croirr": 254,
    "avaxirr": 255,
    "pundixirr": 50,
    "twtirr": 57
}


def fetch_depth_data(symbol):
    url = f"https://api.mexc.com/api/v3/depth/?symbol={symbol}&limit=2"
    response = requests.get(url)

    if response.status_code == 200:
        return 1
    else:
        print(f"Error {response.status_code}: {response.text} and symbol: {symbol}")
        return None


ok_list = []
not_ok_list = []
for symbol in symbol_in_ramzinex_and_pair_id_in_ramzinex.keys():

    if "irr" in symbol:
        continue
    ramzinex_symbol = symbol
    symbol = symbol.upper()
    # print(symbol)
    if fetch_depth_data(symbol):
        ok_list.append(symbol)
        print(symbol_in_ramzinex_and_pair_id_in_ramzinex[ramzinex_symbol], ",", symbol, ",1")
    else:
        not_ok_list.append(symbol)
    sleep(0.01)

print(ok_list)
print(not_ok_list)
