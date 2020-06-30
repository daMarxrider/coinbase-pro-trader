from Controller import client_controller
from Controller import market_controller as market
from datetime import datetime as fucking_date
import datetime
import time

product_history = []
client = None


def get_history(f=None):
    global client, product_history

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
                end_date = start_date+datetime.timedelta(0, 21600*300)

                if start_date > fucking_date.now():
                    time.sleep(10)
                    continue
                if end_date > fucking_date.now():
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
                print('exception')
                print(e)
            try:
                print('newest date in {}\n{}'.format(product.id,
                                                     fucking_date.fromtimestamp(p_history[0]['data'][-1][0])))
                product.historic_rates = p_history[0]['data']
            except Exception as e:
                print('fuck {}'.format(product.id))
                try:
                    print('newest date in {}\n{}'.format(product.id,
                                                         fucking_date.fromtimestamp(p_history['data'][-1][0])))
                    product.historic_rates = p_history['data']
                    pass
                except Exception as e:
                    print('and fuck it hard')
                #print('fucking fuck\n {}\n can suck my fucking cock'.format(p_history))
            time.sleep(.5)
        print('history')
        print([x['id']+'{}'.format(len(x['data'])) for x in product_history])
        # print(product_history)
        # time.sleep(10)
