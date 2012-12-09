#encoding:utf-8

import json
from pyramid.view import view_config
from pyramid.security import (authenticated_userid, forget, remember)
from pyramid.httpexceptions import (HTTPFound,HTTPForbidden)
from velruse import login_url

import logging
log = logging.getLogger(__name__)


@view_config(route_name='home')
def home_view(request):
    return HTTPFound(location='reader')
    
    
@view_config(route_name='logout')
def logout(request):
    log.debug('logout')
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers)
                         
    
@view_config(
    route_name='velruse_login',
    renderer='velruse/login.mako',)
def login_view(request):
    # get came_from
    referrer = request.url
    if referrer == request.route_url('velruse_login'):
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    log.debug(came_from)
    return {
        'login_url': login_url,
        'providers': request.registry.settings['login_providers'],
        'came_from': came_from,
    }
    
        
@view_config(
    context='velruse.AuthenticationComplete',
    renderer='velruse/result.mako',)
def login_complete_view(request):
    
    context = request.context
    result = {
        'profile': context.profile,
        'credentials': context.credentials,
    }
    account = context.profile['accounts'][0]
    userid='_'.join((account['domain'], account['userid']))
    headers = remember(request, userid)
    return HTTPFound(location = came_from,
                 headers = headers)
#    return {
#        'result': json.dumps(result, indent=4),
#    }

@view_config(
    context='velruse.AuthenticationDenied',
    renderer='velruse/result.mako',)
def login_denied_view(request):
    return {
        'result': 'denied',
    }
