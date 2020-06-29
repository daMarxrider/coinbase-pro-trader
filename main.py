import cbpro
import os
import sys
import yaml
import Controller.market_controller as market
configuration = []


def configure():
    global configuration
    if len(sys.argv) == 1 or sys.argv[1] == '-p':
        systemname = 'https://api.pro.coinbase.com'
    else:
        systemname = 'https://api-public.sandbox.pro.coinbase.com'
    if os.path.exists(filename := ('{}{}{}'.format(os.getcwd(), os.sep, 'conf.yaml'))):
        configuration = yaml.load(open(filename, 'r'))
    if len(configuration) == 0 or len([x['data']['name'] == systemname for x in configuration]):
        system = {}
        system['data'] = {}
        system['data']['name'] = systemname
        system['data']['api_key'] = input('api_key:')
        system['data']['secret_key'] = input('secret_key:')
        system['data']['passphrase'] = input('passphrase:')
        configuration.append(system)
        yaml.dump(configuration, open(filename, 'w'))
    else:
        system = [x['data']['name'] == systemname for x in configuration][0]
    configuration = system


def main():
    configure()
    # TODO start threads for controllers once created
    market.get_products()


#    client=cbpro.Auth
if __name__ == '__main__':
    main()