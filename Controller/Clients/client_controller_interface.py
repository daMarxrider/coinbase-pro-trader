class Client_Controller(object):
    def setup_client(*args,**kwargs):
        raise NotImplementedError

    def place_order(self,*args,**kwargs):
        raise NotImplementedError

    def get_products(self,*args,**kwargs):
        raise NotImplementedError

    def get_accounts(self,*args,**kwargs):
        raise NotImplementedError

    def get_account_history(self,*args,**kwargs):
        raise NotImplementedError

    def get_order(self,*args,**kwargs):
        raise NotImplementedError

    def get_product_24hr_stats(self,*args,**kwargs):
        raise NotImplementedError

    def get_product_historic_rates(self,*args,**kwargs):
        raise NotImplementedError