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

# removing old csv file
try:
    os.remove("recent_trades.csv")
except:
    None

#  getting recent trades
client = Client("", "")
agg_trades = client.aggregate_trade_iter(symbol='ETHBTC', start_str='10 seconds ago UTC')

# extracting the date and price
###TODO
# UTC is %h%m%s which is too long of a string so numbers mixup with each other
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
    filewriter.writerow(['Time(UTC)' , 'Price(BTC)'])
    for t in trades:
        filewriter.writerow(t)

#  plotting the csv matrices
df = pd.read_csv('recent_trades.csv')
sns.lineplot(x="Time(UTC)", y="Price(BTC)", data=df, markers=True)

priceBought = 

# draw line
plt.axhline(y = priceBought , color = 'r')

# chaning the graph window to full size
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
# show plot
plt.show()





