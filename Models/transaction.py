class Transaction:
    base_currency=None
    quote_currency=None
    base_value=None
    quote_value=None
    fee=None
    rate=None
    def __init__(self,base_currency,quote_currency,base_value,quote_value=.0,fee=.0,rate=.0):
