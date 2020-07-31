import os
import sys
import argparse
import yaml
import _thread as thread
import joblib
from joblib import delayed
import time


from Controller import client_controller as cli
import Controller.market_controller as market
import Controller.wallet_controller as wallet
import Controller.history_controller as history


import Algorithms.Prediction.cross_market_evaluation as cross_market_evaluation
import Algorithms.Trading.trade_all_indicators as trader


parser = argparse.ArgumentParser()
parser.add_argument("--max_value", "-m", type=float,
                    help="set max trading value in euro")
parser.add_argument(
    "--system", "-s", help="the system-name from your yaml config that should be used")
parser.add_argument("--algorithms", "-a", type=str, default=['rsi_based', 'cross_market_evaluation'], nargs='*',
                    help="algorithms to be used. Separated by ; .\n"
                         "default algorithms is rsi and cross_market_evaluation\n implemented algorithms: rsi")
args = parser.parse_args()
configuration = []


def configure():
    global configuration
    wallet.max_trading_value = float(args.max_value)
    if len(sys.argv) == 1:
        systemname = 'prod'
        systemuri = 'https://api.pro.coinbase.com'
    else:
        systemname = args.system
        systemuri = 'https://api-public.sandbox.pro.coinbase.com'
    filename = ('{}{}{}'.format(sys.path[0], os.sep, 'conf.yaml'))
    if os.path.exists(filename):
        configuration = yaml.load(open(filename, 'r'), Loader=yaml.Loader)
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
    global pr
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
    funcs = [{'function': history.get_history, 'params': (history.calculate_indicators), 'kwargs': {'start_early': True}},
             {'function': cross_market_evaluation.setup, 'params': (), 'kwargs': {}},
             {'function': trader.setup, 'params': (), 'kwargs': {}}]
    joblib.Parallel(n_jobs=len(funcs), require='sharedmem', pre_dispatch="all", verbose=100)(
        delayed(func['function'])(func['params'], **func['kwargs']) for func in funcs)
    while 1:
        time.sleep(3600)


if __name__ == '__main__':
    main()
