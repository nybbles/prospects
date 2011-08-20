import logging
import random

import shopify_sessions

random.seed()

shop_name = {}
shop_products = {}

def index_shop(session):
    shop = session.Shop.shop()
    shop_name[shop.id] = shop.name
    
    products = session.Product.find()
    for product in products:
        logging.info("indexing %s from store %s" % (product.title, shop.name))
        shop_products[product.id] = (product, shop.id)

def hit_me():
    product = shop_products[random.choice(d.keys())]
    return product
