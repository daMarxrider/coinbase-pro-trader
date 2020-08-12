# coinbase-pro-trader

## Why this bot
most other open-source bots can only trade one product(e.g. BTC-EUR, ETH-EUR) at a time.
This sucks ass and thus I made a bot that can trade every tradable product(coinbase pro only atm) at the same time.

## Requirements
* Python Version>=Python3.6
    * mostly tested with PyPy 7.3.1 (https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy use this to install numpy and pandas for PyPy or just use linux and install dependencies like you normally do)
* coinbase-pro(/sandbox) api-key
* pip modules, for more information run main.py and read the error messages

## Start-params
param | value
------------ | -------------
-s --system | system in your conf.yaml to use
-m --max_value | max value per trade
-a --algorithms | algorithms to use

## Disclaimer
Insert copy-paste Disclaimer for "use at your own risk, I´m not responsible for any loses, you´re at your own bitch"

## additional Information
* feel free to provide ideas for Algorithms/Trading-Strategies
* if you want to make PRs:
    * ##### start with RTFS 
* uses of try-except instead of if-else to handle exceptional cases.(python performance optimization is weird)
* code displays various levels of salt
* objects are nearly always retrieved by reference, to ensure processing of live-data

