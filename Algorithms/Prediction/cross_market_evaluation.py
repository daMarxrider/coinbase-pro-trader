import sys
import linecache
from Controller import history_controller as history
import statistics
from datetime import timedelta, datetime as fucking_date
from Controller import market_controller as market

evaluated_products = []
product_history = []
products=[]


def setup():
    global evaluated_products, product_history
    while 'history.product_history' not in dir(history):
        pass
    product_history=history.product_history
    evaluated_products = []
    while 1:
        try:
            products=market.products
            product_history = history.product_history
            if any(x['data'][-1][0] >= (fucking_date.now()-timedelta(1)).timestamp() for x in product_history):
                for p_history in product_history:
                    try:
                        if len([x for x in evaluated_products if x.id == p_history['id']]) == 0:
                            evaluated_products.append(
                                EvaluatedProduct(p_history['id']))
                        else:
                            [x for x in evaluated_products if x.id ==
                                p_history['id']][0].create_dependents()
                    except:
                        pass
        except Exception as e:
            print('exception')
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            print('Exception at {} line {}'.format(filename, lineno))


class EvaluatedProduct(object):
    id = ''
    p_ref = None
    dependencies = []
    highest_mimicry = None

    def __init__(self, p_id, dependencies=[]):
        self.id = p_id
        self.create_dependents()
        print('{}-{} with {}'.format(self.id,
                                     self.highest_mimicry['id'], self.highest_mimicry['value']))

    def create_dependents(self):
        try:
            slots = [x for x in product_history if x['id']
                     == self.id][0]['data']

            def mapper(slot, mimics):
                diff = None
                for mimic in mimics:
                    if mimic is None:
                        continue
                    if diff == None or abs(slot[0] - mimic[0]) < diff:
                        diff = abs(slot[0] - mimic[0])
                    else:
                        return mimic

            # from docs
            # [ time, low, high, open, close, volume   ],
            # [ 1415398768, 0.32, 4.2, 0.35, 4.2, 12.3   ],
            for dep_product in product_history:
                if dep_product['id'] == self.id:
                    continue
                mimic_results = []
                for slot in slots:
                    mimic = mapper(slot, dep_product['data'])
                    if mimic is None:
                        continue
                    mimic_results.append(
                        (mimic[4]/mimic[3])/(slot[4]/slot[3]))

                mimicry = statistics.pstdev(mimic_results)
                if mimicry < 0.1:
                    [x for x in market.products if x.id == self.id][0].mimicries.append({'id':dep_product['id'],'value':mimic})
                    id = ([x for x in self.dependencies if x['id'] == dep_product['id']])
                    if len(id) == 0:
                        self.dependencies.append(
                            {'id': dep_product['id'], 'value': mimicry})
                    else:
                        # index=self.dependencies.index((id))
                        id[0]['value'] = mimicry
            for dep in self.dependencies:
                if self.highest_mimicry is None or self.highest_mimicry['value'] > dep['value']:
                    self.highest_mimicry = dep
            [x for x in market.products if x.id == self.id][0].highest_mimicry={'id':self.highest_mimicry['id'],'value':self.highest_mimicry['value']}
        except IndexError:
            print('probably no valid history available, if you are using the sandbox api, this is definitely the case')
        except Exception as e:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            pass
