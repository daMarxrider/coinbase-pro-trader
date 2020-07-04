from Controller import client_controller
from Controller import market_controller as market
from Models.product import Product
from datetime import datetime as fucking_date
import datetime
import time
import statistics
import sys

product_history = []

# TODO
product_current_data = []
product_complete_data = []

client = None


def get_history(f=None):
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
                    end_date = start_date+datetime.timedelta(0,21600*100)

                    if start_date > fucking_date.now() and end_date > fucking_date.now():
                        end_date = fucking_date.now()

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
                    x=0
                    pass
                try:
                    print('newest date in {}\n{}'.format(product.id,
                                                         fucking_date.fromtimestamp(p_history[0]['data'][-1][0])))
                    product.historic_rates = p_history[0]['data']
                except Exception as e:
                    try:
                        print('newest date in {}\n{}'.format(product.id,
                                                             fucking_date.fromtimestamp(p_history['data'][-1][0])))
                        product.historic_rates = p_history['data']
                    except Exception as e:
                        pass
                time.sleep(1)
            try:
                start_date = fucking_date.now() - \
                    datetime.timedelta(12) if len(
                        p_history) == 0 else fucking_date.fromtimestamp(p_history[0]['data'][-1][0])
                end_date = fucking_date.now()
                mfi_values = client.get_product_historic_rates(
                    product.id, start=start_date, end=end_date, granularity=3600)
                mfi_values.reverse()
                low = mfi_values[0][1]
                high = mfi_values[0][2]
                pos=[]
                lows=[]
                for i in range(2,len(mfi_values)):
                    if mfi_values[i][4]>mfi_values[i-1][4]:
                        pos.append(mfi_values[i][4])
                    else:
                        lows.append(mfi_values[i][4])
                for value in mfi_values:
                    if value[1] < low:
                        low = value[1]
                    if value[2] > high:
                        high = value[2]
                rs=max(pos)/min(lows)
                rsi=100-100/(1+rs)
                product.rsi=rsi
                close = mfi_values[-1][4]
                tp = (high+low+close)/3
                # mf = tp*
            except:
                pass
            time.sleep(1)
        print('history')
        print([x['id']+'{}'.format(len(x['data'])) for x in product_history])
        # print(product_history)
        # time.sleep(10)
