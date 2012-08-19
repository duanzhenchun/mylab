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
    logging.info(fpath)
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
        
@view_config(route_name='worddict',request_method='POST',renderer='string') 
def edit_word(request):
    cs, en = [request.params[i] for i in ('cs','en')]
    global g_worddic
    if en in g_worddic:
        g_worddic[en]=cs
    else:
        olden = find_key(g_worddic,cs)
        if olden:
            del g_worddic[olden]
        g_worddic[en]=cs
    return "OK"
    
@view_config(route_name='worddict.del',request_method='DELETE',renderer='string') 
def delete_word(request):
    en = request.matchdict['en']
    global g_worddic
    del g_worddic[en]
    return "OK"
    
            
"""      
@view_config(route_name='edit_word', renderer='edit_word.jinja2')
def edit_word(request):
    word = request.matchdict['word']
    if 'form.submitted' in request.params:
        global g_worddic
        word.cs = request.params['cs']
        word.en = request.params['en']
        g_worddic[word.cs] = word.en
        return HTTPFound(location = request.route_url('view_word',
                                                      word=word))
    return dict(
        page=page,
        save_url = request.route_url('edit_word', word=word),
        )
      
@view_config(route_name='add_word', renderer='edit_word.jinja2')
def add_word(request):
    if 'form.submitted' in request.params:
        return edit_word(request)
        
    word = request.matchdict['word']   
    save_url = request.route_url('add_word', word=name)
    word = {'cs':'', 'en':''}
    return dict(word=word, save_url=save_url)
    
    
@view_config(route_name='view_word', renderer='view_word.jinja2')
def view_word(request):
    word = request.matchdict['word'] 
    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page is None:
        return HTTPNotFound('No such page')

    content = publish_parts(page.data, writer_name='html')['html_body']
    content = wikiwords.sub(check, content)
    edit_url = request.route_url('edit_page', pagename=pagename)
    return dict(page=page, content=content, edit_url=edit_url,
                logged_in=authenticated_userid(request))
                
                """
