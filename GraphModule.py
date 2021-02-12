# fix errors
# sometimes price axis changes units change - probably because dp too large for units
from binance.client import Client
from binance.enums import *
import matplotlib.pyplot as plt 
import numpy as np
import csv
import pandas as pd
import seaborn as sns
import datetime
import os
import math

# Removing old csv file if there is one
try:
    os.remove("recent_trades.csv")
except:
    None

#  Getting recent trades
client = Client("", "")
agg_trades = client.aggregate_trade_iter(symbol='ETHBTC', start_str='10 seconds ago UTC')

# extracting the date and price
###TODO
# 1. UTC is %h%m%s which is too long of a string so numbers sometimes mixup with each other.
# 2. There can be multiple trades every second, graph only uses the last trade made in each second - make average.
trades = []
for t in agg_trades:
    # Converting price from BTC to Satoshi
    t = [t['T'],(float(t['p'])*100000000)] 
    # Converting Unix timestamp to UTC and disregarding date data
    t[0] = datetime.datetime.utcfromtimestamp(round(t[0]/1000))
    split_t = str(t[0]).split(' ')
    t[0] = split_t[1]
    
    trades.append(t)

print(trades)

# Creating a csv file with the trades data
with open('recent_trades.csv', 'w',newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Time(UTC)' , 'Price(Satoshi)'])
    for t in trades:
        filewriter.writerow(t)

# Plotting the csv matrices with Seaborn library
df = pd.read_csv('recent_trades.csv')
sns.lineplot(x="Time(UTC)", y="Price(Satoshi)", data=df, markers=True)

# Takes the price bought and draws red line y = p where p is the price bought

# priceBought = ***price***
# plt.axhline(y = priceBought , color = 'r')

# Chaning the graph window to full size
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

# Show plot (opens a new window)
plt.show()





