
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

def calculate_rsi(client, product):
    shortened_mfi = []
    better_start_date = fucking_date.now() - datetime.timedelta(days:=14)
    better_end_date = better_start_date + datetime.timedelta(1)
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

    shortened_df = (pd.DataFrame(
        shortened_mfi, columns=['Open', 'High', 'Low', 'Close', 'Volume']))

    shortened_rsi_value = \
        rsi(pd.Series(data=[x[4] for x in shortened_mfi]), n=shortened_mfi).values[-1]
    product.rsi = shortened_rsi_value