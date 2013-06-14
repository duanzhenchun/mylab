#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
import json, itertools, urlparse
import DB

def home(request):
    return HttpResponse('OK')

def init_view(request):
    return HttpResponse(DB.Cli.new_uid())
    
import json
def json_response(dic):
    json_response = json.dumps(dic)
    return HttpResponse(json_response, mimetype='application/json')

def businfo(request):
    return [ request.POST.get(i) for i in ('uid', 'busnum', 'direct', 'loc')]

def feed_view(request):
    info = businfo(request)
    DB.Cli.set(info + ['feed'])
    res = DB.Cli.getall(info[1], info[2], 'need')
    return json_response(res)

def need_view(request):
    info = businfo(request)
    DB.Cli.set(info)
    res = DB.Cli.getall(info[1], info[2], 'feed')
    return json_response(res)
        
def need_over(request):
    info = businfo(request)
    DB.Cli.remove(info)
    #log 
    return HttpResponse('OK')

def feed_over(request):
    info = businfo(request)
    DB.Cli.remove(info + ['feed'])
    return HttpResponse('OK')
    
def getbest(need):
    k = ':'.join(need[:2])
    best = min(choice in Routes.get(k, []) + [MAX_DIS], key=distance)
    return best
        
def distance(p1, p2):    
    return ((p1[0] - p1[0]) ** 2 + (p1[1] - p1[1]) ** 2) ** .5

MAX_DIS = 10 ** 7
