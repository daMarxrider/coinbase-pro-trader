# coinbase-pro-trader WIP
see TODOs in code for more information.
Also could use more algorithms and a importance for every algorithm if multiple are used at the same time.
## Important TODOs:
* add multiple Trading Platforms(e.g. Binance)
* prevent purchase of recently added products, that look like they are going to crash hard.
    * predicted problem: not enough data => look for data on other sources

## Why this bot
most other open-source bots can only trade one product(e.g. BTC-EUR, ETRH-EUR) at a time.
This sucks ass and thus I made a bot that can trade every tradable product at the same time.

## Requirements
* Python Version>=python3.8
* coinbase-pro/sandbox api-key
* pip modules, for more information run main.py and read the error messages

## Start-params
param | value
------------ | -------------
-s --system | system in your conf.yaml to use
-m --max_value | max value per trade


## Disclaimer
Insert copy-paste Disclaimer for "use at your own risk, I´m not responsible for any loses, you´re at your own bitch"

## additional Information
* feel free to make Pull-Requests or provide ideas for Algorithms/Trading-Strategies
* uses of try-except instead of if-else to handle exceptional cases.(see python optimizations)
* code displays various levels of salt
* objects are often retrieved by reference, to ensure processing of live-data
* if someone knows how to get rid of the error, that shitty GUIs get,when importing modules in another Directory 
    WITHOUT inserting the path manually(that solution sucks, just because it´s generally accepted, doesn´t mean it´s good)
    please make a PR.
    * btw, python doesn't care about the above mentioned error,thus the term "shitty GUIs"
