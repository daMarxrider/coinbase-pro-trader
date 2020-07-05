
from Controller import market_controller as market
from Controller import wallet_controller as wallet

products = []


def setup():
    products = market.products
    while 1:
        try:
            for product in products:
                if product.rsi != 0:
                    x = 0
                    for order in wallet.wallets.orders:
                        #TODO check if last order was a buy or sell of same product and prevent duplicate orders
                        if order.quote_currency in product.id and order.base_currency in product.id:
                            if order.statius in ['pending', 'open']:
                                continue
                    if product.rsi < 33:                          
                        wallet.buy(product)
                    elif product.rsi > 66:  
                        wallet.sell(product)
        except Exception as e
            print('error during market placement')
            print(e)
