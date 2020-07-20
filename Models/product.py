import Models.transaction
import cbpro
from pandas import DataFrame


class Product(object):
    id = None
    base_currency = None
    quote_currency = None
    base_min_size=None
    base_max_size=None
    quote_increment=None
    base_increment=None
    min_market_funds=None
    max_market_funds=None
    margin_enabled=None
    post_only=None
    limit_only=None
    cancel_only=None
    trading_disabled=None
    status=None

    rate = None
    historic_rates = []
    own_orders = []
    public_orders = []
    amount = None
    own_transactions = []
    public_transactions = []
    mfi = 0
    rsi=0
    highest_mimicry={}
    mimicries=[]
    min_transaction_size=None
    is_analyzed=False
    best_route_to_euro=[]
    euro_rate=1
    euro_rsi=None
    calculated_indicators:DataFrame=None

    def __init__(self, id=None,
                 base_currency=None, quote_currency=None, own_orders=None, public_orders=None,
                 amount=None, own_transactions=None, public_transactions=[], historic_rates=[], mfi=0,rsi=0,min_transaction_size=0,
                 calculated_indicators:DataFrame=None,euro_rsi=None,
                 json=None):
        self.id = id
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.own_orders = own_orders
        self.public_orders = public_orders
        self.amount = amount
        self.public_transactions = public_transactions
        self.mfi = mfi
        self.rsi=rsi
        self.highest_mimicry={}
        self.mimicries=[]
        self.min_transaction_size=float(min_transaction_size)
        self.is_analyzed=False
        self.best_route_to_euro=[]
        self.euro_rate=1
        self.calculated_indicators=calculated_indicators
        self.euro_rsi=euro_rsi
        if json!=None:
            for key,val in json.items():
                setattr(self,key,val)

