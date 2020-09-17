class Client_Controller(object):
    def setup_client(*args,**kwargs):
        raise NotImplementedError

    def place_order(self,*args,**kwargs):
        raise NotImplementedError

    def get_products(self,*args,**kwargs):
        raise NotImplementedError
