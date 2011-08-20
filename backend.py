import logging

import shopify_api as s

from flask import Flask
app = Flask(__name__)

from flask import request

api_key = u'c90bd39bb9e9b66cf818046528b43e2e'
secret = u'e146abb4648f2c27d4d654738eded4bc'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/callback")
def callback():
    shop_url = request.args['shop']
    logging.info("Callback accessed by %s" % shop_url)
    
    request_dict = {}
    for k, v in request.args.iteritems():
        request_dict[k] = v

    try:
        logging.info("Authenticating for %s" % shop_url)
        import ipdb
        ipdb.set_trace()
        shop = s.Session(api_key, shop_url, secret, params=request_dict)
        logging.info("Authentication succeeded for %s" % shop_url)
    except s.AuthException as auth_e:
        logging.error("Authentication failed for %s" % shop_url)
        raise auth_e

if __name__ == "__main__":
    app.run()
