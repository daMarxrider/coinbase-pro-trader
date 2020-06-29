import cbpro
import websocket
import _thread as thread
import time
import json
import sys
from Controller import fuck_json
from Models.product import Product

client = cbpro.PublicClient()
products = []


# TODO extract into own class and set new values with function references
def on_ticker_message(ws, message):
    global products
    try:
        message = json.loads(message)
        # print(message)
        # print(message['price'])
        [x for x in products if x.id == message['product_id']
         ][0].rate = message['price']
    except Exception as e:
        print(e)
        print(message)


def on_error(ws, error):
    pass
    # print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        body = {'type': 'subscribe',
                'product_ids': [x.id for x in products],
                'channels': [{'name': 'ticker'}]}
        ws.send(fuck_json.to_json(body))
        # time.sleep(1)
        # ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


def init_products():
    global products
    if len(products) == 0:
        for product in client.get_products():
            products.append(Product(
                id=product['id'], base_currency=product['base_currency'], quote_currency=product['quote_currency']))
    return products


def get_products_feed():
    init_products()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com/ticker",
                                on_message=on_ticker_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


def get_orders(product):
    # TODO
    pass


def get_transactions(days=0):
    # TODO
    pass


def get_rate(product):
    pass
    # TODO listen for websocket (see coinbasepro-python/blob/master/cbpro/public-client.py)
    # at get_product_ticker
