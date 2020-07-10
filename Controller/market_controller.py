import cbpro
import websocket
import _thread as thread
import time
import json
import sys
from Controller import fuck_json
from Models.product import Product
from Models.transaction import Transaction

client = cbpro.PublicClient()
products = []


def on_ticker_message(ws, message):
    global products
    try:
        message = json.loads(message)
        # print(message)
        #print('{}:{}'.format(message['product_id'], message['price']))
        [x for x in products if x.id == message['product_id']
         ][0].rate = message['price']
        [x for x in products if x.id == message['product_id']
         ][0].get_best_route_to_euro()
        base_currency = message['product_id'].split(
            '-')[1] if message['side'] == 'buy' else message['product_id'].split('-')[0]
        quote_currency = message['product_id'].split(
            '-')[0] if message['side'] == 'sell' else message['product_id'].split('-')[1]
        [x for x in products if x.id == message['product_id']
         ][0].public_transactions.append(Transaction(
             message['trade_id'], base_currency, quote_currency, rate=message['price']))
    except Exception as e:
        pass
        # print(e)
        # print(message)


def on_error(ws, error):
    pass
    # print(error)


def on_close(ws):
    print("### closed ###")
    get_products_feed()


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
                id=product['id'], base_currency=product['base_currency'], quote_currency=product['quote_currency'],view_only= product['trading_disabled'],min_transaction_size=product['min_market_funds']))
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


def get_transactions(days=0):
    # TODO
    pass
