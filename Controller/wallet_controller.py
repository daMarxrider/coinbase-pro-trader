from Controller import client_controller
from Models.transaction import Transaction

wallets = []
orders = []
client = None


def get_wallets():
    global wallets, orders, client
    if client == None:
        client = client_controller.client
    wallets = client.get_accounts()
    orders = []
    for wallet in wallets:
        json_orders = client.get_account_holds(wallet['id'])
        for order in json_orders:
            amount = order['amount']
            order = client.get_order(order['ref'])
            base_currency = order['product_id'].split(
                '-')[1] if order['side'] == 'buy' else order['product_id'].split('-')[0]
            quote_currency = order['product_id'].split(
                '-')[0] if order['side'] == 'sell' else order['product_id'].split('-')[1]
            orders.append(Transaction(
                order['id'], base_currency, quote_currency, fee=order['fill_fees'], base_value=amount, quote_value=order['size'], rate=order['price']))
    return wallets, orders
