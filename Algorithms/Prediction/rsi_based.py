
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

def calculate_rsi(product,**kwargs):
    shortened_mfi = []
    days = 14
    better_start_date = fucking_date.now() - datetime.timedelta(days)
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