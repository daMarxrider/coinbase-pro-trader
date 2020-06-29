from Controller import client_controller
from Controller import market_controller as market

product_history = {}


def get_history():
    # TODO https://docs.pro.coinbase.com/#get-historic-rates
    for product in market.products:
        print('wallet:')
        print(product)
