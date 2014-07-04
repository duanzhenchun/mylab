#coding: utf8

import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template import Template, RequestContext
from django import forms
from captcha.fields import CaptchaField 
import word_level
from conf import *
from utils import *


pagesize=4000


def read(request):
    uid = request.user.id
    if request.method == 'GET':
        return render_to_response('read.html', context_instance=RequestContext(request))
    elif request.method == 'POST':
        fname, txt, curpage = [request.POST.get(i, '') for i in ('fname', 'txt', 'curpage')]
        if len(txt) > pagesize:
            return json_response({'error':'page size too long'})
        word_level.set_lastpage(fname, curpage, uid) 
        dic = {'title':fname,
               'article': article_html(word_level.decorate(to_lines(txt), uid)),
              }     
        return json_response(dic)


def lastpage(request):
    fname = request.GET.get('fname', '')
    last = word_level.lastpage(fname, request.user.id)
    return json_response({'last':last})

def article_html(lines):
    res = ''
    for line in lines:
        res +="<p class='p_txt'>%s</p>" %line
    return res

def word_html(dic, wtype):
    res=''
    for k,v in dic.iteritems():
        res += "<div><span class='wl_%s %s' >%s</span> " %(v[1], wtype, k)
        if wtype == 'unknown_word':
            res += "<span class='dt'>%s</span></div><div>%s</div></br>" %( fmt_timestamp(v[2]), v[0])
        else:
            res += "</div><div>%s</div></br>" %v[0]
    return res

def json_response(dic):
    json_response = json.dumps(dic)
    return HttpResponse(json_response, mimetype='application/json')


def word_change(request):
    uid = request.user.id
    w, unknown, txt = [request.POST.get(i, '') for i in ('w', 'unknown', 'txt')]
    w = w.strip()
    unknown = (unknown == 'true') and True or False
    if w:
        lines = list(word_level.updateK(w.strip(), unknown, txt, uid))
        return json_response({'lines': lines})


def word_unknown(request):
    return render_to_response('mywords.html', 
            {'dic': word_level.unknowns(request.user.id )
            },
            context_instance=RequestContext(request))

def word_rescue(request):
    uid = request.user.id
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    w, yn = (request.POST.get(i) for i in ('w', 'yn'))
    w=w.strip()
    yn = (yn == 'true') and True or False
    if w:
        word_level.rescue(w, uid, yn)
    dic = dict(word_level.show_forgotten(uid))
    return json_response({'forgotten': word_html(dic, 'forgotten_word'),
                         })

def word_repeat(request):
    uid = request.user.id
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    w = request.POST.get('w').strip()
    if w:
        word_level.repeat(w, uid)
    dic = dict(word_level.show_unknowns(uid))
    return json_response({'wait': word_level.time2wait(uid),
                         'unknown': word_html(dic, 'unknown_word'),
                         })
