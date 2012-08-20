from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
            
from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
            
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    session_factory = session_factory_from_settings(settings)
    config.include('pyramid_beaker')
    config.set_session_factory(session_factory)

    config.include('pyramid_mailer')
    config.include('pyramid_jinja2')
    
    config.add_route('home', '/')
    config.include(demo_view, route_prefix='/demo')
    config.include(text_view, route_prefix='/text')
    config.scan()
    return config.make_wsgi_app()

def demo_view(config):
    for i in ('string','post','bar','mail','jinja',):
        config.add_route(i,'/'+i)
    config.add_route('json','/json/{foo}')
        
def text_view(config):    
    for i in ('upload','list','worddict'):
        config.add_route(i,'/'+i)
    config.add_route('worddict.del','/worddict/{en}')
    config.add_route('show','/show/{filename}')
