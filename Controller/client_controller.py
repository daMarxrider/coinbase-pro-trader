import functools
import types

import cbpro
from cbpro import AuthenticatedClient
import time
client: AuthenticatedClient = None
last_request = None
isWorking=False


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
    global client
    client = cbpro.AuthenticatedClient(config['system']['api_key'],
                                       config['system']['secret_key'],
                                       config['system']['passphrase'],
                                       api_url=config['system']['uri'])
    setup_api_timeout()
    return client
