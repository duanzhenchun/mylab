from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
 
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy            

from .models import (
    DBSession,
    Base,
    groupfinder,
    )

import logging
log = logging.getLogger(__name__)


def main(global_config, **settings):

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    authn_policy = AuthTktAuthenticationPolicy(
        #settings['auth.secret'],
		settings['persona.secret'],
        callback=groupfinder
    )
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        root_factory='mypyramid.models.RootFactory',
    )
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
            
    config.include('pyramid_beaker')
    config.include('pyramid_mailer')
    config.include('pyramid_jinja2')
    config.include('pyramid_persona')
    
    ## Velruse Auth
    #config.include('velruse.providers.facebook')
    config.include('velruse.providers.twitter')
    
#    setprovider(config,**settings)    
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('velruse_login','/login') 
    config.add_route('logout','/logout') 
    config.add_route('editor.home', '/editor')
    config.add_route('oauthuser_list', '/oauth/')
    config.add_route('favicon', '/favicon.ico')
    config.include(reader_view)
    config.include(file_view, route_prefix='/file')
    config.scan()
    return config.make_wsgi_app()

def file_view(config):    
    for i in ('upload','list','sample'):
        config.add_route('file.'+i,'/'+i)
    config.add_route('file.show','/show/{filename}')


def reader_view(config):
    config.add_route('reader', '/reader')
    config.add_route('worddict','/worddict')
    config.add_route('worddict.del','/worddict/{en}')
    config.add_route('upload', '/upload')
    
            
#def setprovider(config, **settings):
#    # determine which providers we want to configure
#    providers = settings.get('login_providers', '')
#    providers = filter(None, [p.strip()
#                              for line in providers.splitlines()
#                              for p in line.split(', ')])
#    settings['login_providers'] = providers
#    if not any(providers):
#        log.warn('no login providers configured, double check your ini '
#                 'file and add a few')

#    if 'douban' in providers:
#        config.include('velruse.providers.douban')
#        config.add_douban_login_from_settings(prefix='douban.')
#        
#    if 'taobao' in providers:
#        config.include('velruse.providers.taobao')
#        config.add_taobao_login_from_settings(prefix='taobao.')
#        
#    if 'facebook' in providers:
#        config.include('velruse.providers.facebook')
#        config.add_faceoauthuser_login_from_settings(prefix='facebook.')
#        
#    if 'github' in providers:
#        config.include('velruse.providers.github')
#        config.add_github_login_from_settings(prefix='github.')

#    if 'twitter' in providers:
#        config.include('velruse.providers.twitter')
#        config.add_twitter_login_from_settings(prefix='twitter.')

#    if 'live' in providers:
#        config.include('velruse.providers.live')
#        config.add_live_login_from_settings(prefix='live.')

#    if 'bitbucket' in providers:
#        config.include('velruse.providers.bitbucket')
#        config.add_bitbucket_login_from_settings(prefix='bitbucket.')

#    if 'google' in providers:
#        config.include('velruse.providers.google')
#        config.add_google_login(
#            realm=settings['google.realm'],
#            consumer_key=settings['google.consumer_key'],
#            consumer_secret=settings['google.consumer_secret'],
#        )

#    if 'yahoo' in providers:
#        config.include('velruse.providers.yahoo')
#        config.add_yahoo_login(
#            realm=settings['yahoo.realm'],
#            consumer_key=settings['yahoo.consumer_key'],
#            consumer_secret=settings['yahoo.consumer_secret'],
#        )   
