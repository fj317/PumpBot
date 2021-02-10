from binance.client import Client
from binance.enums import *
import matplotlib.pyplot as plt 
import numpy as np
import csv
import pandas as pd
import seaborn as sns
import datetime

#  getting recent trades
client = Client("wDPuqBa0zeqQRHE26takNQ5G9jLyyFkWxisrheBqmxHDhz4RPcNzR8bPLg4E4Gka", "NwUcys7q7NLPl1ISoIAB97wyAjGNOc2Kw3nJqRJ8BwzFO4ERAsCqdOnK1eDzaPQk")
agg_trades = client.aggregate_trade_iter(symbol='ETHBTC', start_str='15 seconds ago UTC')

# only extracting the date and price
trades = []
for t in agg_trades:
    t = [t['T'],t['p']]
    t[0] = datetime.datetime.utcfromtimestamp(round(t[0]/1000))
    split_t = str(t[0]).split(' ')
    t[0] = split_t[1]
    trades.append(t)


# creating a csv file with the  trades data
with open('recent_trades.csv', 'w',newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['time' , 'price'])
    for t in trades:
        filewriter.writerow(t)

#  plotting the csv matrices
df = pd.read_csv('recent_trades.csv')
sns.lineplot(x="time", y="price", data=df)

# chaning the graph window to full size
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())


plt.show()





