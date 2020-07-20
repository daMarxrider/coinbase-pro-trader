from Controller import market_controller as market, wallet_controller as wallet

products = []

trading_configs = [{
    "name": "momentum_rsi",
    "buy": lambda x: x.calculated_indicators["momentum_rsi"].values[-1] <= 33,
    "sell": lambda x: x.calculated_indicators["momentum_rsi"].values[-1] >= 66
}]


def setup(indicators=[]):
    global products
    products = market.products
    while 1:
        used_configs = []
        used_configs.append(trading_configs[0])
        try:
            for product in products:
                votes=[]
                try:
                    for conf in used_configs:
                        for order in wallet.orders:
                            if order.quote_currency in product.id and order.base_currency in product.id:
                                if order.status in ['pending', 'open']:#TODO check if date is old enough to start new transaction ~7days
                                    continue
                        if conf['buy'](product):
                            if len(product.own_transactions) > 0 and product.own_transactions[-1].type == 'buy':
                                continue
                            votes.append("buy")
                        elif conf['sell'](product):
                            if len(product.own_transactions) > 0 and product.own_transactions[-1].type == 'sell':
                                continue
                            votes.append("sell")
                        else:
                            votes.append("hold")
                    for action in set(votes):
                        if 1/(len(votes)/votes.count(action))>70:
                            getattr(wallet,action)(product)
                except:
                    pass
        except Exception as e:
            print('error during market placement')
            print(e)
