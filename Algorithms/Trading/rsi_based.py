# from Controller import market_controller as market
# from Controller import wallet_controller as wallet
#
# products = []
#
# min_rsi, max_rsi=33,66
#
# #TODO check for rsi to euro and send "order-chain"(i.e. buy and sell according to best_route_to_euro of product)
# def setup(plugins=[]):
#     products = market.products
#     while 1:
#         try:
#             for product in products:
#                 if 'COMP' in product.id:
#                     continue
#                 #TODO func-ref check 1
#                 if product.rsi!=0:
#                     x = 0
#                     for order in wallet.orders:
#                         if order.quote_currency in product.id and order.base_currency in product.id:
#                             if order.status in ['pending', 'open']:
#                                 continue
#                     #TODO func-ref check 2 start
#                     if product.rsi < min_rsi:
#                         if len(product.own_transactions)>0 and product.own_transactions[-1].type=='buy':
#                             continue
#                         wallet.buy(product)
#                     elif product.rsi > max_rsi:
#                         if len(product.own_transactions)>0 and product.own_transactions[-1].type=='sell':
#                             continue
#                         wallet.sell(product)
#                     #TODO func-ref check 2 end
#         except Exception as e:
#             print('error during market placement')
#             print(e)
#
