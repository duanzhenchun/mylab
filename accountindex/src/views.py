#coding=utf-8


from django.http import HttpResponse
from django.shortcuts import render_to_response
import json
from utils import get_connect
from src.execl import write_excel

def json_response(dic):
    json_response = json.dumps(dic)
    return HttpResponse(json_response, mimetype='application/json')


def home(request):
    cursor = get_connect()
    sqlcmd = 'select DISTINCT(`day`)  from report  ORDER BY day desc'
    cursor.execute(sqlcmd)
    res = cursor.fetchall()
    return render_to_response('tasklist.html', {'rows':res})
    
def download(request):
    #下载分析结果
    taskcontent = request.POST.get('taskcontent', '')
    filename = taskcontent+'.xls' if taskcontent else 'result.xls'
    response = HttpResponse(mimetype="applicationnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    if taskcontent:
        cursor = get_connect()
        sql = '''select b.screen_name, a.* from report a join tasklist b on a.uid=b.uid where a.day=%s'''
        cursor.execute(sql, (taskcontent, ))
        res = cursor.fetchall()
        if res:
            wb = write_excel(res)
            wb.save(response)
    return response
    
def chart(request):
    words = [['Grand Prix', 1864], ['Singapore Grand Prix', 1219], ['Vettel', 851], ['Sebastian', 633], ['Formula', 605], ['Alonso', 482], ['Ferrari', 442], ['Fernando', 358], ['Christian Horner', 354], ['Rosberg', 318], ['pole position', 283], ['Mercedes', 281], ['Webber', 271], ['Hamilton', 266], ['Romain Grosjean', 251], ['Raikkonen', 229], ['chequered flag', 198], ['principal Christian Horner', 197], ['Nico', 191], ['championship leader Sebastian', 182], ['Marina', 181], ['practice session', 135], ['start-to-finish win', 133], ['Lotus', 122], ['championship', 120], ['fourth-straight championship', 119], ['McLaren', 112], ['German', 110], ['team principal Eric', 109], ['consecutive Formula', 104], ['threatening Raikkonen', 99], ['team principal', 94], ['pair Jenson Button', 93], ['Grand Prix victory', 91], ['qualifying session', 90], ['Massa', 85], ['team-mate Lewis Hamilton', 82], ['spot-lit Marina Bay', 82], ['Malaysian Grand Prix', 78]]
    return render_to_response('charts.html', {'words': words})
