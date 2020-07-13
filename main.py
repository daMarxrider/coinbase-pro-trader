import cbpro
import os
import sys
import argparse
import yaml
import _thread as thread

import time
import re
# cli=__import__()
import importlib
# importlib.import_module('.rsi_based','Algorithms.Prediction')
from Controller import client_controller as cli
import Controller.market_controller as market
import Controller.wallet_controller as wallet
import Controller.history_controller as history

import re
# x=[]
# def find(name,path):
#     s=path
#     print(path)
#     for root, dirs, files in os.walk(path):
#         x.extend(files)
#         print(path)
#         print(files)
#         if any(name in file for file in files):
#             return os.path.join(root, name)

# Prediction_Algorithms=__import__('Algorithms.Prediction',globals(),locals(),['Basics'])
# Tading_Algorithms=__import__('Algorithms.Trading',globals(),locals(),['*'])
from Algorithms.Prediction import cross_market_evaluation as cross_market_evaluation
import Algorithms.Trading.rsi_based as rsi_based
from datetime import datetime as fucking_date
import datetime
parser=argparse.ArgumentParser()
parser.add_argument("--max_value","-m",type=float,help="set max trading value in euro")
parser.add_argument("--system","-s",help="the system-name from your yaml config that should be used")
parser.add_argument("--algorithms","-a",type=str,default=['rsi_based','cross_market_evaluation'], nargs='*',
                    help="algorithms to be used. Separated by ; .\n"
                         "default algorithms is rsi and cross_market_evaluation\n implemented algorithms: rsi")
args=parser.parse_args()
configuration = []
# xs=[]
# osy=[]
# for d,_,f in os.walk(sys.path[0]):
#     for file in f:
#         if file.__contains__('.py') and '__pycache__' not in d:
#             try:
#                 if any(a in file for a in args.algorithms):
#                     globals()[file[:-3]]=getattr(__import__(a:=(re.search(r'^.*?(Algorithms.*)',d).groups()[0].replace(os.sep,'.')),fromlist=[file[:-3]])[],file[:-3])
#             except:pass


def configure():
    global configuration
    wallet.max_trading_value=float(args.max_value)
    if len(sys.argv) == 1:
        systemname = 'prod'
        systemuri = 'https://api.pro.coinbase.com'
    else:
        systemname = args.system
        systemuri = 'https://api-public.sandbox.pro.coinbase.com'
    filename = ('{}{}{}'.format(sys.path[0], os.sep, 'conf.yaml'))
    if os.path.exists(filename):
        configuration = yaml.load(open(filename, 'r'), Loader=yaml.FullLoader)
        print(configuration)
    if len(configuration) == 0 or len([x for x in configuration if x['system']['name'] == systemname]) == 0:
        system = {}
        system['system'] = {}
        system['system']['name'] = systemname
        system['system']['uri'] = systemuri
        system['system']['api_key'] = input('api_key:')
        system['system']['secret_key'] = input('secret_key:')
        system['system']['passphrase'] = input('passphrase:')
        configuration.append(system)
        yaml.dump(configuration, open(filename, 'w'))
    else:
        system = [x for x in configuration if x['system']
                  ['name'] == systemname][0]
    configuration = system
    cli.setup_client(configuration)


def main():
    configure()
    wallet.get_wallets()
    for w in wallet.wallets:
        print(w)
    products = market.products
    thread.start_new_thread(market.get_products_feed, ())

    # #TODO require user input for funtion(s)
    # algoritms_to_use=[]
    # for algo in args.algorithms:
    #     algoritms_to_use.append(__import__('Algorithms', globals(), locals(), fromlist=[algo]))

    thread.start_new_thread(history.get_history, ([history.calculate_indicators],), {'start_early':True})
    thread.start_new_thread(cross_market_evaluation.setup, ())
    thread.start_new_thread(rsi_based.setup, ())
    while 1:
        # threads keep running, but this prevents the script from closing without using a shitty framework
        time.sleep(3600)


if __name__ == '__main__':
    main()
