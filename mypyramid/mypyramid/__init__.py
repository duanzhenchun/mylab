from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
 
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy            
from pyramid.security import( Allow, Everyone,Authenticated, ALL_PERMISSIONS)

from .models import DBSession, groupfinder
from mypyramid.models import USERS


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'create'),
        (Allow, 'g:editor', 'edit'),
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]
    def __init__(self, request):
        self.request = request
        
        
def main(global_config, **settings):

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        callback=groupfinder
    )
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        root_factory=Root,
    )
    config.add_static_view('static', 'static', cache_max_age=3600)

    session_factory = session_factory_from_settings(settings)
    config.include('pyramid_beaker')
    config.set_session_factory(session_factory)

    config.include('pyramid_mailer')
    config.include('pyramid_jinja2')
    
    config.add_route('home', '/')
    config.include(demo_view, route_prefix='/demo')
    config.include(reader_view)
    config.include(file_view, route_prefix='/file')
    config.include(login_view,route_prefix='/accounts')
    config.include(admin_view,route_prefix='/admin')
    config.scan()
    return config.make_wsgi_app()

def demo_view(config):
    for i in ('string','post','bar','mail','jinja',):
        config.add_route(i,'/'+i)
    config.add_route('json','/json/{foo}')
        
def file_view(config):    
    for i in ('upload','list','sample'):
        config.add_route('file.'+i,'/'+i)
    config.add_route('file.show','/show/{filename}')

def reader_view(config):
    config.add_route('reader', '/reader')
    config.add_route('worddict','/worddict')
    config.add_route('worddict.del','/worddict/{en}')

    
def login_view(config):
    for i in ('login','logout','signup'):
        config.add_route(i,'/'+i)

def admin_view(config):
    for i in ('users',):
        config.add_route(i,'/'+i)   
    config.add_route('user','/user/{login}')  
         
