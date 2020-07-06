
from Controller import market_controller as market
from Controller import wallet_controller as wallet

products = []


def setup(plugins=[]):
    products = market.products
    while 1:
        try:
            for product in products:
                if product.rsi != 0:
                    x = 0
                    for order in wallet.orders:
                        # TODO check if last order was a buy or sell of same product and prevent duplicate orders
                        if order.quote_currency in product.id and order.base_currency in product.id:
                            if order.statius in ['pending', 'open']:
                                continue
                    if product.rsi < 33:
                        if len(product.own_transactions)>0 and product.own_transactions[-1].status=='buy':
                            continue
                        wallet.buy(product)
                    elif product.rsi > 66:
                        if len(product.own_transactions)>0 and product.own_transactions[-1].status=='sell':
                            continue
                        wallet.sell(product)
        except Exception as e:
            print('error during market placement')
            print(e)

