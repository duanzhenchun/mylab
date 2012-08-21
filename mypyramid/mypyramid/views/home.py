from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import forbidden_view_config

### INITIALIZE MODEL
USERS = {}
FILES = {}
    
@view_config(route_name='home', renderer='home.jinja2')
def home_view(request):
    login = authenticated_userid(request)
    user = USERS.get(login)
    return {
        'user': user,
        'user_user_files': [p for (t, p) in FILES.iteritems() if p.owner == login],
    }
    
