def make_dict_from_request_args(request_args):
    request_dict = {}
    for k, v in request_args.iteritems():
        request_dict[k] = v
    return request_dict


