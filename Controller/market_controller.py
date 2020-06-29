import cbpro
client = cbpro.PublicClient()


def get_products():
    products = client.get_products()
    print(products)
    return products
