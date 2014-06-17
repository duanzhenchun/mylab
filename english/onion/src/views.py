#coding: utf8

import json
import re
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template import Template, RequestContext
from django import forms
from captcha.fields import CaptchaField 
import word_level
from conf import *
from utils import *


class UploadFileForm(forms.Form):
    file = forms.FileField()
    captcha=CaptchaField()

@benchmark
def read(request):
    uid = request.user.id
    print 'user:%s, uid:%d' %(request.user, uid)
    cur = get_curpage(request)
    lines = word_level.cur_txt(cur)
    pagecount = len(word_level.Content)
    pagelist, page_range, addr = get_page_content(request, pagecount, cur)
    unkowns = dict(word_level.show_unknowns(uid))
    return render_to_response('read.html', 
            {'title': word_level.title(), 
             'lines': list(word_level.decorate(lines, uid)),
             'unkown': unkowns,
             'addr':addr, 'pagelist':pagelist, 
             'curpage':cur, 
             'page_range':page_range, 'pagecount':pagecount},
             context_instance=RequestContext(request))


def fit_urlpath(fname):
    return re.match('^[\w\.]+$', fname)


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest()
        human = True
        f = request.FILES['file']
        if not fit_urlpath(f.name):
            return HttpResponseBadRequest('file name should only contaions alpha, num, or _')
        elif f.size > UPLOAD_LIMIT:
            return HttpResponseBadRequest('file size too big: ' + str(f.size))
        else:
            return process(request, f.name, f.read())
    else:
        return render_to_response('upload.html', {'form': UploadFileForm},
                                  context_instance=RequestContext(request))


@benchmark
def upload_txt(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    data = request.POST.get('content', '')
    test_name = request.POST.get('test_name', '')
    if not data.strip():
        return HttpResponseBadRequest(data)
    elif not test_name or not fit_urlpath(test_name):
        return HttpResponseBadRequest('file name should only contaions alpha, num, or _')
    elif len(data) > UPLOAD_LIMIT:
        return HttpResponseBadRequest('Error: file size too big: ' + len(data))
    else:
        return process(request, test_name, data)


def json_response(dic):
    json_response = json.dumps(dic)
    return HttpResponse(json_response, mimetype='application/json')


@benchmark
def process(request, fname, data):
    word_level.set_article(fname, data)
    return redirect(request.path.rsplit('/', 1)[0] + '/')


@benchmark
def word_mark(request):
    uid = request.user.id
    w, unkown, context, cur = [request.POST.get(i, '') for i in ('w', 'unkown', 'context', 'curpage' )]
    w = w.strip()
    unkown = unkown == 'true' and True or False
    if w:
        lines = list(word_level.updateK(w, unkown, int(cur), uid))
        return json_response({'lines': lines})


@benchmark
def mywords(request):
    res={}
    for i,dic in word_level.mywords(request.user.id):
        res[i]=dic
    return render_to_response('mywords.html', 
            {'title':'mywords', 'result':res })


@benchmark
def word_repeat(request):
    uid = request.user.id
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    w = request.POST.get('w').strip()
    word_level.repeat(w, uid)
    return json_response(dict(word_level.show_unknowns(uid)))
