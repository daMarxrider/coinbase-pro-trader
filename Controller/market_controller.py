from Controller import client_controller
import websocket
import _thread as thread
import json
from Controller import fuck_json
from Models.product import Product
from Models.transaction import Transaction

client = client_controller.client
products = []


def on_ticker_message(ws, message):
    global products
    try:
        message = json.loads(message)
        # print(message)
        # print('{}:{}'.format(message['product_id'], message['price']))
        received_product = [x for x in products if x.id == message['product_id']][0]
        received_product.rate = float(message['price'])
        get_best_route_to_euro(received_product)
        base_currency = message['product_id'].split('-')[1] if message['side'] == 'buy' else message['product_id'].split('-')[0]
        quote_currency = message['product_id'].split('-')[0] if message['side'] == 'sell' else message['product_id'].split('-')[1]
        [x for x in products if x.id == message['product_id']][0].public_transactions.append(Transaction(
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
        body = {'type': 'subscribe', 'product_ids': [x.id for x in products], 'channels': [{'name': 'ticker'}]}
        ws.send(fuck_json.to_json(body))
        # #time.sleep(1)
        # ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


def init_products():
    global products
    if len(products) == 0:
        for product in client.get_products():
            products.append(Product(json=product))
    return products


# semi-important TODO:
# read more about full channel in docs and maybe switch/implement retrievement/handling of additional data


def get_products_feed():
    global client
    if client is None:
        client=client_controller.client
    init_products()
    if client_controller.type == "coinbase-pro":
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com/ticker", on_message=on_ticker_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
    else:
        raise NotImplementedError


def get_best_route_to_euro(inst_product):
    routes = []
    if inst_product.id.__contains__('EUR'):
        inst_product.best_route_to_euro = [inst_product.id]
        inst_product.euro_rate = inst_product.rate
        return
    for product in products:
        try:
            route_start = [x for x in product.best_route_to_euro if x.split('-')[0] == inst_product.quote_currency]
            if product.euro_rate != 1 and len(route_start):
                calc_rate = inst_product.rate
                route_list = product.best_route_to_euro[product.best_route_to_euro.index(route_start[0]):]
                for p_temp in products:
                    if p_temp.id in route_list:
                        calc_rate *= p_temp.rate * 0.995
                routes.append({'route': [inst_product.id] + route_list, 'rate': calc_rate})
        except Exception:
            pass
    try:
        routes.sort(key=lambda x: x['rate'], reverse=True)
        inst_product.best_route_to_euro = routes[0]['route']
        inst_product.euro_rate = routes[0]['rate']
        return inst_product.best_route_to_euro, inst_product.euro_rate
    except Exception:
        # no route found
        pass


def get_transactions(days=0):
    # TODO
    pass
