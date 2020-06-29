import transaction


class Product():
    base_currency = None
    quote_currency = None
    rate = None
    orders = []
    amount = None

    def __init__(self, base_currency='', quote_currency='', rate=.0, orders=[], amount=.0):
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.rate = rate
        self.orders = orders
        self.amount = amount
