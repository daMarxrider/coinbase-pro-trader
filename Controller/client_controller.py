import sys
import cbpro
client = None


def setup_client(config):
    global client
    client = cbpro.AuthenticatedClient(config['system']['api_key'], config['system']
                                       ['secret_key'], config['system']['passphrase'], api_url=config['system']['uri'])
    return client
