import random

import pymongo

import shopify_sessions

random.seed()

shop_products = {}

class ProductIndexer(object):
    logger = None
    
    mongo_conn = None
    shopifydb = None
    products = None
    shop_names = None
    
    def __init__(self, logger):
        self.logger = logger
        self.mongo_conn = pymongo.Connection('127.0.0.1', 5050)
        self.shopifydb = self.mongo_conn['shopify']
        self.products = self.shopifydb['products']
        self.shop_names = self.shopifydb['shop_names']

    def add_shop_name(self, shop_id, shop_name):
        query = {'shop_id' : shop_id}
        record = {'shop_id' : shop_id, 'shop_name' : shop_name}
        self.shop_names.update(query, record, upsert=True)
    def get_shop_name(self, shop_id):
        query = {'shop_id' : shop_id}
        result = self.shop_names.find_one(query)

        if result is None:
            return None

        return result['shop_name']

    def add_product(self, shop_id, product):
        query = {'product_id' : product.id, 'shop_id' : shop_id}
        record = {'product_id' : product.id, 'shop_id' : shop_id,
                  'product' : {
                      'title' : product.title,
                      'price' : float(product.variants[0].price),
                      }}
        self.products.update(query, record, upsert=True)
    def get_product(self, shop_id, product_id):
        query = {'product_id' : product_id, 'shop_id' : shop_id}
        result = self.products.find_one(query)

        if result is None:
            return None

        return result['product']

    def get_all_product_ids(self):
        results = self.products.find(spec=None,
                                     fields=['product_id', 'shop_id'])
        for r in results:
            yield (r['shop_id'], r['product_id'])

    def index_shop(self, session):
        shop = session.Shop.shop()
        self.add_shop_name(shop.id, shop.name)
    
        products = session.Product.find()
        for product in products:
            self.logger.debug("indexing %s from store %s" %
                              (product.title, shop.name))
            self.add_product(shop.id, product)

class ProductRex(object):
    logger = None
    product_indexer = None
    all_product_ids = None
    
    def __init__(self, logger, product_indexer):
        self.logger = logger
        self.product_indexer = product_indexer

        self.all_product_ids = {}
        for x in product_indexer.get_all_product_ids():
            self.all_product_ids[x] = 1

    def add_product_id(self, shop_id, product_id):
        self.all_product_ids[(shop_id, product_id)] = 1

    def hit_me(self):
        shop_id, product_id = random.choice(self.all_product_ids.keys())
        product = self.product_indexer.get_product(shop_id, product_id)

        discount = random.random()
        return product, discount, self.product_indexer.get_shop_name(shop_id)
