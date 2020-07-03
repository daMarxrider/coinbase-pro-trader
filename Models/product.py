import Models.transaction
from Controller import *
import Controller.market_controller as market
import cbpro


class Product():
    id = None
    base_currency = None
    quote_currency = None
    rate = None
    historic_rates = []
    own_orders = []
    public_orders = []
    amount = None
    own_transactions = []
    public_transactions = []

    def __init__(self, id,
                 base_currency=None, quote_currency=None, own_orders=None, public_orders=None,
                 amount=None, own_transactions=None, public_transactions=[], historic_rates=[]):
        self.id = id
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.own_orders = own_orders
        self.public_orders = public_orders
        self.amount = amount
        self.public_transactions = public_transactions

    def calculate_rate(self):
        # TODO
        return self.rate
