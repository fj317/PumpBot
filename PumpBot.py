from binance.client import Client
from binance.enums import *
from binance.exceptions import *
import sys
import math
import json
import requests
import webbrowser


# UTILS
def float_to_string(number, precision=10):
    return '{0:.{prec}f}'.format(
        number, prec=precision,
    ).rstrip('0').rstrip('.') or '0'


def log(information):
    logfile.writelines(information)


# make log file
logfile = open("log.txt", "w+")

# read json file
f = open('keys.json', )
data = json.load(f)
apiKey = data['apiKey']
apiSecret = data['apiSecret']
if (apiKey == "") or (apiSecret == ""):
    log("API Keys Missing")
    sys.exit("One or Both of you API Keys are missing.\n"
    "Please open the keys.json to include them.")

f = open('config.json', )
data = json.load(f)
# loading config settings
coinPair = data['coinPair']
buyLimit = data['buyLimit']
percentOfWallet = float(data['percentOfWallet']) / 100
manualBTC = float(data['manualBTC'])
profitMargin = float(data['profitMargin']) / 100
stopLoss = float(data['stopLoss'])

# create binance Client
client = Client(apiKey, apiSecret)

# get all symbols with coinPair as quote
tickers = client.get_all_tickers()
symbols = []
for ticker in tickers:
    if coinPair in ticker["symbol"]: symbols.append(ticker["symbol"])

# cache average prices
print("Caching all {} pairs average prices...\nThis can take a while. Please, be patient...\n".format(coinPair))
tickers = client.get_ticker()
averagePrices = []
for ticker in tickers:
    if coinPair in ticker['symbol']:
        averagePrices.append(dict(symbol=ticker['symbol'], wAvgPrice=ticker["weightedAvgPrice"]))

# getting btc conversion
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
data = response.json()
in_USD = float((data['bpi']['USD']['rate_float']))

# find amount of bitcoin to use
try:
    BTCBalance = float(client.get_asset_balance(asset='BTC')['free'])
except (BinanceRequestException, BinanceAPIException):
    log("Invalid API keys.")
    sys.exit("Invalid API keys.")

# decide if use percentage or manual amount
if manualBTC <= 0:
    BTCtoSell = BTCBalance * percentOfWallet
else:
    BTCtoSell = manualBTC

# nice user message
print(''' 
 ___                                ___           _   
(  _`\                             (  _`\        ( )_ 
| |_) ) _   _   ___ ___   _ _      | (_) )   _   | ,_)
| ,__/'( ) ( )/' _ ` _ `\( '_`\    |  _ <' /'_`\ | |  
| |    | (_) || ( ) ( ) || (_) )   | (_) )( (_) )| |_ 
(_)    `\___/'(_) (_) (_)| ,__/'   (____/'`\___/'`\__)
                         | |                          
                         (_)                          ''')
# wait until coin input
print("\nInvesting amount for BTC: {}".format(BTCtoSell))
print("Investing amount in USD: {}".format(float_to_string((in_USD * BTCtoSell), 2)))
tradingPair = input("\nCoin pair: ").upper() + coinPair

# get trading pair price
try:
    price = float(client.get_avg_price(symbol=tradingPair)['price'])
except BinanceAPIException as e:
    if e.code == -1121:
        print(
            "Invalid trading pair given. Check your input is correct as well as config.json's 'coinPair' value to "
            "fix the error.")
    else:
        print("A BinanceAPI error has occurred. Code = " + str(e.code))
        print(
            e.message + "Please use https://github.com/binance/binance-spot-api-docs/blob/master/errors.md to find "
                        "greater details on error codes before raising an issue.")
    quit()
except Exception as d:
    print(d)
    print("An unknown error has occurred.")
    quit()

# calculate amount of coin to buy
amountOfCoin = BTCtoSell / price

# ensure buy limit is setup correctly
averagePrice = 0
for ticker in averagePrices:
    if ticker["symbol"] == tradingPair:
        averagePrice = ticker["wAvgPrice"]
if averagePrice == 0: averagePrice = price

# rounding the coin amount to the specified lot size
info = client.get_symbol_info(tradingPair)
minQty = float(info['filters'][2]['minQty'])
amountOfCoin = float_to_string(amountOfCoin, int(- math.log10(minQty)))

# rounding price to correct dp
minPrice = minQty = float(info['filters'][0]['minPrice'])
averagePrice = float(averagePrice) * buyLimit
averagePrice = float_to_string(averagePrice, int(- math.log10(minPrice)))

try:
    # buy order
    order = client.order_limit_buy(
        symbol=tradingPair,
        quantity=amountOfCoin,
        price=averagePrice)
    print('Buy order has been made!')
    coinOrderInfo = order["fills"][0]
    coinPriceBought = float(coinOrderInfo['price'])
    coinOrderQty = float(coinOrderInfo['qty'])
except BinanceAPIException as e:
    print("A BinanceAPI error has occurred. Code = " + str(e.code))
    print(
        e.message + "Please use https://github.com/binance/binance-spot-api-docs/blob/master/errors.md to find "
                    "greater details on error codes before raising an issue.")
    quit()
except Exception as d:
    print(d)
    print("An unknown error has occurred.")
    quit()

print('Processing sell order.')

# rounding sell price to correct dp
priceToSell = coinPriceBought * profitMargin
roundedPriceToSell = float_to_string(priceToSell, int(- math.log10(minPrice)))

# waits until the buy order has been confirmed 
orders = client.get_open_orders(symbol=tradingPair)
while client.get_open_orders(symbol=tradingPair):
    print("Waiting for coin to buy...")

try:
    # oco order (with stop loss)
    order = client.create_oco_order(
        symbol=tradingPair,
        quantity=coinOrderQty,
        side=SIDE_SELL,
        price=roundedPriceToSell,
        stopPrice=float_to_string(stopLoss * coinPriceBought, int(- math.log10(minPrice))),
        stopLimitPrice=float_to_string(stopLoss * coinPriceBought, int(- math.log10(minPrice))),
        stopLimitTimeInForce=TIME_IN_FORCE_GTC
    )
except BinanceAPIException as e:
    print("A BinanceAPI error has occurred. Code = " + str(e.code))
    print(
        e.message + "Please use https://github.com/binance/binance-spot-api-docs/blob/master/errors.md to find "
                    "greater details "
                    "on error codes before raising an issue.")
    quit()
except Exception as d:
    print(d)
    print("An unknown error has occurred.")
    quit()

print('Sell order has been made!')
# open binance page to trading pair
webbrowser.open('https://www.binance.com/en/trade/' + tradingPair)

# wait for Enter to close
input("\nPress Enter to Exit...")

# close Log file and exit
logfile.close()
sys.exit()
