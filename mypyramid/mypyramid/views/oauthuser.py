import os
from pyramid.response import Response
from pyramid.view import view_config
from mypyramid.models import DBSession, OauthUser

@view_config(route_name='oauthuser_list', renderer='../templates/oauthuser_list.pt')
def user_list(request):
    users = DBSession.query(OauthUser).all()
    return dict(users = users)
