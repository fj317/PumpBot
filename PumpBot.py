from binance.client import Client
import math
import json

def float_to_string(number, precision=10):
    return '{0:.{prec}f}'.format(
        number, prec=precision,
    ).rstrip('0').rstrip('.') or '0'

# read json file
f = open('config.json',)
data = json.load(f)
apiKey = data['apiKey']
apiSecret = data['apiSecret']
profitMargin = data['profitMargin']
percentOfWallet = data['percentOfWallet']
buyLimit = data['buyLimit']
client = Client(apiKey, apiSecret)

# find amount of bitcoin to use
BTCBalance = float(client.get_asset_balance(asset='BTC')['free'])
BTCtoSell = BTCBalance * percentOfWallet
# wait until coin input
tradingPair = input("Coin: ").upper() + 'BTC'

# get trading pair price
price = float(client.get_avg_price(symbol=tradingPair)['price'])
# calculate amount of coin to buy
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
averagePrice = float(averagePrice) * buyLimit
# buy order
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

# waits until the buy order has been confirmed 
orders = client.get_open_orders(symbol=tradingPair)
while (client.get_open_orders(symbol=tradingPair) != []):
    print("Waiting for coin to buy...")

# sell order
order = client.order_limit_sell(
    symbol=tradingPair,
    quantity=coinOrderQty,
    price=roundedPriceToSell)
print('Sell order has been made!')
coinPriceBought = float_to_string(coinPriceBought, int(- math.log10(minPrice)))
print('\nOrder bought at: {}\nSell order made at: {}'.format(coinPriceBought, roundedPriceToSell))



