import logging

from flask import Flask
app = Flask(__name__)

from flask import request, render_template

import shopify_sessions
import indexer

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/callback")
def callback():
    shop_url, shop_session = shopify_sessions.create_shopify_session(request)
    indexer.index_shop(shop_session)
    return render_template('authenticated.html', shop_url=shop_url)

@app.route("/hitme")
def hit_me():
    product = indexer.hit_me()
    kwargs = {
        'name' : product.name
    }
    
    return render_template('hit_me.html', **kwargs)

if __name__ == "__main__":
    app.run()
