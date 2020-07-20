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
import pymongo
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne, WriteConcern, MongoClient

product_history = []

# TODO
product_current_data = []
product_complete_data = []

client = client_controller.client


#TODO get best algorithm for every product
#TODO get indicators to euro with best_route_to_euro of product
def calculate_indicators(product, **kwargs):
    shortened_mfi = []
    #TODO change to 2 months and check if rsi was less than 30% above 50 in the last month, to identify sinking products
    #Addendum: maybe use less than 2 months, as Dataframe-Creation/Evaluation takes
    # approx. 6 sec and speed is key in trading
    #TODO add rsi_history to product class
    days = 60
    better_start_date = fucking_date.now() - datetime.timedelta(days)
    better_end_date = fucking_date.now()
    shortened_mfi = client.get_product_historic_rates(product.id,
                                                      start=better_start_date,
                                                      end=better_end_date,
                                                      granularity=86400)
    shortened_mfi.reverse()
    current_day_dataset = client.get_product_24hr_stats(product.id)
    shortened_mfi[-1] = [
        datetime.datetime.combine(datetime.datetime.today(),
                                  datetime.time()).timestamp(),
        float(current_day_dataset['low']),
        float(current_day_dataset['high']),
        float(current_day_dataset['open']),
        float(current_day_dataset['last']),
        float(current_day_dataset['volume'])
    ]
    shortened_better_data = {
        'Product': product.id,
        'Timestamp': [x[0] for x in shortened_mfi],
        'Open': [x[3] for x in shortened_mfi],
        'High': [x[2] for x in shortened_mfi],
        'Low': [x[1] for x in shortened_mfi],
        'Close': [x[4] for x in shortened_mfi],
        'Volume': [x[5] for x in shortened_mfi]
    }

    # shortened_df = pd.notna(pd.DataFrame(
    #     [x[1:] for x in shortened_mfi], columns=['Open', 'High', 'Low', 'Close', 'Volume']))
    #
    # shortened_rsi_value = \
    #     rsi(pd.Series(data=[x[4] for x in shortened_mfi]), n=14).values[-1]
    #
    # newer_rsi_value = \
    #     rsi(pd.Series(data=[x[4] for x in shortened_mfi][:-1:]+[product.rate]), n=14).values[-1]
    # product.rsi = newer_rsi_value

    #TODO see implementation of ta-library, extra parameter fillna might be more performant/give better results than manually dropping null values

    #IMPORTANT TODO CALCULATE DATA FOR EVERY POSSIBLE RELATION IN A 3DIMENSIONAL ARRAY7
    complete_data = pd.DataFrame(shortened_better_data,
                                 columns=[
                                     'Product', 'Timestamp', 'Open', 'High',
                                     'Low', 'Close', 'Volume'
                                 ])
    all_indicators = add_all_ta_features(complete_data,
                                         open="Open",
                                         high="High",
                                         low="Low",
                                         close="Close",
                                         volume="Volume",
                                         fillna=True)
    product.calculated_indicators = all_indicators
    product.rsi = all_indicators['momentum_rsi'].values[-1]

    mongo = MongoClient()
    # mongo.get_database('coinbase_history')
    db = mongo['coinbase_history']
    try:
        db.create_collection(
            "calculated_products", **{
                '_id': [("Product", pymongo.ASCENDING),
                        ('Timestamp', pymongo.ASCENDING)]
            })
    except:
        pass
    finally:
        db_coll = db["calculated_product"]
        db_coll.create_index([("Product", pymongo.DESCENDING),
                              ('Timestamp', pymongo.DESCENDING)],
                             unique=True)
    for idnex, row in all_indicators.iterrows():
        y = row.to_dict()
        # try:
        #     res=db_coll.insert_one(y)
        # except:
        # db_coll.delete_one({'Product':product.id,'Timestamp':y['Timestamp']})
        # res=db_coll.insert_one(y)
        #fuck this fucking module
        # res=db_coll.replace_one({'Product':product.id,'Timestamp':y['Timestamp']},y,upsert=True)
        try:
            y.pop('_id', None)
            res = db_coll.update_one(
                {
                    'Product': product.id,
                    'Timestamp': y['Timestamp']
                }, {"$set": y},
                upsert=True)
        except:
            print("Reminder to make a db system completely from scratch")
    #i swear to god, this is the last time I use a module, I didn´t write myself
    # res=db_coll.update_many({},y,upsert=True)
    # all_indicators.


def get_history(f=calculate_indicators, **kwargs):
    global client, product_history, product_current_data, product_complete_data
    mongo = MongoClient()
    # mongo.get_database('coinbase_history')
    try:
        db = mongo['coinbase_history']
        granularity = 21600
    except:
        granularity = 21600

    # from docs
    # [ time, low, high, open, close, volume  ],
    # [ 1415398768, 0.32, 4.2, 0.35, 4.2, 12.3  ],
    while 1:

        client = client_controller.client
        for product in market.products:
            db_coll = db[product.id]

            if len(product_history) > 0:
                p_history = [
                    x for x in product_history if x['id'] == product.id
                ]
            else:
                p_history = []
            try:
                start_date = fucking_date.now() - \
                    datetime.timedelta(336) if len(
                        p_history) == 0 else fucking_date.fromtimestamp(p_history[0]['data'][-1][0])
                end_date = start_date + datetime.timedelta(
                    0, granularity * 200)
                #calculate statistics for wanted data
                if start_date > fucking_date.now() - datetime.timedelta(
                        1) or end_date > fucking_date.now(
                        ) - datetime.timedelta(1) or kwargs.get('start_early'):
                    try:
                        f(product=product, **kwargs)
                    except Exception as e:
                        [fnctn(product=product, **kwargs) for fnctn in f]
                    finally:
                        product.is_analyzed = True
                    if kwargs.get('start_early'):
                        pass
                    else:
                        continue

                data = client.get_product_historic_rates(
                    product.id,
                    start=start_date,
                    end=end_date,
                    granularity=granularity)

                if len(p_history) == 0 and len(data) > 1:
                    data.reverse()
                    p_history = {'id': product.id, 'data': data}
                    product_history.append(p_history)
                    # mongo.()
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
        print([
            x['id'] + '{}, newest timestamp {}\n'.format(
                len(x['data']), fucking_date.fromtimestamp(x['data'][-1][0]))
            for x in product_history
        ])
        print('rsi values')
        #Note:
        #sorted doesn´t change the original list
        rsi_sorted = sorted(market.products, key=lambda x: x.rsi)
        print([
            f'{x.id}:{x.rsi:.{2}f}'.format(x.id, x.rsi) for x in rsi_sorted
            if x.rsi != 0
        ])
        print('euro_rates')
        print([
            '{}:{}:{}'.format(x.id, x.euro_rate, x.best_route_to_euro)
            for x in market.products if x.euro_rate != 1
        ])
        # print(product_history)
        # #time.sleep(10)
