from binance.client import Client
from binance.enums import *
from binance.exceptions import *
import sys
import os
import math
import json
import requests
import webbrowser
import time


def float_to_string(number, precision=10):
    return '{0:.{prec}f}'.format(
        number, prec=precision,
    ).rstrip('0').rstrip('.') or '0'


# make log file
logfile = open("log.txt", "w+")


def log(information):
    logfile.writelines(information)


# load settings
configFiles = ["default-config.json", "config.json"]
if os.path.exists(configFiles[1]):
    # read json files
    for file in configFiles:
        f = open(file, )
        data = json.load(f)
        if 'apiKey' in data: apiKey = data['apiKey']
        if 'apiSecret' in data: apiSecret = data['apiSecret']
        if 'coinPair' in data: coinPair = data['coinPair']
        if 'secondsAveragePrice' in data: secondsAveragePrice = float(data['secondsAveragePrice'])
        if 'buyLimit' in data: buyLimit = data['buyLimit']
        if 'percentOfWallet' in data: percentOfWallet = float(data['percentOfWallet']) / 100
        if 'manualBTC' in data: manualBTC = float(data['manualBTC'])
        if 'profitMargin' in data: profitMargin = float(data['profitMargin']) / 100
        if 'stopLoss' in data: stopLoss = float(data['stopLoss'])
        f.close()
else:
    # if no custom config file created, make one
    d = open(configFiles[0])
    c = open(configFiles[1], "w+")
    c.write(d.read())
    c.close()
    d.close()
    log("No custom File. Making one")
    print("\nNo custom Config file detected. We just created one for you. Change settings as you like.\n")
    quit()

# create binance Client
client = Client(apiKey, apiSecret)

# get all symbols with coinPair as quote
tickers = client.get_all_tickers()
symbols = []
for ticker in tickers:
    if coinPair in ticker["symbol"]:
        symbols.append(ticker["symbol"])

# cache average prices
print("Caching all {} pairs average prices...\nThis can take a while. Please, be patient...\n".format(coinPair))
tickers = client.get_ticker()
averagePrices = []
for ticker in tickers:
    if coinPair in ticker['symbol']:
        averagePrices.append(dict(symbol=ticker['symbol'], wAvgPrice=ticker["weightedAvgPrice"]))


# Getting btc conversion
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

print(roundedPriceToSell)
print(float_to_string(stopLoss * coinPriceBought, int(- math.log10(minPrice))))

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
        e.message + "Please use https://binance-docs.github.io/apidocs/spot/en/#error-codes to find greater details "
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

# close Log file
logfile.close()

sys.exit()
