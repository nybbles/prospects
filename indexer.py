import random

import shopify_sessions

random.seed()

shop_name = {}
shop_products = {}

class ProductIndexer(object):
    logger = None
    
    def __init__(self, logger):
        self.logger = logger

    def index_shop(self, session):
        shop = session.Shop.shop()
        shop_name[shop.id] = shop.name
    
        products = session.Product.find()
        for product in products:
            self.logger.debug("indexing %s from store %s" % (product.title, shop.name))
            shop_products[product.id] = (product, shop.id)

class ProductRex(object):
    logger = None
    
    def __init__(self, logger):
        self.logger = logger

    def hit_me(self):
        product, shop_id = shop_products[random.choice(shop_products.keys())]
        discount = random.random()
        
        return product, discount, shop_name[shop_id]
