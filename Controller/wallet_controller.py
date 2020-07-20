from Controller import client_controller
from Models.transaction import Transaction
from Controller import market_controller as market
from cbpro import AuthenticatedClient
import dateutil.parser
import datetime
import time

max_trading_value=None
wallets = []
orders = []
client = None

def hold(product):
    pass

def buy(product):
    execute_order("buy",product)

def sell(product):
    execute_order("sell",product)


def execute_order(type,product,funds=None):
    if not funds:
        funds = float([x for x in wallets if x['currency'] == product.id.split('-')[1]][0]['available'])
        if funds * product.euro_rate > max_trading_value:
            funds = max_trading_value / product.euro_rate
    if product.trading_disabled:
        return
    relevant_orders = [x for x in orders if x.product_id == product.id and x.type != 'fee']
    sorted(relevant_orders, key=lambda x: x.executed_at)
    if len(relevant_orders) > 0 and relevant_orders[0].type == type:  # TODO check if date is old enough to start new transaction ~7days
        return

    if funds > product.min_transaction_size:
        if product.limit_only:
            order = client.place_limit_order(product.id, type, product.rate, funds)
        else:
            order = client.place_market_order(product.id, type, size=funds)
        if 'message' not in order.keys():
            # product.own_transactions.append(Transaction(product.id, '', '', type=type))
            get_wallets()
            return order
        if order['message'].__contains__('too accurate'):
            decimals = len(order['message'].split('.')[-1])
            execute_order(type,product,funds=funds.__round__(decimals))
        else:
            x=0



def get_wallets():
    global wallets, orders, client
    if client == None:
        client = client_controller.client
    wallets = client.get_accounts()
    orders = []
    for wallet in wallets:
        json_orders = client.get_account_history(wallet['id'])
        for order in json_orders:
            #time.sleep(1)
            amount = order['amount']
            if order['type']=='fee':
                type='fee'
            elif order['type']=='match':
                if float(order['balance'])<0:
                    type='sell'
                else:
                    type='buy'
            elif order['type']=='transfer':
                continue
            order = client.get_order(order['details']['order_id'])
            base_currency = order['product_id'].split(
                '-')[1] if order['side'] == 'buy' else order['product_id'].split('-')[0]
            quote_currency = order['product_id'].split(
                '-')[1] if order['side'] == 'sell' else order['product_id'].split('-')[0]
            #TODO also add order to product.own_orders
            orders.append(Transaction(
                order['id'], base_currency, quote_currency,product_id=order['product_id'],
                fee=order['fill_fees'], base_value=amount,
                quote_value=order['size']if 'size' in dir(order) else '0',
                status=order['status'],type=type,
                executed_timestamp= dateutil.parser.isoparse(order['done_at'])))
    return wallets, orders
