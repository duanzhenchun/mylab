#encoding:utf-8

import os
import logging
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import (HTTPFound, HTTPForbidden)
from tools_0 import *

#import  mypyramid.word_dic
from word_dic.auto_index  import find_dicmatch
#from mypyramid.word_dic.tools import to_unicode

filestore = 'store'
g_worddic = getdic(filestore + '/sorted_en')

@view_config(route_name='upload', http_cache=3600, request_method='GET', renderer="upload.jinja2")
def get_upload(request):
#    owner = authenticated_userid(request)
#    if owner is None:
#        raise HTTPForbidden()
    return {}

#@view_config(route_name='upload', permission='create', request_method='POST')
@view_config(route_name='upload', request_method='POST', renderer="upload.jinja2")
def upload(request):
    from word_dic.genwords import gen_single_enf, gen_singlef
    name = 'enfile'
    fname = request.POST[name].filename
    enf = request.POST[name].file
    endic, modi_ens = gen_single_enf(enf)
    name = 'csfile'
    fname = request.POST[name].filename
    csf = request.POST[name].file
    csdic = gen_singlef(csf)
#    upload_file(fname,fin)
    res = find_dicmatch(endic, modi_ens, csdic, enf, csf)
    return {'result': txt2html(res)}

#    return HTTPFound(location = request.route_url('file.show', filename=fname))

def write_file(fname, fin):
    fpath = getabspath(safe_join(filestore, fname))
    fout = open(fpath, 'wb')
    # write file
    fin.seek(0)
    while 1:
        data = fin.read(2 << 16)
        if not data:
            break
        fout.write(data)
    fout.close()
    return {}


@view_config(route_name='file.list', renderer="file/list.jinja2")
def file_list(request):
    import glob
    folder = getabspath(filestore)
    files = glob.glob('%s/*.txt' % folder)
    fnames = map(lambda s:s.split('/')[-1], files)
    print fnames
    lst = [ {'name':i, 'href':request.route_url('file.show', filename=i)} for i in fnames]
    return {'files':lst}

def redirectpage(request, fname, index):
        url = request.route_url('file.show', filename=fname)
        url += '?page=%d' % index
        return HTTPFound(url)

import os
@view_config(route_name='file.show', http_cache=3600, renderer="reader.jinja2")
def file_view(request):
    fname = request.matchdict['filename']
    pageindex = request.params.get('page')
    if not pageindex:
        return redirectpage(request, fname, 0)

    fpath = getabspath(os.path.join(filestore, fname))
    logging.debug(fpath)
    pageindex = int(pageindex)
    if pageindex < 0:
        return redirectpage(request, fname, getlastpage(fpath))
    try:
        txt = getpage(fpath, pageindex)
    except OutpageException, e:
        return redirectpage(request, fname, e.pagenum)

    txt = to_unicode(txt)
    global g_worddic
    dicref = request.route_url('file.worddict')
    txt = dicsub(g_worddic, txt, dicref)
    txt = txt2html(txt)
    return {
        'file':{'name':fname, 'text':txt, 'curpage':pageindex}
        }

@view_config(route_name='file.sample')
def sample(request):
    return redirectpage(request, 'sample.txt', 0)

