#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template import Template, RequestContext
import json
import re
import word_level
from conf import *
from utils import *
from django import forms
import math

class UploadFileForm(forms.Form):
    file = forms.FileField()


def read(request, page_size=40):
    cur = get_curpage(request)
    lines = word_level.cur_txt(cur, page_size)
    txt = word_level.decorate(lines)
    allcount = len(word_level.Content)
    pagecount = int(math.ceil(allcount / (page_size * 1.0)))
    pagelist, page_range, addr = get_page_content(request, allcount, page_size, cur)
    return render_to_response('read.html', 
            {'title': 'article', 'txt': txt, 
             'addr':addr, 'pagelist':pagelist, 
             'curpage':cur, 'page_size':page_size,
             'page_range':page_range, 'pagecount':pagecount})


def fit_urlpath(fname):
    return re.match('^[\w\.]+$', fname)


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest()
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
        return process(request, test_name, tounicode(data))


def json_response(dic):
    json_response = json.dumps(dic)
    return HttpResponse(json_response, mimetype='application/json')


@benchmark
def process(request, fname, data):
    word_level.set_txt(data)
    return redirect(request.path.rsplit('/', 1)[0] + '/')

def word_mark(request):
    w, unkown, context, cur, page_size = [request.POST.get(i, '') for i in ('w', 'unkown', 'context', 'curpage', 'page_size')]
    unkown = unkown == 'true' and True or False
    if w:
        txt = word_level.updateK(w, unkown, int(cur), int(page_size))
        print txt
        return json_response({'txt': txt})


def personal(request):
    res={}
    for i,dic in word_level.personal_words():
        res[i]=dic
    return render_to_response('personal.html', 
            {'title':'personal', 'result':res})
