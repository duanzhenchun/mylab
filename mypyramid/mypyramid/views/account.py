from pyramid.view import view_config
from pyramid.security import (authenticated_userid, forget, remember)
from pyramid.view import forbidden_view_config
from pyramid.httpexceptions import (HTTPFound,HTTPForbidden)
from mypyramid.models import User, USERS

FILES = {}

@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    login = authenticated_userid(request)
    user = USERS.get(login)
    return {
        'user': user,
        'user_user_files': [p for (t, p) in FILES.iteritems() if p.owner == login],
    }

@forbidden_view_config()
def forbidden_view(request):
    """user 'next' query parameter to redirect back, after login successfully
    """
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)
    
    
@view_config(route_name='login',renderer='login.mako')
def login(request):
    next = request.params.get('next') or request.route_url('home')
    login = ''
    did_fail = False
    if 'submit' in request.POST:
        login = request.POST.get('login', '')
        passwd = request.POST.get('passwd', '')
        user = USERS.get(login, None)
        if user and user.check_password(passwd):
            headers = remember(request, login)
            return HTTPFound(location=next, headers=headers)
        did_fail = True

    return {
        'login': login,
        'next': next,
        'failed_attempt': did_fail,
        'users': USERS,
    }
    
@view_config(route_name='logout',)
def logout(request):
#    session = request.session
#    session.invalidate()
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)
