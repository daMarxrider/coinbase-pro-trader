import cbpro
import os
import sys
import yaml
configuration = []


def configure():
    global configuration
    systemname = 'https://api.pro.coinbase.com' if sys.argv[1] == '-p' else 'https://public.sandbox.pro.coinbase.com'
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


def main():
    configure()


#    client=cbpro.Auth
if __name__ == '__main__':
    main()
