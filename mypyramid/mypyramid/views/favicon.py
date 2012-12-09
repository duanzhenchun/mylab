import os
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently

@view_config(route_name='favicon')
def favicon_view(request):
    return HTTPMovedPermanently(location='/static/favicon.ico')
    
