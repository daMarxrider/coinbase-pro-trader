import sys


class Transaction:
    id = None
    base_currency = None
    quote_currency = None
    base_value = None
    quote_value = None
    fee = None
    rate = None

    def __init__(self, id, base_currency, quote_currency, **kwargs):
        pass
