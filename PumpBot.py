from binance.client import Client
import math
import time
from datetime import datetime
import decimal

def float_to_string(number, precision=10):
    return '{0:.{prec}f}'.format(
        number, prec=precision,
    ).rstrip('0').rstrip('.') or '0'

# api keys
apiKey = ''
apiSecret = ''
# max amount for buy limit to pay
buyLimit = 1.15
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
amountOfCoin = float_to_string(amountOfCoin, int(- math.log10(minQty)))



# find average price in last 30 mins
agg_trades = client.aggregate_trade_iter(symbol=tradingPair, start_str='30 minutes ago UTC')
agg_trade_list = list(agg_trades)
total = 0
for trade in agg_trade_list:
    fvalue = float(trade['p'])
    total = total + fvalue
averagePrice = total / len(agg_trade_list)
minPrice = minQty = float(info['filters'][0]['minPrice'])
averagePrice = float_to_string(averagePrice, int(- math.log10(minPrice)))
averagePrice = averagePrice * buyLimit

# # buy order
order = client.order_limit_buy(
    symbol=tradingPair, 
    quantity=amountOfCoin,
    price=averagePrice)
print('Order has been bought!')
coinOrderInfo           = order["fills"][0]
coinPriceBought         = float(coinOrderInfo['price'])
coinOrderQty            = float(coinOrderInfo['qty'])

# rounding sell price to correct dp
priceToSell = coinPriceBought * profitMargin
#roundedPriceToSell = float_to_string(priceToSell)
roundedPriceToSell = float_to_string(priceToSell, int(- math.log10(minPrice)))

# sell order
order = client.order_limit_sell(
    symbol=tradingPair,
    quantity=coinOrderQty,
    price=roundedPriceToSell)
print('Sell order has been made!')
coinPriceBought = float_to_string(coinPriceBought, int(- math.log10(minPrice)))
print('\nOrder bought at: {}\nSell order made at: {}'.format(coinPriceBought, roundedPriceToSell))



