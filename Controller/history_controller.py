from . import client_controller
from . import market_controller as market
from Models.product import Product
from datetime import datetime as fucking_date
import datetime
import time
import statistics
import sys
import os
import pandas as pd
#from tapy import Indicators
from ta import add_all_ta_features
from ta.utils import dropna
from ta.momentum import rsi



product_history = []

# TODO
product_current_data = []
product_complete_data = []

client = None

    #TODO get best algorithm for every product
    #TODO get indicators to euro with best_route_to_euro of product
def calculate_indicators(product, **kwargs):
    shortened_mfi = []
    #TODO change to 2 months and check if rsi was less than 30% above 50 in the last month, to identify sinking products
        #Addendum: maybe use less than 2 months, as Dataframe-Creation/Evaluation takes
        # approx. 6 sec and speed is key in trading
    #TODO add rsi_history to product class
    days = 14
    better_start_date = fucking_date.now() - datetime.timedelta(days)
    better_end_date = fucking_date.now()
    shortened_mfi = client.get_product_historic_rates(
        product.id, start=better_start_date, end=better_end_date, granularity=86400)
    shortened_mfi.reverse()
    # shortened_better_data = {
    #     'Open': [x[3] for x in shortened_mfi],
    #     'High': [x[2] for x in shortened_mfi],
    #     'Low': [x[1] for x in shortened_mfi],
    #     'Close': [x[4] for x in shortened_mfi],
    #     'Volume': [x[5] for x in shortened_mfi]
    # }

    # shortened_df = pd.notna(pd.DataFrame(
    #     [x[1:] for x in shortened_mfi], columns=['Open', 'High', 'Low', 'Close', 'Volume']))
    #
    # shortened_rsi_value = \
    #     rsi(pd.Series(data=[x[4] for x in shortened_mfi]), n=14).values[-1]
    newer_rsi_value = \
        rsi(pd.Series(data=[x[4] for x in shortened_mfi][:-1:]+[product.rate]), n=14).values[-1]
    product.rsi = newer_rsi_value

#TODO see implementation of ta-library, extra parameter fillna might be more performant/give better results than manually dropping null values
    # complete_data = pd.DataFrame(shortened_better_data, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    # all_indicators=add_all_ta_features(complete_data,open="Open",high="High",low="Low",close="Close",volume="Volume",fillna=True)
    # product.calculated_indicators=all_indicators



def get_history(f=calculate_indicators, **kwargs):
    global client, product_history, product_current_data, product_complete_data
    # from docs
    # [ time, low, high, open, close, volume  ],
    # [ 1415398768, 0.32, 4.2, 0.35, 4.2, 12.3  ],
    while 1:
        if client == None:
            client = client_controller.client
        for product in market.products:
            if len(product_history) > 0:
                p_history = [
                    x for x in product_history if x['id'] == product.id]
            else:
                p_history = []
            try:
                start_date = fucking_date.now() - \
                    datetime.timedelta(336) if len(
                        p_history) == 0 else fucking_date.fromtimestamp(p_history[0]['data'][-1][0])
                end_date = start_date+datetime.timedelta(0, 21600*100)
                #calculate statistics for wanted data
                if start_date > fucking_date.now()-datetime.timedelta(1) or end_date > fucking_date.now()-datetime.timedelta(1) or kwargs.get('start_early'):
                    try:
                        f(product=product,**kwargs)
                    except Exception as e:
                        [fnctn(product=product,**kwargs) for fnctn in f]
                    finally:
                        product.is_analyzed=True
                    if kwargs.get('start_early'):
                        pass
                    else:
                        continue

                data = client.get_product_historic_rates(
                    product.id, start=start_date, end=end_date, granularity=21600)

                if len(p_history) == 0 and len(data) > 1:
                    data.reverse()
                    p_history = {'id': product.id, 'data': data}
                    product_history.append(p_history)
                elif len(data) > 1:
                    data.reverse()
                    p_history[0]['data'].extend(data)
            except Exception as e:
                pass
            try:
                product.historic_rates = p_history[0]['data']
            except Exception as e:
                try:
                    product.historic_rates = p_history['data']
                except Exception as e:
                    pass
            #time.sleep(1)
        print('history')
        print([x['id']+'{}, newest timestamp {}\n'.format(len(x['data']),fucking_date.fromtimestamp(x['data'][-1][0])) for x in product_history])
        print('rsi values')
        #Note:
        #sorted doesn´t change the original list
        rsi_sorted=sorted(market.products,key=lambda x : x.rsi)
        print([f'{x.id}:{x.rsi:.{2}f}'.format(x.id,x.rsi) for x in rsi_sorted if x.rsi!=0])
        print('euro_rates')
        print(['{}:{}'.format(x.id,x.euro_rate) for x in market.products if x.euro_rate!=1])
        # print(product_history)
        # #time.sleep(10)


