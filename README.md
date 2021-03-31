![PumpBot Logo](https://github.com/fj317/PumpBot/blob/master/resources/logo.jpg)
 A bot to use in a pump & dump event on Binance.com. 
 
 **Please note the bot is in heavy devleopment currently so be aware of errors. If you experience errors please check the issue tab to see whether it has been documented already. If not, open an issue and give as much detail to the error as you can!**
  
 ### Features
 - Speedy. 
   - Can create buy and sell orders within a second of entering the coin pair.
 - Stop loss feature. 
   - Means you can set a stop loss sell order to ensure you won't lose too much in case coin never reaches your profit goal.
 - Average price checker. 
   - Bot checks last 24 hours average price of coin and creates a buy order at a maximum pre-defined value. This means you won't be buying coins at huge markups from people pre-pumping.
 - Simple to use.
   - Easy to setup with a customisable config file.
 - Free
   - Its not costing you $300 like some other bots out there.
 - Regular updates with good support. 
    
### Quick Setup
 1. Ensure you have the most recent of [Python](https://www.python.org/downloads/) installed, as well as [sammchardy's Python Binance API](https://github.com/sammchardy/python-binance).
 2. Download the [bot](https://github.com/fj317/PumpBot/archive/master.zip).
 3. Enter customisable data in config.json (see below for further details)
 4. Run python file on the terminal with the command 'python3 PumpBot.py' prior to event
 5. Enter coin into the bot once it has been given
 6. Let bot setup buy order and sell order 
 7. Profit?

![Menu Screen](https://github.com/fj317/PumpBot/blob/master/resources/menuScreen.png)  
 
 ### Config.JSON
 Config.json allows the user to customise the bot to their liking. The parameters the user can change are as follows: 
  - **quotedCoin**: allow you to change the quoted coin (in case Bitcoin is not the pair used in the pump). Default value is BTC.
 - **buyLimit**: enter the price for the Limit Buy order you will pay in relation to the current price of the coin when it is entered into the program. Eg 1.2 means you are will pay 1.2x the price of the coin to secure it. Default value is 1.15.
   - If this value is set to 1, the bot will create a market order rather than limit order. Please ensure you are aware of the differences if you use a market order. 
 - **percentOfWallet**: determines what percentage of your wallet's BTC will be used. Default value is 50%.
 - **manualQuoted**: enter the exact amount of BTC you want use when placing buy order. If 0 then the percentOfWallet parameter will be used instead. Default value is 0.0.
 - **profitMargin**: determines what price the coin's sell order will be put at. Default value is 150 (a 50% increase)
 - **stopLoss**: sets a stop loss sell order at percentage of what you paid for the coin. Default value is 0.9 (i.e. coin will automatically sell at market price if value reaches 90% of what you orignally bought at).
 - **endpoint**: change what endpoint you will use to connect to Binance.com. Default value is 'default'. The possible values are:
   - default
   - api1
   - api2
   - api3
 
### Keys.json
 Keys.json is where you enter your Binance's API keys. These can be found on your [Binance profile](https://www.binance.com/en/support/articles/360002502072). These values are required for the bot to work so please do not forget to enter them. Please note, you will have to rename Keys.json.example to keys.json for the bot to correctly read your API keys.
 - **apiKey**: enter your own API key here.
 - **apiSecret**: enter your own secret API key here.

### Common Errors
- Timestamp for this request was 1000ms ahead of the server's time
  - This is an error with your PC rather than the program. See this [thread](https://github.com/yasinkuyu/binance-trader/issues/63#issuecomment-355857901) for help
- Insufficient balance
  - Ensure you have enough funds to pay for transaction fees (I'd recommend using BNB for the discount)
  - If using BNB, make sure to enable using BNB for the fees in your dashboard settings found [here](https://www.binance.com/en/my/dashboard)
- Invalid API keys
  - You have entered your API keys incorrectly in keys.json.
 
 
 ### Work in Progress Features
 - [ ] Add ability to override config.json data by entering arguments on the command line when starting program.
 - [ ] Pre-pump detection. This is a monumental feature so is not currently actively being worked on.
 - [ ] Improve profit strategies.
 - [ ] Real time price checker.
 - [ ] Sell 25% of coins bought at a time
 
 ### Contributing
 - Fork this Repo
 - Commit your changes (git commit -m 'Add some feature')
 - Push to the changes (git push)
 - Create a new Pull Request
 
Thank you for your contributions...
- @ezanchi
- Noa Sade

 ### Disclaimer
 Please remember do not invest with money that you cannot afford to lose. I am not responsible if you invest money using the bot and for some reason a bug or error occurs that causes you to lose the money. I'll repeat this - do not invest money you cannot afford to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS. **I'd recommend you to have some coding, Python and crypto-knowledge before using the bot.** The bot is currently still in development so expect bugs and errors.
 
 ### Copyright

PumpBot is licensed under the BSD 2-Clause License.

Copyright (c) 2021 Freddie Jonas & Ariel Katzir.
