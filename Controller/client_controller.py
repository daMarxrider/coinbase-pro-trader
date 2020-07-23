import functools
import sys
import types

import cbpro
from cbpro import AuthenticatedClient
import time
client: AuthenticatedClient= None
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
        try:
            if type(res)in [list,types.GeneratorType]:
                results=[]
                for x in res:
                    results.append(x)
            else:
                results={}
                for key,value in res.items():
                    results[key]=value
        except:
            results=res
        if 'message' in results:
            message=res['message']
            if message.__contains__('rate limit exceeded'):
                time.sleep(1)
                res=f(*args,**kwargs,)
        return results
    return wrapper

def setup_client(config):
    global client
    client = cbpro.AuthenticatedClient(config['system']['api_key'], config['system']
                                       ['secret_key'], config['system']['passphrase'], api_url=config['system']['uri'])
    setup_api_timeout()
    return client
