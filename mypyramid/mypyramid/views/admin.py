from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from mypyramid.models import USERS

@view_config(
    route_name='users',
    permission='admin',
    renderer='users.mako',
)
def users_view(request):
    return {
        'users': sorted(USERS.keys()),
    }

@view_config(
    route_name='user',
    permission='admin',
    renderer='user.mako',
)
def user_view(request):
    login = request.matchdict['login']
    user = USERS.get(login)
    if not user:
        raise HTTPNotFound()

    files=[]
#    files = [p for (t, p) in FILES.iteritems() if p.owner == login]

    return {
        'user': user,
        'pages': files,
    }


