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
    mfi = 0
    rsi=0
    highest_mimicry={}
    mimicries=[]
    view_only=False
    min_transaction_size=None
    is_analyzed=False
    best_route_to_euro=[]
    euro_rate=1

    def __init__(self, id,
                 base_currency=None, quote_currency=None, own_orders=None, public_orders=None,
                 amount=None, own_transactions=None, public_transactions=[], historic_rates=[], mfi=0,rsi=0,view_only=False,min_transaction_size=0):
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
        self.view_only=view_only
        self.min_transaction_size=float(min_transaction_size)
        self.is_analyzed=False
        self.best_route_to_euro=[]
        self.euro_rate=1


    def get_best_route_to_euro(self):
        routes=[]
        if self.id.__contains__('EUR'):
            self.best_route_to_euro.append(self.id)
            self.euro_rate=self.rate
            return
        for product in market.products:
            try:
                if product.euro_rate!=1 and len(route_start:=[x for x in product.best_route_to_euro if x.split('-')[0]==self.quote_currency]):
                    calc_rate=float(self.rate)
                    route_list=product.best_route_to_euro[product.best_route_to_euro.index(route_start[0]):]
                    #TODO dont iterate if direct conversion to euro is possible
                    for p_temp in market.products:
                        if p_temp.id in route_list:#TODO fix stablecoin duplication in list error. See above comment
                            calc_rate*=float(p_temp.rate)*0.995
                    routes.append({'route':[self.id]+route_list,'rate':calc_rate})
            except:
                pass
        try:
            routes.sort(key=lambda x: x['rate'],reverse=True)
            self.best_route_to_euro=routes[0]['route']
            self.euro_rate=routes[0]['rate']
            return self.best_route_to_euro,self.euro_rate
        except:
            #no route found
            pass