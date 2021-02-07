# PumpBot
 A bot to use in a pump & dump event on Binance.com.
 
### Quick Setup
 1. Ensure you have the most recent of [Python](https://www.python.org/downloads/) installed, as well as [sammchardy's Python Binance API](https://github.com/sammchardy/python-binance).
 2. Enter customisable data in config.json (see below for further details)
 3. Run python file *pumpbot.py* prior to event
 4. Enter coin into the bot once it has been given
 5. Let bot setup buy order and sell order 
 6. Profit?
 
 ### Config.JSON
 Config.json allows the user to customise the bot to their liking. The parameters the user can change are as follows:
 - **apiKey**: enter your own [API key](https://www.binance.com/en/support/articles/360002502072) here 
 - **apiSecret**: enter your own secret API key here
 - **buyLimit**: enter what the maximum price above the average in the last 30 minutes you will be willing to pay. This is done to avoid coins that are pre-pumped (i.e. this avoids you buying the coin at a higher price and then being unable to sell). Default value is 1.15.
 - **profitMargin**: determines what price the coin's sell order will be put at. Default value is 150 (a 50% increase)
 - **percentOfWallet**: determines what percentage of your wallet's BTC will be used. Default value is 50%.
 
 ### Possible Future Features
 - GUI which graphs the price of the selected coin pair in real time. 
 - Give user the ability to manually cash out the coin (would automatically setup sell order at current price).
