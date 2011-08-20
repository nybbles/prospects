import logging

from flask import Flask
app = Flask(__name__)

from flask import request, render_template

import shopify_sessions
import indexer

session_manager = shopify_sessions.ShopifySessionManager(app.logger)
product_indexer = indexer.ProductIndexer(app.logger)
product_rex = indexer.ProductRex(app.logger)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/callback")
def callback():
    shop_url, shop_session = session_manager.add_shopify_session(request)
    product_indexer.index_shop(shop_session)
    return render_template('authenticated.html', shop_url=shop_url)

@app.route("/hitme")
def hit_me():
    product = product_rex.hit_me()
    kwargs = {
        'name' : product[0].title
    }
    
    return render_template('hit_me.html', **kwargs)

if __name__ == "__main__":
    app.debug = True
    app.run()
