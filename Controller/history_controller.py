from Controller import client_controller
from Controller import market_controller as market
from Models.product import Product
from datetime import datetime as fucking_date
import datetime
import time
import statistics
import sys
import pandas as pd
# from tapy import Indicators
from ta import add_all_ta_features
from ta.utils import dropna
from ta.momentum import rsi

product_history = []

# TODO
product_current_data = []
product_complete_data = []

client = None
def calculate_rsi(product,**kwargs):
    shortened_mfi = []
    better_start_date = fucking_date.now() - datetime.timedelta(days:=14)
    better_end_date = fucking_date.now()
    shortened_mfi = client.get_product_historic_rates(
        product.id, start=better_start_date, end=better_end_date, granularity=86400)
    shortened_mfi.reverse()
    time.sleep(1)
    shortened_better_data = {
        'Open': [x[3] for x in shortened_mfi],
        'High': [x[2] for x in shortened_mfi],
        'Low': [x[1] for x in shortened_mfi],
        'Close': [x[4] for x in shortened_mfi],
        'Volume': [x[5] for x in shortened_mfi]
    }

    shortened_df = pd.notna(pd.DataFrame(
        [x[1:] for x in shortened_mfi], columns=['Open', 'High', 'Low', 'Close', 'Volume']))

    shortened_rsi_value = \
        rsi(pd.Series(data=[x[4] for x in shortened_mfi]), n=len(shortened_mfi)).values[-1]
    product.rsi = shortened_rsi_value


def get_history(f=calculate_rsi,**kwargs):
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
                    #Duck Typing + betterPerformance than if, i know, but python optimizes exception as if it´s life depended on it
                    # ^ encouraged by python
                    try:
                        f(product=product,**kwargs)
                    except Exception as e:
                        [fnctn(product=product,**kwargs) for fnctn in f]
                    finally:
                        product.is_analyzed=True
                    if kwargs.get('start_early'):
                        time.sleep(1)
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
            time.sleep(1)
        print('history')
        print([x['id']+'{}, newest timestamp {}\n'.format(len(x['data']),fucking_date.fromtimestamp(x['data'][-1][0])) for x in product_history])
        print('rsi values')
        print(['{}:{}'.format(x.id,x.rsi) for x in market.products if x.rsi!=0])
        print('euro_rates')
        print(['{}:{}'.format(x.id,x.euro_rate) for x in market.products if x.euro_rate!=1])
        # print(product_history)
        # time.sleep(10)


