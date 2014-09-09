# coding=utf-8

import traceback
import cgi, urlparse, datetime, time, re
try:
    from weibo import APIClient
except:
    pass
try:
    from crawl.weibo import APIClient
except:
    pass

from mysql_tool import get_connect
from conf import *

def tweet_url(uid, tid):
    return 'http://api.t.sina.com.cn/%s/statuses/%s' % (uid, tid)
    
def url_query_parameter(url, parameter, default=None, keep_blank_values=0):
    """Return the value of a url parameter, given the url and parameter name"""
    queryparams = cgi.parse_qs(urlparse.urlsplit(str(url))[3], \
                               keep_blank_values=keep_blank_values)
    return queryparams.get(parameter, [default])[0]

def continuation_data(db_data, timefrom=None):
    # 将数据库中获取的不连续的时间数据变成连续的
    con_data = []
    if timefrom:
        timefrom = get_datetime(timefrom, 'date', '-1')
    for dbdata in db_data:
        dbdata = list(dbdata)
        dbdata[0] = get_datetime(dbdata[0], 'date')
        gapdata = (dbdata[0] - get_datetime(timefrom, 'date')).days if timefrom else 0
        if not gapdata or gapdata == 1:
            con_data.append([dbdata[0], dbdata[1]])
            timefrom = dbdata[0]
        elif gapdata < 0:
            continue
        else:
            for day in range(1, gapdata):
                timefrom = timefrom + datetime.timedelta(days=1)
                con_data.append((timefrom, 0))
            con_data.append([dbdata[0], dbdata[1]])
            timefrom = dbdata[0]
    return con_data

def continuation_time(db_data):
    max_date = db_data[-1]
    min_date = db_data[0]
    gaps = (max_date[0] - min_date[0]).days * 24 + max_date[1] - min_date[1]
    datedict = {}
    date_tuple = list(min_date[0].timetuple()[:3])
    date_tuple.append(min_date[1])
    repost_date = datetime.datetime(*date_tuple)
    for i in range(gaps):
        datedict[(repost_date.date(), repost_date.hour)] = 0
        repost_date += datetime.timedelta(seconds=3600)
    for j in db_data:
        datedict[(j[0], j[1])] = j[2]
    date_tuple[1] -= 1
    return date_tuple, datedict
    
def get_pagenum(request):
    # 获取页码数
    try:
        page = int(request.GET.get("page", 1))
        # print('page----->',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    return page

def get_type(request):
    # 获取任务ID
    try:
        stype = int(request.GET.get("type", 0))
    except ValueError:
        stype = 0
    return stype

def fmt_create_at(create_at):
    try:
        return datetime.datetime.strptime(create_at, '%a %b %d %H:%M:%S +0800 %Y')
    except:
        #traceback.print_exc()
        return ''
        
def get_datetime(strdate, datetype='date', datediff=0):
    # 将时间 日期格式化。
    try:
        datediff = int(datediff)
    except:
        datediff = 0
    try:
        if datetype == 'date':
            if isinstance(strdate, datetime.date):
                stfdate = strdate
            else:
                stfdate = datetime.datetime.strptime(strdate, '%Y-%m-%d').date()
            if datediff: 
                return stfdate + datetime.timedelta(days=datediff)
            else: return stfdate
        if datetype == 'datetime':
            if isinstance(strdate, datetime.datetime):
                stfdate = strdate
            else:
                stfdate = datetime.datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
            if datediff: 
                return stfdate + datetime.timedelta(days=datediff)
            else: return stfdate
    except:
        return ''

def right_data(maxnum, *args):
    if not args or not maxnum:
        return []
    valid = {}
    [valid.update({i:[]}) for i in range(maxnum)]
    for first in args:
        dict1 = {}
        [dict1.update({i[0]: [int(j) for j in i[1:]]})  for i in first]
        if not dict1:
            continue
            # lenght = 1 
        else:
            lenght = len(dict1.values()[0])
        for j in valid.keys():
            if dict1.get(j):
                valid[j].extend(dict1.get(j))
            else:
                valid[j].extend([0 for n in range(lenght)])
    return sorted(valid.items(), key=lambda x: x[0])

def get_chart(trpath, path='', abstrpath=[]):
    for i, j in trpath.items():
        if j:
            abstrpath.append('+'.join([path, i]))
            # print path, '+', i
            path += '----'
            get_chart(j, path, abstrpath)
            path = '----'
        else:
            abstrpath.append(''.join([path, i]))

def loop_get_data(client, attr, attrname=None, **kargs):
    # 循环3次获取API数据
    weibotext = {}
    for i in range(3):
        try:
            weibotext = client.__getattr__(attr)(**kargs)
        except Exception, e:
            err = e.message.lower()
            if err == 'ip requests out of rate limit!':
                res = client.get.account__rate_limit_status()
                time.sleep(res.get('reset_time_in_seconds', 10))
            if err == 'user does not exists!':
                break
            time.sleep(1)
            print 'APIError: %s' % repr(e)
            if getattr(e, 'error_code', 0) == 20112 and e.message.startswith(u'Permission Denied!'):
                return client, {}
            # APIError: APIError: 20112: Permission Denied!, request: /2/statuses/show.json
            err = e.message.lower()
            if not [i for i in ['timed out', 'no json object could be decoded', 'remote service error'] if err.startswith(i)]:
                send_err_to_mail('APIError', 'APIError:  错误内容:%s 请求参数:%s token:%s api:%s' % (repr(e), repr(kargs), client.access_token, attr))
            #c = client.get.account__rate_limit_status()
            #当API次数用尽时 退出
            if err.startswith('exceed call times limited'):
                client.access_token = ''
                return client, {}
            if err in ('source paramter(appkey) is missing', 'invalid_access_token', 'expired_token'):
                # 如果使用的商业接口，不刷新token直接退出
                import sys
                sys.exit(1)
                print client.isbuss
                if client.isbuss:
                    import sys
                    sys.exit(0)
                    client.access_token = ''
                    return client, {}
                try:
                    rc_client = refresh_client()
                    if not rc_client:
                        import sys
                        sys.exit(0)
                    client = rc_client
                except Exception, e:
                    print '重新获取token失败: %s' % repr(e)
        if not attrname and weibotext:
            return client, weibotext
        try:
            weitexts = weibotext.get(attrname, '')
        except:
            weibotext = {}; weitexts = None
        if weitexts:
            return client, weibotext
    return client, weibotext
    
def get_querymid(url):
    return url.split('/')[-1].split('#')[0]

def unicode_to_str(cstr, coding='utf-8'):
    if isinstance(cstr, str):
        return cstr
    try:
        return cstr.encode(coding)
    except:
        return cstr

def send_err_to_mail(subject='', body='', to=OP_MAIL_Tos, **kwargs):
    pass
    print datetime.datetime.now(),  body
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    msg = MIMEMultipart() 
    msg['From'] = OP_MAIL_From 
    msg['Subject'] = OP_MAIL_SBUJECT + subject
    msg['To'] = ','.join(to)
    msg.attach(MIMEText(body)) 
    try:
        import base64
        smtppwd = 'kn\xbd\xdbm\xb8'
        smtp = smtplib.SMTP('smtp.cicdata.com')
        smtp.login(OP_MAIL_From, base64.encodestring(smtppwd).strip())
        smtp.sendmail(OP_MAIL_From, to, msg.as_string()) 
    except Exception, e:
        print 'send_err_to_mail error: %s' % e

def refresh_client():
    cursor = get_connect()
    re_token = get_token(cursor, 'refresh')
    re_client = APIClient(app_key=CO_APP_KEY, app_secret=CO_APP_SECRET, redirect_uri=CO_CALLBACK_URL)
    rt = re_client.refresh_access_token(re_token)
    if not rt.get('access_token'): return False
    uid, ac_token, rf_token, expires_in = rt.get('uid', -1), rt.get('access_token', ''), rt.get('refresh_token', ''), rt.get('expires_in', '')
    insert_token = '''insert into access_token set uid=%s, access_token=%s, refresh_token=%s, expires_in=%s, create_at=%s
                        on duplicate key update  access_token=%s, refresh_token=%s, expires_in=%s'''
    cursor.execute(insert_token, (uid, ac_token, rf_token, expires_in, time.time(), ac_token, rf_token, expires_in))
    cursor.connection.close()
    re_client.set_access_token(ac_token, expires_in)
    return re_client

def set_client(cursor, isbuss=False, needAuth=False, uid=''):
    domain = 'api.weibo.com'
    if isbuss:
        domain = 'c.' + domain
    client = APIClient(app_key=CO_APP_KEY, app_secret=CO_APP_SECRET,
                       redirect_uri=CO_CALLBACK_URL, domain=domain)
    client.isbuss = False
    if needAuth:
        acc_token = get_buss_token(cursor, uid)
        #acc_token = BUSINESS_TOKEN
        client.isbuss = True
    else:
        # 从数据库获取最新的token
        acc_token = get_token(cursor, 'access')
        #acc_token = ACCESS_TOKEN
    client.set_access_token(*acc_token)
    # client.get.account__rate_limit_status()
    return client

def get_token(cursor, token_type='refresh'):
    # 返回所需要的token信息
    if token_type == 'refresh':
        # 返回refresh_token 用于重新获取token
        findsql = "select create_at, refresh_token from access_token where refresh_token<>'' "
        # findsql = "select create_at, refresh_token from access_token where uid='2472274971' and refresh_token<>'' "
        cursor.execute(findsql)
        refresh = cursor.fetchall()
        if not refresh:
            return None
        refresh = sorted(refresh, key=lambda x: x[0])
        return refresh[-1][1]
    else:
        # 返回access_token用于爬取
        findsql = "select create_at, access_token, expires_in from access_token"
        # findsql = "select create_at, access_token, expires_in from access_token where uid='2472274971' "
        cursor.execute(findsql)
        access = cursor.fetchall()
        if not access:
            return ACCESS_TOKEN
        access = sorted(access, key=lambda x: x[-1])
        return access[-1][1:]
    
def get_buss_token(cursor, uid=''):
    uidstr = ''
    if uid: uidstr = 'and uid=%s'%uid
    findsql = "select access_token from " + TASKLIST_TABLE + " where access_token<>''  %s"%uidstr
    cursor.execute(findsql)
    access = cursor.fetchone()
    expires_in =  time.time() + 3600*24
    if access: return (access[0].strip(), expires_in)
    return ('', expires_in)
    
def topn_index(topn):
    dic = {}
    for i in xrange(len(topn)):
        dic[topn[i][1]] = i
    return dic
                   
def get_source(source):
        source = re.findall('<\S*a.*?>(.*?)<', source)
        if source:
            return source[0]
        return ''
    
def querymid(client, queryid, wtype=1):
        client, weiboid = loop_get_data(client, 'statuses__querymid', 'mid', id=queryid, type=wtype)
        try:
            weiboid = weiboid.get('mid')
        except:
            return None
        weiboid = None if weiboid in ['-1', -1] else weiboid
        return weiboid

def get_create_at(s):
    try:
        return datetime.datetime.strptime(s, '%a %b %d %H:%M:%S +0800 %Y')
    except:
        #traceback.print_exc()
        return ''
    
def todaytimestamp():
    td = datetime.date.today()
    return int(time.mktime(td.timetuple()))

def currenthour():
    return int(time.time()) / 3600 * 3600

def hours_ago(n):
    return (int(time.time()) / 3600 - n) * 3600
    
    
def lastweek(before=False):
    now = time.time()
    nowdate = datetime.datetime.now()
    res = datetime.datetime.fromtimestamp(int(now) / 3600 * 3600 - 
          ((7 * before + nowdate.weekday()) * 24 + nowdate.hour) * 3600)
    return res

def daysago(day, n):
    return day - datetime.timedelta(days=n)

def month_str(day=None):
    if not day:
        day = datetime.datetime.now()
    return '_'.join((str(day.year), str(day.month)))

def month_tables(start, end):
    return set([month_str(i) for i in (start, end)])
    
def sortv_iter(dic):
    for key, value in sorted(dic.iteritems(), reverse=True, key=lambda (k, v): (v, k)):
        yield key, value
        
def chunks(lst, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(lst), n):
        yield lst[i:i + n]

def benchmark(getcost=False):  # decrator arg
    def deco(f):  # func
        def _(*a, **kw):  # func args
            t = time.time()
            res = f(*a, **kw) 
            cost = time.time() - t
            print '%s %f %s' % (f.__name__, cost, 'sec')
            if getcost:
                return cost, res
            else:
                return res
        return _
    return deco

def gen_nounword(txt):
    import jieba.posseg as pseg
    words = pseg.cut(txt)
    for w in words:
        if w.flag.startswith('n'):
            yield w.word
            
def tounicode(s):
    return isinstance(s, unicode) and s or s.decode('utf-8') 

def toutf8(s):
    return isinstance(s, unicode) and s.encode('utf-8') or s 
            
if __name__ == '__main__':
    print right_data(7, [[1, 2], [2, 3], [4, 5]], [[5, 8]])
    send_err_to_mail('abc', 'bcd')
    
