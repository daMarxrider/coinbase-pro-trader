import sys
from Controller import market_controller as market, wallet_controller as wallet

products = []

trading_configs = [{
    "name": "momentum_rsi",
    "buy": lambda x: x.calculated_indicators["momentum_rsi"].values[-1] <= 33,
    "sell": lambda x: x.calculated_indicators["momentum_rsi"].values[-1] >= 66,
}, {
    "name": "trend_macd",
    "buy": lambda x: x.calculated_indicators["trend_macd"].values[-1] > x.calculated_indicators["trend_macd_signal"].values[-1],
    "sell": lambda x: x.calculated_indicators["trend_macd"].values[-1] < x.calculated_indicators["trend_macd_signal"].values[-1],
}, {
    "name":
        "trend_ichimoku",
    "buy":
        lambda x: x.calculated_indicators['Close'].values[-1] > x.calculated_indicators["trend_ichimoku_a"].values[-1] and x.
        calculated_indicators['Close'].values[-1] > x.calculated_indicators["trend_ichimoku_b"].values[-1],
    "sell":
        lambda x: not (x.calculated_indicators['Close'].values[-1] > x.calculated_indicators["trend_ichimoku_a"].values[-1] and x.calculated_indicators['Close'].values[-1] > x.calculated_indicators["trend_ichimoku_b"].values[-1]),
}]


def setup(used_configs):
    global products
    products = market.products

    resolved_configs = []
    for conf in used_configs:
        for res in trading_configs:
            if res['name'] == conf:
                resolved_configs.append(res)
                break
        else:
            print(f'config {conf} not found')
    used_configs=resolved_configs
    while 1:
        try:
            for product in products:
                votes = []
                try:
                    for conf in used_configs:
                        for order in wallet.orders:
                            if order.quote_currency in product.id and order.base_currency in product.id:
                                if order.status in ["pending", "open"]:  # TODO check if date is old enough to start new transaction ~7days
                                    continue
                        if conf["buy"](product):
                            if len(product.own_transactions) > 0 and product.own_transactions[-1].type == "buy":
                                continue
                            votes.append("buy")
                        elif conf["sell"](product):
                            if len(product.own_transactions) > 0 and product.own_transactions[-1].type == "sell":
                                continue
                            votes.append("sell")
                        else:
                            votes.append("hold")
                    for action in set(votes):
                        if 1 / (len(votes) / votes.count(action)) > 0.70:
                            getattr(wallet, action)(product)
                            break
                    else:
                        print(product.id)
                        print(votes)
                except Exception as e:
                    exc_type, exc_obj, tb = sys.exc_info()
                    f = tb.tb_frame
                    lineno = tb.tb_lineno
                    filename = f.f_code.co_filename
        except Exception as e:
            print("error during market placement")
            print(e)
