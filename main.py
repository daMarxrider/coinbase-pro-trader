import cbpro
import os
import sys
import yaml
import _thread as thread
import time
import Controller.market_controller as market
from Controller import client_controller as cli
import Controller.wallet_controller as wallet
configuration = []


def configure():
    global configuration
    if len(sys.argv) == 1 or sys.argv[1] == '-p':
        systemname = 'https://api.pro.coinbase.com'
    else:
        systemname = 'https://api-public.sandbox.pro.coinbase.com'
    if os.path.exists(filename := ('{}{}{}'.format(os.getcwd(), os.sep, 'conf.yaml'))):
        configuration = yaml.load(open(filename, 'r'), Loader=yaml.FullLoader)
        print(configuration)
    if len(configuration) == 0 or len([x for x in configuration if x['system']['name'] == systemname]) == 0:
        system = {}
        system['system'] = {}
        system['system']['name'] = systemname
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
    wallet.init_wallets()
    # TODO start threads for controllers once created
    products = market.products
    thread.start_new_thread(market.get_products_feed, ())
   # for i in range(10):
   #     print('new values:')
   #     for product in products:
   #         if product.id == "ETH-EUR":
   #             print(product.rate)
   #     time.sleep(10)
    while 1:
        # threads keep running, but this prevents the script from closing without using a shitty framework
        time.sleep(3600)


if __name__ == '__main__':
    main()
