from binance.client import Client
from binance.enums import *
from binance.exceptions import *
import math
import json
import webbrowser

def float_to_string(number, precision=10):
    return '{0:.{prec}f}'.format(
        number, prec=precision,
    ).rstrip('0').rstrip('.') or '0'

# read json file
f = open('config.json',)
data = json.load(f)
apiKey = data['apiKey']
apiSecret = data['apiSecret']
profitMargin = float(data['profitMargin']) / 100
percentOfWallet = float(data['percentOfWallet']) / 100
manualBTC = float(data['manualBTC'])
buyLimit = data['buyLimit']
stopLoss = data['stopLoss']
coinPair = data['coinPair']
getAveragePrice = data['getAveragePrice']
minutesAveragePrice = data['minutesAveragePrice']
client = Client(apiKey, apiSecret)

# find amount of bitcoin to use
try:
    BTCBalance = float(client.get_asset_balance(asset='BTC')['free'])
except:
    print("Invalid API keys.")
    quit()
if (manualBTC <= 0):
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
print("Investing amount: {} BTC".format(BTCtoSell));
tradingPair = input("Coin pair: ").upper() + coinPair

# get trading pair price
try: 
    price = float(client.get_avg_price(symbol=tradingPair)['price'])
except BinanceAPIException as e:
    if e.code == -1121:
        print("Invalid trading pair given. Check your input is correct as well as config.json's 'tradingPair' value to correct error.")
    else:
        print("A BinanceAPI error has occured. Code = " + str(e.code))
        print(e.message + " Please use https://github.com/binance/binance-spot-api-docs/blob/master/errors.md to find greater details on error codes before raising an issue.")
    quit()
except Exception as d:
    print(d)
    print("An unknown error has occured.")
    quit()

# calculate amount of coin to buy
amountOfCoin = BTCtoSell / price

# ensure buy limit is setup correctly
if(getAveragePrice == "TRUE"):
    # find average price in last 2 mins
    agg_trades = client.aggregate_trade_iter(symbol=tradingPair, start_str=minutesAveragePrice + " minutes ago UTC")
    agg_trade_list = list(agg_trades)
    total = 0
    for trade in agg_trade_list:
        fvalue = float(trade['p'])
        total = total + fvalue
    averagePrice = total / len(agg_trade_list)  
else:
    averagePrice = price

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
    coinOrderInfo           = order["fills"][0]
    coinPriceBought         = float(coinOrderInfo['price'])
    coinOrderQty            = float(coinOrderInfo['qty'])
except BinanceAPIException as e:
    print("A BinanceAPI error has occured. Code = " + str(e.code))
    print(e.message + " Please use https://github.com/binance/binance-spot-api-docs/blob/master/errors.md to find greater details on error codes before raising an issue.")
    quit()
except Exception as d:
    print(d)
    print("An unknown error has occured.")
    quit()

print('Processing sell order.')


# rounding sell price to correct dp
priceToSell = coinPriceBought * profitMargin
roundedPriceToSell = float_to_string(priceToSell, int(- math.log10(minPrice)))

# waits until the buy order has been confirmed 
orders = client.get_open_orders(symbol=tradingPair)
while (client.get_open_orders(symbol=tradingPair) != []):
    print("Waiting for coin to buy...")

try:
    # oco order (with stop loss)
    order = client.create_oco_order(
        symbol=tradingPair,
        quantity=coinOrderQty,
        side = SIDE_SELL,
        price = roundedPriceToSell,
        stopPrice = float_to_string(stopLoss * coinPriceBought, int(- math.log10(minPrice))),
        stopLimitPrice = float_to_string(stopLoss * coinPriceBought, int(- math.log10(minPrice))),
        stopLimitTimeInForce = TIME_IN_FORCE_GTC
        )
except BinanceAPIException as e:
    print("A BinanceAPI error has occured. Code = " + str(e.code))
    print(e.message + " Please use https://binance-docs.github.io/apidocs/spot/en/#error-codes to find greater details on error codes before raising an issue.")
    quit()
except Exception as d:
    print(d)
    print("An unknown error has occured.")
    quit()

print('Sell order has been made!')
# open binance page to trading pair
webbrowser.open('https://www.binance.com/en/trade/' + tradingPair)
