from pyramid.response import Response
from pyramid.view import view_config
import logging

@view_config(route_name='json',renderer="json")
def json_view(request):
    foo = request.matchdict['foo']
    return {'json':foo}

@view_config(route_name='string',renderer="string") 
def string_view(request):
    logging.info('string view')
    #print request.json_body
    return 'string'    
    
@view_config(route_name='post',request_method='POST',renderer="json") 
def post_view(request):
    dic = {}
    for i in ('a','b'):
        dic[i]=request.params[i]
    return dic
    
@view_config(route_name='bar')
def route_accepts(request):
    introspector = request.registry.introspector
    route_name = request.matched_route.name     #'bar'
    route_intr = introspector.get('routes', route_name)
    print route_intr
    return Response(str(route_intr['pattern']))
    
@view_config(route_name='mail')
def test_mail(request):
    from pyramid_mailer import get_mailer
    from pyramid_mailer.message import Message
    mailer = get_mailer(request)
    message = Message(subject="hello world",
                      sender="whille@163.com",
                      recipients=["whille@163.com"],
                      body="hello, arthur")
    mailer.send(message)                  
    #mailer.send_to_queue(message)
    return Response('ok')

@view_config(route_name='jinja', renderer='test.jinja2')    
def test_jinja(request):
    return {'foo':1, 'bar':3}

    

