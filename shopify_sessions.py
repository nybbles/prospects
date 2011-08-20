import shopify_api as s
import utils

class ShopifySessionManager(object):
    api_key = u'c90bd39bb9e9b66cf818046528b43e2e'
    secret = u'e146abb4648f2c27d4d654738eded4bc'

    sessions = {}
    logger = None
    
    def __init__(self, logger):
        self.logger = logger

    def add_shopify_session(self, request):
        request_dict = utils.make_dict_from_request_args(request.args)
        shop_url = request_dict['shop']

        if not shop_url in self.sessions:
            try:
                self.logger.debug("Authenticating for %s" % shop_url)
                shop_session = s.Session(self.api_key, shop_url, self.secret,
                                         params=request_dict)
                self.logger.debug("Authentication succeeded for %s" % shop_url)
                self.sessions[shop_url] = shop_session
            except s.AuthException as auth_e:
                self.logger.error("Authentication failed for %s" % shop_url)
                raise auth_e

        return shop_url, self.sessions[shop_url]
