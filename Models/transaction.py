import sys


class Transaction:
    id = None
    base_currency = None
    quote_currency = None
    base_value = None
    quote_value = None
    fee = None
    rate = None

    def __init__(self, id, base_currency, quote_currency, fee=None, base_value=None, quote_value=None, rate=None):
        self.id = id
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.fee = fee
        self.base_value = base_value
        self.quote_value = quote_value
        self.rate = rate
