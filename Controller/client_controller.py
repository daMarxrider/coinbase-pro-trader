import sys
import cbpro
client = None

#TODO insert hook/decorator into client requests, to prevent exceeded rate limit
# https://docs.pro.coinbase.com/#rate-limits

# #Example from another project:
# #Important Note: Client-Object has multiple functions that call functions in the same scope
# #Therefore the stacktrace has to be analyzed additionally, as we don´t wan´t too much delay
#
# def setup(use_cf_scraper=False,combos=[]):
#     import requests
#     reset_proxies(combos=combos)
#     func_names=dir(requests)
#     if use_cf_scraper: requests=cfscrape.create_scraper()
#     for func_name in func_names:
#         # if callable(getattr(requests,func_name)):
#         obj=getattr(requests,func_name)
#         if isinstance(obj,types.FunctionType):
#             setattr(requests,func_name,decorator(obj))
#
#
# def decorator(f):
#     @functools.wraps(f)
#     def wrapper(*args,**kwargs):
#         try:
#             proxy=get_random_proxy()
#             return f(*args,**kwargs,proxies=proxy)
#         except Exception as e:
#             try:
#                 proxies.remove(proxy)
#             except:
#                 #proxy already removed, probably multithreading issue
#                 #everything ok
#                 pass
#     return wrapper

def setup_client(config):
    global client
    client = cbpro.AuthenticatedClient(config['system']['api_key'], config['system']
                                       ['secret_key'], config['system']['passphrase'], api_url=config['system']['uri'])
    return client
