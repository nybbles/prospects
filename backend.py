import logging

from flask import Flask
app = Flask(__name__)

from flask import request, render_template

import shopify_sessions

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/callback")
def callback():
    shop_url, _ = shopify_sessions.create_shopify_session(request)
    return render_template('authenticated.html', shop_url=shop_url)

if __name__ == "__main__":
    app.run()
