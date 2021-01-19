#"""This module contains common functionality used in FastAPI and legacy controllers."""
#
#class Router(APIRouter):
#    def __init__(self, *args, **kwargs):
#        super(args, kwargs)
#        self.prefix = '/api'
#
#
#def parse_serialization_params(kwd, default_view):
#    view = kwd.get('view', None)
#    keys = kwd.get('keys')
#    # TODO change this to pythonic
#    # TODO point all legacy stuff here
#    if isinstance(keys, str):
#        keys = keys.split(',')
#    return dict(view=view, keys=keys, default_view=default_view)
#
#
