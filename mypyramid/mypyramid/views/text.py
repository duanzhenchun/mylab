import os
import logging
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from tools import *

filestore='store'

@view_config(route_name='upload', request_method='GET',renderer="upload.jinja2")
def get_upload(request):
    return {}
    
@view_config(route_name='upload', request_method='POST')
def upload(request):
    fname = request.POST['text'].filename
    fin = request.POST['text'].file
    fpath = getabspath(os.path.join(filestore, fname))
    fout = open(fpath, 'wb')
    # write file
    fin.seek(0)
    while 1:
        data = fin.read(2<<16)
        if not data:
            break
        fout.write(data)
    fout.close()
    return HTTPFound(location = request.route_url('show', filename=fname))

     
@view_config(route_name='list', renderer="file_list.jinja2")        
def file_list(request):
    dummy = ('1.txt','2.txt')
    lst=[ {'name':i,'href':os.path.join(filestore, i)} for i in dummy]
    return {'files':lst}
        
import os
@view_config(route_name='show', http_cache=3600, renderer="show_text.jinja2")
def text_view(request):
    fname = request.matchdict['filename']
    fpath = getabspath(os.path.join(filestore, fname))
    fin = open(fpath, 'r')
    txt = to_unicode(open(fpath, 'r').read())
    global g_worddic
    dicref = request.route_url('worddict')
    txt = dicsub(g_worddic,txt,dicref)
    txt = txt2html(txt)
    return {
        'file':{'name':fname, 'text':txt}
        }
        
@view_config(route_name='sample',http_cache=3600, renderer="show_text.jinja2")
def sample(request):
    request.matchdict['filename']='sample.txt'
    return text_view(request)
#    response = Response(content_type='text/plain')
#    response.app_iter = fin
#    return response

g_worddic=getdic(filestore +'/sorted_en')
    
@view_config(route_name='worddict', renderer="show_text.jinja2")        
def wordict_view(request):
    global g_worddic
    txt=''
    for k,v in sorted(g_worddic.iteritems()):
        txt += '%s:\t%s\n' %(k,v)
    txt = txt2html(txt)
    return {
        'file':{'name':'worddict', 'text':txt}
        }
        
