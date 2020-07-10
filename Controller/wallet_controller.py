from Controller import client_controller
from Models.transaction import Transaction
from Controller import market_controller as market
from cbpro import AuthenticatedClient

max_trading_value=None
wallets = []
orders = []
client:  AuthenticatedClient= None

def buy(product):
    if product.id.__contains__('USD') or product.view_only:
        return
    for order in orders:
        if order.status=='open' and order.id==product.id:
            return
    if len([x for x in orders if x.product_id==product.id and x.type!='fee'])>0 and [x for x in orders if x.product_id==product.id and x.type!='fee'][0].type=='buy':
        return
    funds=float([x for x in wallets if x['currency']==product.id.split('-')[1]][0]['available'])
    if funds*product.euro_rate>max_trading_value:
        funds=max_trading_value/product.euro_rate
    if funds!=0 and (product.min_transaction_size is None or product.min_transaction_size<funds):
        order=client.place_market_order(product.id,'buy',size=funds)
        if 'message' not in order.keys():
            product.own_transactions.append(Transaction(product.id,'','',type='buy'))
            get_wallets()
            return order
        if order['message'].__contains__('too accurate'):
            decimals=len(order['message'].split('.')[-1])
            order=client.place_market_order(product.id,'buy',size=funds.__round__(decimals))
        # order=client.place_market_order(product.id,'buy',size=float(funds).__round__(5))
        try:
            if order['message'].__contains__('funds is too small. Minimum size is 10.00000000') or order['message'].__contains__('Trading pair not available'):
                product.view_only=True
            if order['message'].__contains__('too small'):
                product.min_transaction_size=float(order['message'].split(' ')[-1])
                x=0
            if order['message']=='Limit only mode':
                order=client.place_limit_order(product.id,'buy',product.rate,funds)
                if order['message'].__contains__('too small'):
                    product.min_transaction_size = float(order['message'].split(' ')[-1])
                else:
                    x=0
            else:
                x=0
        except:
            product.own_transactions.append(Transaction(product.id,'','',type='buy'))
            get_wallets()

def sell(product):
    if product.id.__contains__('USD') or product.view_only:
        return
    for order in orders:
        if order.status=='open' and order.id==product.id:
            return
    if len([x for x in orders if x.product_id==product.id and x.type!='fee'])>0 and [x for x in orders if x.product_id==product.id and x.type!='fee'][0].type=='sell':
        return
    funds=float([x for x in wallets if x['currency']==product.id.split('-')[0]][0]['available'])
    if funds*product.euro_rate>max_trading_value:
        funds=max_trading_value/product.euro_rate
    if funds!=0 and (product.min_transaction_size is None or product.min_transaction_size<funds):
        order=client.place_market_order(product.id,'sell',size=funds)
        if 'message' not in order.keys():
            product.own_transactions.append(Transaction(product.id,'','',type='buy'))
            get_wallets()
            return order
        if order['message'].__contains__('too accurate'):
            decimals=len(order['message'].split('.')[-1])
            order=client.place_market_order(product.id,'sell',size=funds.__round__(decimals))
        # order=client.place_market_order(product.id,'sell',size=float(funds).__round__(5))
        try:
            if order['message'].__contains__('funds is too small. Minimum size is 10.00000000') or order['message'].__contains__('Trading pair not available'):
                product.view_only=True
            if order['message'].__contains__('too small'):
                product.min_transaction_size=float(order['message'].split(' ')[-1])
                x=0
            if order['message']=='Limit only mode':
                order=client.place_limit_order(product.id,'sell',product.rate,funds)
                if order['message'].__contains__('too small'):
                    product.min_transaction_size = float(order['message'].split(' ')[-1])
                else:
                    x=0
                x=0
            else:
                x=0
        except:
            product.own_transactions.append(Transaction(product.id,'','',type='sell'))
            get_wallets()


def get_wallets():
    global wallets, orders, client
    if client == None:
        client = client_controller.client
    wallets = client.get_accounts()
    orders = []
    for wallet in wallets:
        json_orders = client.get_account_history(wallet['id'])
        for order in json_orders:
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
            orders.append(Transaction(
                order['id'], base_currency, quote_currency,product_id=order['product_id'], fee=order['fill_fees'], base_value=amount, quote_value=order['size']if 'size' in dir(order) else '0', status=order['status'],type=type))
    return wallets, orders
