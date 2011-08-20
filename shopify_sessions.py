import logging
import shopify_api as s
import utils

api_key = u'c90bd39bb9e9b66cf818046528b43e2e'
secret = u'e146abb4648f2c27d4d654738eded4bc'

sessions = {}

def create_shopify_session(request):
    request_dict = utils.make_dict_from_request_args(request.args)
    shop_url = request_dict['shop']

    try:
        logging.info("Authenticating for %s" % shop_url)
        shop_session = s.Session(api_key, shop_url, secret, params=request_dict)
        logging.info("Authentication succeeded for %s" % shop_url)

        if shop_url in sessions:
            raise Exception("Session already exists for %s" % shop_url)
        else:
            sessions[shop_url] = shop_session
    except s.AuthException as auth_e:
        logging.error("Authentication failed for %s" % shop_url)
        raise auth_e

    return shop_url, sessions[shop_url]
