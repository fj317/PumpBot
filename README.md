# PumpBot
 A bot to use in a pump & dump event on Binance.com.
 
 To run the bot:
 1. Enter customisable data in config.json (see below for further details)
 2. Run bot prior to event
 3. Enter coin into the bot once it has been given
 4. Let bot setup buy order and sell order 
 5. Profit?
 
 
 ### Config.JSON
 The file config.json is used to enter your own API key's so that the bot will be able to connect to your Binance account. Config.json also allows the user to customise the bot to their liking. The parameters the user can change are as follows:
 - **apiKey**: enter your own API key here
 - **apiSecret**: enter your own secret API key here
 - **buyLimit**: enter what the maximum price above the average in the last 30 minutes you will be willing to pay. This is done to avoid coins that are pre-pumped (i.e. this avoids you buying the coin at a higher price and then being unable to sell). Default value is 1.15.
 - **profitMargin**: determines what price the coin's sell order will be put at. Default value is 150 (a 50% increase)
 - **percentOfWallet**: determines what percentage of your wallet's BTC will be used. Default value is 50%.


Uses [sammchardy's Python Binance API](https://github.com/sammchardy/python-binance).
