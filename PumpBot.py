from binance.client import Client
import math
import time
from datetime import datetime
import decimal

def rounding(calcResult, minParam):
    calcResult = calcResult / minParam
    if isinstance(calcResult, int) == False:
        calcResult = round(calcResult) 
    return calcResult * minParam

def float_to_string(number, precision=10):
    return '{0:.{prec}f}'.format(
        number, prec=precision,
    ).rstrip('0').rstrip('.') or '0'

#ari keys
apiKey = ''
apiSecret = ''
client = Client(apiKey, apiSecret)
profitMargin = float(input("Profit(%): ")) / 100
percentOfWallet = float(input("Percent of wallet(%): ")) / 100
# find amount of bitcoin to use
BTCBalance = float(client.get_asset_balance(asset='BTC')['free'])
BTCtoSell = BTCBalance * percentOfWallet
# wait until coin input
tradingPair = input("Coin: ").upper() + 'BTC'

price = float(client.get_avg_price(symbol=tradingPair)['price'])
amountOfCoin = BTCtoSell / price;

# rounding the coin to the specified lot size
info = client.get_symbol_info(tradingPair)
minQty = float(info['filters'][2]['minQty'])
amountOfCoin = rounding(amountOfCoin, minQty)

# buy order
order = client.create_order(
    symbol=tradingPair, 
    side=SIDE_BUY, 
    type=ORDER_TYPE_MARKET, 
    quantity=amountOfCoin)
print('Order has been bought!')
coinOrderInfo           = order["fills"][0]
coinPriceBought         = float(coinOrderInfo['price'])
coinOrderQty            = float(coinOrderInfo['qty'])

# rounding sell price to correct dp
minPrice = float(info['filters'][0]['minPrice'])
priceToSell = coinPriceBought * profitMargin
roundedPriceToSell = float_to_string(priceToSell)

# sell order
order = client.order_limit_sell(
    symbol=tradingPair,
    quantity=coinOrderQty,
    price=roundedPriceToSell)
print('Sell order has been made!')
print('\nOrder bought at: {}\nSell order made at: {}'.format('{0:.8f}'.format(coinPriceBought), roundedPriceToSell))



