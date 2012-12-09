from pyramid.renderers import render
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.view import (
    forbidden_view_config,
    view_config,
    )

import logging
log = logging.getLogger(__name__)

@forbidden_view_config()
def editor_signin(request):
    import traceback
    for line in traceback.format_stack():
        print line.strip()
    log.debug('editor_signin')
    body = render('editor/signin.mako', {}, request=request)
    return Response(body, status='403 Forbidden')


@view_config(
    route_name='editor.home',
    renderer='editor/home.mako',
    permission='edit',
    )
def editor_home(request):
    userid = authenticated_userid(request)
    log.debug('editor_home: %s', userid)
    return {'userid': userid}
