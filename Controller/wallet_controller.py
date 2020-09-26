import datetime
import dateutil.parser
from Models.transaction import Transaction
from Controller import client_controller
import sys
import math
from cbpro import AuthenticatedClient
sys.path

max_trading_value = None
wallets = []
orders = []
client: AuthenticatedClient = None


def hold(product):
    pass


def buy(product):
    execute_order("buy", product)


def sell(product):
    execute_order("sell", product)


def execute_order(type, product, funds=None):
    try:
        if product.trading_disabled:
            return
        if not funds:
            funds, wallet = set_funds(type, product)
            if funds is None:
                return
        json_orders = client.get_account_history(wallet['id'])
        relevant_orders = [
            x for x in json_orders if 'product_id' in x['details'] and x['details']['product_id'] == product.id and x['type'] != 'fee'
        ]
        sorted(relevant_orders, key=lambda x: x['created_at'])
        if len(relevant_orders) > 0 and (type == 'buy' and float(relevant_orders[0]['amount']) > 0
                                         or type == 'sell' and float(relevant_orders[0]['amount']) < 0)\
                                    and datetime.datetime.strptime(relevant_orders[0]['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")\
                                        > (datetime.datetime.now() - datetime.timedelta(7)):
            return

        if not product.min_transaction_size or funds > product.min_transaction_size:
            if product.limit_only:
                order = client.place_limit_order(product.id, type, product.rate, size=funds)
            else:
                order = client.place_market_order(product.id, type, size=funds)
            if 'message' not in order.keys():
                # product.own_transactions.append(Transaction(product.id, '', '', type=type))
                get_wallets()
                return order
            if order['message'].__contains__('too accurate'):
                decimals = len(order['message'].rstrip('0').split('.')[-1])
                funds = funds * 0.99
                funds = math.floor(funds * float(10**decimals)) / float(10**decimals)
                execute_order(type, product, funds=funds.__round__(decimals))
            else:
                pass

    except Exception:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        print(exc_obj)
        print(lineno)
        print(filename)


def set_funds(type, product):
    try:
        if type == 'buy':
            index = 1
        elif type == "sell":
            index = 0
        for wallet in wallets:
            if wallet['currency'] == product.id.split('-')[index]:
                break
        funds = float(wallet['available'])
        min_funds = ['base_min_size', 'min_market_funds']
        # TODO figure correct attributes out
        if funds < float(getattr(product, min_funds[index])):
            return None, wallet
    except Exception:
        funds = float(product.base_min_size)
    if funds * product.euro_rate > max_trading_value:
        funds = max_trading_value / product.euro_rate
    return funds, wallet


def get_wallets():
    global wallets, orders, client
    if client is None:
        client = client_controller.client
    wallets = client.get_accounts()
    orders = []
    for wallet in wallets:
        json_orders = client.get_account_history(wallet['id'])
        for order in json_orders:
            # time.sleep(1)
            amount = order['amount']
            if order['type'] == 'fee':
                type = 'fee'
            elif order['type'] == 'match':
                if float(order['balance']) < 0:
                    type = 'sell'
                else:
                    type = 'buy'
            elif order['type'] == 'transfer':
                continue
            order = client.get_order(order['details']['order_id'])
            base_currency = order['product_id'].split('-')[1] if order['side'] == 'buy' else order['product_id'].split('-')[0]
            quote_currency = order['product_id'].split('-')[1] if order['side'] == 'sell' else order['product_id'].split('-')[0]
            # TODO also add order to product.own_orders
            orders.append(
                Transaction(order['id'],
                            base_currency,
                            quote_currency,
                            product_id=order['product_id'],
                            fee=order['fill_fees'],
                            base_value=amount,
                            quote_value=order['size'] if 'size' in dir(order) else '0',
                            status=order['status'],
                            type=type,
                            executed_timestamp=dateutil.parser.isoparse(order['done_at'])))
    return wallets, orders
