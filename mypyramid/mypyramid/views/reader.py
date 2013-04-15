#encoding:utf-8

import os
import logging
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import (HTTPFound, HTTPForbidden)
from tools_0 import *

filestore = 'store'
g_worddic = getdic(filestore + '/sorted_en')
pagesize = 5500


@view_config(route_name='reader', http_cache=3600, request_method='GET', renderer="reader.jinja2")
def get_text(request):
    fname = 'sample.txt'
    fpath = getabspath(safe_join(filestore, fname))
    txt = open(fpath, 'r').read()
    userid = None
    print request.session
    if 'userid' in request.session:
        userid = request.session['userid']
    print 'aaa', authenticated_userid(request)
    return {
        'file':{'name':fname, 'text':trans(txt, request), },
        'logged_in': userid #authenticated_userid(request),
        }

def trans(txt, request):
    txt = to_unicode(txt)
    global g_worddic
    dicref = request.route_url('worddict')
    txt = dicsub(g_worddic, txt, dicref)
    txt = txt2html(txt)
    return txt

@view_config(route_name='reader', http_cache=3600, request_method='POST', renderer="string")
def post_text(request):
    fname = request.params['fname']
    txt = request.params['txt']
    if len(txt) > pagesize:
        raise "upload txt too long";
    return trans(txt, request)


@view_config(route_name='worddict', renderer="reader.jinja2")
def wordict_view(request):
    global g_worddic
    txt = ''
    for k, v in sorted(g_worddic.iteritems()):
        txt += '%s:\t%s\n' % (k, v)
    txt = txt2html(txt)
    return {
        'file':{'name':'worddict', 'text':txt},
        'logged_in': authenticated_userid(request),
        }

@view_config(route_name='worddict',
    request_method='POST',
    permission='edit',
    renderer='string'
)
def edit_word(request):
    logging.debug(request.client_addr)
    cs, en = (request.params[i] for i in ('cs', 'en'))
    global g_worddic
    if en in g_worddic:
        g_worddic[en] = cs
    else:
        olden = find_key(g_worddic, cs)
        if olden:
            del g_worddic[olden]
        g_worddic[en] = cs
    return "OK"

@view_config(
    route_name='worddict.del',
    request_method='DELETE',
    permission='edit',
    renderer='string'
)
def delete_word(request):
    en = request.matchdict['en']
    global g_worddic
    del g_worddic[en]
    return "OK"
