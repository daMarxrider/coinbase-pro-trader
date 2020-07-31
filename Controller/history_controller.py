from . import client_controller
from . import market_controller as market
from Models.product import Product
from datetime import datetime as fucking_date
import datetime
import pandas as pd
from ta import add_all_ta_features
import pymongo
from pymongo import *

product_history = []

product_current_data = []
product_complete_data = []

client = client_controller.client


def get_data_for_timespan(start: datetime, end: datetime, product):
    mongo = MongoClient()
    db = mongo["coinbase_history"]
    c = db.get_collection("historical_data")
    data = []
    for d in c.find({'Product': product.id}):
        data.append(d)
    days = (end - start).days

    wanted_dates = []
    for i in range(0, days + 1):
        wanted_dates.append((start + datetime.timedelta(i)).timestamp())
    dates, last_date = [], start.timestamp()
    data.reverse()
    # TODO get biggest diff of data to check if data is missing
    for i in range(0, len(data)):
        try:
            # if abs(data[i]['Timestamp'] - wanted_dates[0]) > abs(data[i - 1]['Timestamp'] - wanted_dates[0]):
            #     dates.append(data[i - 1])
            #     wanted_dates.pop(0)
            if abs((fucking_date.fromtimestamp(data[i]['Timestamp']) - fucking_date.fromtimestamp(
                    wanted_dates[0])).total_seconds()) < 43200:
                dates.append(data[i])
                wanted_dates.pop(0)
        except Exception as e:
            pass
    # if fucking_date.fromtimestamp(dates[-1]['Timestamp']).date()==fucking_date.fromtimestamp(wanted_dates[0]).date():
    #     wanted_dates.pop(0)

    if len(wanted_dates) == 1 and fucking_date.fromtimestamp(wanted_dates[0]).date() == fucking_date.today().date() \
            or len(dates)>0 and (fucking_date.now().date() - fucking_date.fromtimestamp(dates[-1]['Timestamp']).date()).days == 1 \
            and end.date() == fucking_date.today().date():
        today = client.get_product_24hr_stats(product.id)
        parsed_today = {

            "Product": product.id,
            "Timestamp": datetime.datetime.combine(datetime.datetime.today(), datetime.time()).timestamp(),
            "Low": float(today['low']),
            "High": float(today['high']),
            "Open": float(today['open']),
            "Close": float(today['last']),
            "Volume": float(today['volume'])
        }
        dates.append(parsed_today)
        mongo.close()
        return dates
    else:
        for i in range(0, wanted_dates.__len__()):
            wanted_dates[i] = fucking_date.fromtimestamp(wanted_dates[i]).date()
        # TODO get still needed data from client
        data = []
        if wanted_dates[-1] == fucking_date.now().date():
            wanted_dates.pop(-1)
            data.append(client.get_product_24hr_stats(product.id))
        data.extend(client.get_product_historic_rates(product.id, start=start, end=end,
                                                      granularity=86400))
        data.reverse()
        try:
            db.create_collection("historical_data",
                                 **{"_id": [("Product", pymongo.ASCENDING), ("Timestamp", pymongo.ASCENDING)]})
        except Exception:
            pass
        finally:
            db_coll = db["historical_data"]
            db_coll.create_index([("Product", pymongo.DESCENDING), ("Timestamp", pymongo.DESCENDING)], unique=True)
        for row in data:
            if 'low' in row:
                break
            row = {
                "Product": product.id,
                "Timestamp": row[0],
                "Low": row[1],
                "High": row[2],
                "Open": row[3],
                "Close": row[4],
                "Volume": row[5]
            }
            try:
                db_coll.update_one({"Product": product.id, "Timestamp": row["Timestamp"]}, {"$set": row}, upsert=True)
            except Exception:
                print("Reminder to make a db system completely from scratch")

        dates=[]
        for row in data:
            try:
                dates.append({
                "Product": product.id,
                "Timestamp": row[0],
                "Low": row[1],
                "High": row[2],
                "Open": row[3],
                "Close": row[4],
                "Volume": row[5]
            })
            except Exception:
                try:
                    data[-1] = {
                        "Product": product.id,
                        "Timestamp": datetime.datetime.combine(datetime.datetime.today(), datetime.time()).timestamp(),
                        "Low": float(data[-1]['low']),
                        "High": float(data[-1]['high']),
                        "Open": float(data[-1]['open']),
                        "Close": float(data[-1]['last']),
                        "Volume": float(data[-1]['volume'])
                    }
                except:
                    pass
        try:
            mongo.close()
        except:
            pass
        return dates


# TODO get indicators to euro with best_route_to_euro of product
def calculate_indicators(product: Product, **kwargs):
    try:
        days = 60
        better_start_date = fucking_date.now() - datetime.timedelta(days)
        better_end_date = fucking_date.now()
        shortened_better_data = get_data_for_timespan(better_start_date, better_end_date, product)

        # IMPORTANT TODO CALCULATE DATA FOR EVERY POSSIBLE RELATION IN A 3DIMENSIONAL ARRAY7
        complete_data = pd.DataFrame(shortened_better_data,
                                     columns=["Product", "Timestamp", "Open", "High", "Low", "Close", "Volume"])
        all_indicators = add_all_ta_features(complete_data, open="Open", high="High", low="Low", close="Close",
                                             volume="Volume", fillna=True)
        product.calculated_indicators = all_indicators
        product.rsi = all_indicators["momentum_rsi"].values[-1]

    except Exception as e:
        pass
        # print(f'couldn´t calculate data for {product.id}, due to lack of data')


def get_history(f=calculate_indicators, **kwargs):
    global client, product_history, product_current_data, product_complete_data
    granularity = 86400

    # from docs
    # [ time, low, high, open, close, volume  ],
    # [ 1415398768, 0.32, 4.2, 0.35, 4.2, 12.3  ],
    while 1:

        client = client_controller.client
        for product in market.products:
            if len(product_history) > 0:
                p_history = [x for x in product_history if x["id"] == product.id]
            else:
                p_history = []
            try:
                start_date = (fucking_date.now() - datetime.timedelta(300)
                              if len(p_history) == 0 else fucking_date.fromtimestamp(p_history[0]["data"][-1][0]))
                end_date = start_date + datetime.timedelta(0, granularity * 300)
                # calculate statistics for wanted data
                if (start_date > fucking_date.now() - datetime.timedelta(
                        1) or end_date > fucking_date.now() - datetime.timedelta(1)
                        or kwargs.get("start_early")):
                    try:
                        f(product=product, **kwargs)
                    except Exception as e:
                        [fnctn(product=product, **kwargs) for fnctn in f]
                    finally:
                        product.is_analyzed = True
                    if kwargs.get("start_early"):
                        pass
                    else:
                        continue

                data = get_data_for_timespan(start_date,end_date,product)

                if len(p_history) == 0 and len(data) > 1:
                    p_history = {"id": product.id, "data": data}
                    product_history.append(p_history)
                    # mongo.()
                elif len(data) > 1:
                    p_history[0]["data"].extend(data)
            except Exception:
                pass
            try:
                product.historic_rates = p_history[0]["data"]
            except Exception:
                try:
                    product.historic_rates = p_history["data"]
                except Exception:
                    pass
        print("history")
        print([
            x["id"] + "{}, newest timestamp {}\n".format(len(x["data"]), fucking_date.fromtimestamp(x["data"][-1][0]))
            for x in product_history
        ])
        print("rsi values")
        # Note:
        # sorted doesn´t change the original list
        rsi_sorted = sorted(market.products, key=lambda x: x.rsi)
        print([f"{x.id}:{x.rsi:.{2}f}".format(x.id, x.rsi) for x in rsi_sorted if x.rsi != 0])
        print("euro_rates")
        print(["{}:{}:{}".format(x.id, x.euro_rate, x.best_route_to_euro) for x in market.products if x.euro_rate != 1])
