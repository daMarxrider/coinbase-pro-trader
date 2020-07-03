
from Controller import market_controller as market
from Controller import wallet_controller as wallet

products=[]

def setup():
    products=market.products
    while 1:
        try:
            for product in products:
                if product.rsi!=0:
                    x=0
                    # for order in wallet.wallets.orders:
                    #     if order.quote_currency in product.id and order.base_currency in product.id:
                    #         continue
                    if product.rsi<33:#TODO buy
                        wallet.buy(product)
                    elif product.rsi>66:#TODO sell
                        wallet.sell(product)
        except:
            pass