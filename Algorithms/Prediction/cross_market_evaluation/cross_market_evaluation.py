import sys
import linecache
from Controller import history_controller as history
import statistics
from datetime import timedelta,datetime as fucking_date

evaluated_products = []
product_history = history.product_history


def setup():
    global evaluated_products,product_history,history
    evaluated_products=[]
    while 1:
        try:
            product_history = history.product_history
            if any(x['data'][-1][0] >= (fucking_date.now()-timedelta(1)).timestamp() for x in product_history):
                for p_history in product_history:
                    try:
                        if len([x for x in evaluated_products if x.id==p_history['id']])==0:
                            evaluated_products.append(Dependent(p_history['id']))
                    except:
                        pass
        except:
            pass


class Dependent(object):
    id = ''
    p_ref = None
    dependencies = []
    highest_mimicry = None

    def __init__(self, p_id, dependencies=[]):
        self.id = p_id
        print('getting dependencies')
        self.create_dependents()
        print('{}-{} with {}'.format(self.id,
                                     self.highest_mimicry['id'], self.highest_mimicry['value']))

    def create_dependents(self):
        try:
            slots = [x for x in product_history if x['id']
                     == self.id][0]['data']

            # from docs
            # [ time, low, high, open, close, volume   ],
            # [ 1415398768, 0.32, 4.2, 0.35, 4.2, 12.3   ],
            for dep_product in product_history:
                if dep_product['id'] == self.id:
                    continue
                dependency = {'id': dep_product['id']}
                i = 0
                mimicries = []
                for slot in slots:
                    print(slot)
                    diff = 0
                    for dep_slot in dep_product['data'][i:]:
                        if dep_slot[0] > slot[0]:
                            diff = dep_slot[0]-slot[0]
                        elif dep_slot[0] <= slot[0] and slot[0]-dep_slot[0] < diff:
                            diff = slot[0]-dep_slot[0]
                            i = dep_product['data'].index(dep_slot)
                            # map.append([slots.index(slot), i])
                            mimicries.append({'id': dep_product['id'], 'value':
                                              (slot[4]/slot[3])/(dep_slot[4]/dep_slot[3])})
                            # calculate dependency because mapping is unnecessarily expensive
                            break
                        else:
                            # map.append(
                            #    [slots.index(slot, i := dep_product['data'].index(dep_slot))])
                            i = dep_product['data'].index(dep_slot)-1
                            mimicries.append({'id': dep_product['id'], 'value':
                                              (slot[4]/slot[3])/(dep_product['data'][i][4]/dep_product['data'][i][3])})

                            # calculate dependency because mapping is unnecessarily expensive
                            break
                mimicry = statistics.pstdev([x['value'] for x in mimicries])
                if mimicry > 0.7:
                    self.dependencies.append(
                        {'id': dep_product['id'], 'value': mimicry})
            for dep in self.dependencies:
                if self.highest_mimicry is None or self.highest_mimicry['value'] < dep['value']:
                    self.highest_mimicry = dep
        except IndexError:
            print('probably no valid history available, if you are using the sandbox api, this is definitely the case')
        except Exception as e:
            print('exception')
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            print(e)
            print(lineno)
            print(line)
