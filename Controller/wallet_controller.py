from Controller import client_controller

wallets = []


def init_wallets():
    global wallets, client
    client = client_controller.client
    wallets = client.get_accounts()
    return wallets
