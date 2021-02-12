# PumpBot
 A bot to use in a pump & dump event on Binance.com.
 
 Please remember do not invest with money that you cannot afford to lose. I am not responsible if you invest money using the bot and for some reason a bug or error occurs that causes you to lose the money. I'll repeat this - **do not invest money you cannot afford to lose**. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS. I'd recommend you to have some coding, Python and crypto-knowledge before using the bot.
 
 ### Features
 - Speedy. 
   - Can create buy and sell orders within a second of entering the coin pair.
 - Stop loss feature. 
   - Means you can set a stop loss sell order to ensure you won't lose too much in case coin never reaches your profit goal.
 - Average price checker. 
   - Bot checks 30 min average price of coin and creates a buy order at this maximum pre-defined value. This means you won't be buying coins at huge markups from people pre-pumping. NOTE: I would only recommend using this if you have fast internet as it must download all trades that have occured in the last 30 minutes. This means for highly traded coins it will be downloading a lot of data which slows down your order speed down. Set value to 0 in config to turn off feature.
 - Simple to use.
   - Easy to setup with a customisable config file.
 - Free
   - Its not costing you $300 like some other bots out there.
   
 ![Menu Screen](https://github.com/fj317/PumpBot/blob/master/resources/menuScreen.png)  
 
### Quick Setup
 1. Ensure you have the most recent of [Python](https://www.python.org/downloads/) installed, as well as [sammchardy's Python Binance API](https://github.com/sammchardy/python-binance).
 2. Download the [bot](https://github.com/fj317/PumpBot/archive/master.zip).
 3. Enter customisable data in config.json (see below for further details)
 4. Run python file *pumpbot.py* prior to event
 5. Enter coin into the bot once it has been given
 6. Let bot setup buy order and sell order 
 7. Profit?
 
 ### Config.JSON
 Config.json allows the user to customise the bot to their liking. The parameters the user can change are as follows:
 - **apiKey**: enter your own [API key](https://www.binance.com/en/support/articles/360002502072) here. This is a required value.
 - **apiSecret**: enter your own secret API key here. This is a required value.
 - **profitMargin**: determines what price the coin's sell order will be put at. Default value is 150 (a 50% increase)
 - **percentOfWallet**: determines what percentage of your wallet's BTC will be used. Default value is 50%.
 - **buyLimit**: enter what the maximum price above the average in the last 30 minutes you will be willing to pay. This is done to avoid coins that are pre-pumped (i.e. this avoids you buying the coin at a higher price and then being unable to sell). Set to 0 to disable feature. Default value is 1.15. 
 - **stopLoss**: sets a stop loss sell order at percentage of what you paid for the coin. Default value is 0.9 (i.e. coin will automatically sell at market price if value reaches 90% of what you orignally bought at).
 - **coinPair**: allow you to change the coin pairing (in case bitcoin is not the pair used in the pump). Default value is BTC.
 
 ### Possible Future Features
 - [ ] GUI which graphs the price of the selected coin pair in real time. 
 - [ ] Give user the ability to manually cash out the coin (would automatically setup sell order at current price).
 - [ ] Bot will check how much BNB your wallet contains, and if below a threshold amount with convert some BTC to BNB to pay for Binance's fees.
 - [x] Add safety net (stop loss) so that if coin price falls quickly you will not lose additional money.
 
 ### Copyright

PumpBot is licensed under the BSD 2-Clause License.

Copyright (c) 2021 Freddie Jonas & Ariel Katzir.
