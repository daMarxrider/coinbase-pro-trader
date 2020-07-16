import functools
import sys
import types

import cbpro
import time
client = None
last_request=None

#TODO insert hook/decorator into client requests, to prevent exceeded rate limit
# https://docs.pro.coinbase.com/#rate-limits

#Example from another project:
#Important Note: Client-Object has multiple functions that call functions in the same scope
#Therefore the stacktrace has to be analyzed additionally, as we don´t wan´t too much delay

def setup_api_timeout():
    func_names=dir(client)
    for func_name in func_names:
        # if callable(getattr(requests,func_name)):
        obj=getattr(client,func_name)
        if isinstance(obj,types.FunctionType) or isinstance(obj,types.MethodType):
            setattr(client,func_name,decorator(obj))


def decorator(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        global last_request
        res=f(*args,**kwargs,)
        if 'message' in res:
            message=res['message']
            if message.__contains__('rate limit exceeded'):
                time.sleep(1)
                res=f(*args,**kwargs,)
            else:
                x=0
        return res
        #
        # try:
        #     rest_time=1-(time.perf_counter()-last_request)
        #     time.sleep(rest_time)
        #     last_request=time.perf_counter()
        # except:
        #     last_request=time.perf_counter()
        # return f(*args,**kwargs,)
    return wrapper

def setup_client(config):
    global client
    client = cbpro.AuthenticatedClient(config['system']['api_key'], config['system']
                                       ['secret_key'], config['system']['passphrase'], api_url=config['system']['uri'])
    setup_api_timeout()
    return client
