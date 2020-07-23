import Models.transaction
import cbpro
from pandas import DataFrame


class Product(object):
    id = None
    base_currency = None
    quote_currency = None
    base_min_size = None
    base_max_size = None
    quote_increment = None
    base_increment = None
    min_market_funds = None
    max_market_funds = None
    margin_enabled = None
    post_only = None
    limit_only = None
    cancel_only = None
    trading_disabled = None
    status = None

    rate = None
    historic_rates = []
    own_orders = []
    public_orders = []
    amount = None
    own_transactions = []
    public_transactions = []
    mfi = 0
    rsi = 0
    highest_mimicry = {}
    mimicries = []
    min_transaction_size = None
    is_analyzed = False
    best_route_to_euro = []
    euro_rate = 1
    euro_rsi = None
    calculated_indicators: DataFrame = None

    artificial = False

    def __init__(self, id=None, json=None, **kwargs):
        self.id = id
        if json != None:
            for key, val in json.items():
                setattr(self, key, val)
        if kwargs:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)
