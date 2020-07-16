import sys


class Transaction:
    id = None
    product_id=None
    base_currency = None
    quote_currency = None
    base_value = None
    quote_value = None
    fee = None
    rate = None
    status=None
    type=None
    executed_timestamp=None

    def __init__(self, id, base_currency, quote_currency,product_id=None, fee=None, base_value=None, quote_value=None, rate=None,status=None,type=None,executed_timestamp=None):
        self.id = id
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.product_id=product_id
        self.fee = fee
        self.base_value = base_value
        self.quote_value = quote_value
        self.rate = rate
        self.status=status
        self.type=type
        self.executed_timestamp=executed_timestamp
