import types
from client_controller_interface import *
import cbpro
from cbpro import AuthenticatedClient
import time
client: AuthenticatedClient = None
last_request = None
isWorking = False


class CbPro_Client(Client_Controller):
    def setup_api_timeout():
        func_names = dir(client)
        for func_name in func_names:
            # if callable(getattr(requests,func_name)):
            obj = getattr(client, func_name)
            if isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType):
                setattr(client, func_name, decorator(obj))

    def decorator(f):
        def wrapper(*args, **kwargs):
            global last_request
            while True:
                res = f(
                    *args,
                    **kwargs,
                )
                try:
                    if type(res) in [list, types.GeneratorType]:
                        results = []
                        for x in res:
                            results.append(x)
                    else:
                        results = {}
                        for key, value in res.items():
                            results[key] = value
                except Exception:
                    results = res
                if 'message' in results and results['message'].__contains__('rate limit exceeded'):
                    time.sleep(1)
                    continue
                return results

        return wrapper

    def setup_client(config):
        global client,isWorking
        client = cbpro.AuthenticatedClient(config['system']['api_key'],
                                           config['system']['secret_key'],
                                           config['system']['passphrase'],
                                           api_url=config['system']['uri'])
        isWorking = True
        setup_api_timeout()
        return client

    def place_order(self,product_id=None,side=None,limit=False,funds=0,rate=None,*args,**kwargs):
        if limit:
            return client.place_limit_order(product_id, side, rate, size=funds)
        else:
            return client.place_market_order(product_id, side, size=funds)

    def get_products(self,*args,**kwargs):
        return client.get_products()

    def get_accounts(self,*args,**kwargs):
        return client.get_accounts(*args)

    def get_account_history(self,*args,**kwargs):
        return client.get_account_history(*args)

    def get_order(self,*args,**kwargs):
        return client.get_order(*args)

    def get_product_24hr_stats(self,*args,**kwargs):
        return client.get_product_24hr_stats(*args)
