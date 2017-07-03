#coding=utf-8
import os
import sys
import ast
import copy
from dateutil.relativedelta import relativedelta
sys.path.insert(0, os.path.split(os.getcwd())[0])
sys.path.insert(0, os.path.split(os.path.split(os.getcwd())[0])[0])
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
try:
    from django.db import IntegrityError, transaction
except:
    pass
from utils import *

FANNUM_DISTRIBUTION = [10, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000]

def fan_growth(uid, start, end):
    #因为查询的是fans_trend表 只有几个有商业接口的才有数据。这里要另外加张表统计粉丝增长
    fansdata = fan_num(uid, start)
    start_fans, end_fans = (0, 0)
    if fansdata:
        start_fans = fansdata[0][0]
        for i in fansdata:
            if i[1] > end and end_fans:
                break
            end_fans = i[0]
    growth = end_fans - start_fans
    if start_fans == 0:
        growthp = end_fans > 0 and TOP_LIMIT or 0
    else:
        growthp = float(growth) / start_fans
    return end_fans, growth, growthp

def fan_num(uid, start):
    cmd = 'select followers_count, day from %s where uid=%s and day>="%s" order by day'%(ACCOUNT_GROWTH_TABLE, uid, start)
    return get_DB(cmd)

def tweets_stat(uid, start, end):
    cursor = get_connect()
    cmd = 'select reposts_count, comments_count, attitudes_count from ' + ACCOUNT_TWEET_TABLE + \
             ' where uid= %s and ' % uid + time_between('date(created_at)', start, end)
    cursor.execute(cmd)
    tweets = cursor.fetchall()
    attitudes_count = sum([i[0] for i in tweets])
    dic = {}
    for table in month_tables(start, end):
        cmd = 'select tasktype, count(1) from %s where src_uid=%s and ' \
            % (INTERACT_TABLE + table, uid) + time_between('date(created_at)', start, end) + \
            ' group by tasktype'
        res = get_DB(cmd)
        for tasktype, count in res:
            dic.setdefault(tasktype, 0)
            dic[tasktype] += count
    cursor.connection.close()
    return len(tweets), dic.get('reposts', 0), dic.get('comments', 0), attitudes_count

def directat_num(uid, start, end):
    cmd = 'select count(1) from %s ' % DIRECTAT_TABLE + \
          ' where target_uid=%s and ' % uid + \
          time_between('date(created_at)', start, end)
    return get1_DB(cmd)

def exposure_num(uid, start, end):
    cmd = 'select sum(exposure_count) from %s ' % EXPOSURE_TALBE + \
          ' where uid = %s and ' % uid + time_between('date(day)', start, end)
    return get1_DB(cmd)

def er_nday(uid, ndays, end):
    """
    (retweet+comment+direct @)/tweet number/fans number of past 30 days
    2014-2-17 change to
    (retweet+comment+direct @+attitudes)/tweet number/fans number of past 30 days
    """
    start = daysago(end, ndays-1)
    nfan = fan_num(uid, end)
    nfan = nfan[0][0] if nfan else 0
    nt, nret, ncmt, natt = tweets_stat(uid, start, end)
    nat = directat_num(uid, start, end)
    if nt == 0 or nfan == 0:
        er = 0
    else:
        er = float(nret + ncmt + nat + natt) / nt / nfan
    return er

def top_hashtags(n, uid, start, end):
    tops = topn.TopN(n)
    cmd = 'select hashtag, reposts_count, comments_count, followers_count ' + \
           ' from %s where hashtag<>"" and uid = %s and ' % \
            (ACCOUNT_TWEET_TABLE, uid) + time_between('date(created_at)', start, end)
    tweets = get_DB(cmd)
    dic = {}
    for hashtag, nret, ncmt, nfan in tweets:
        er = float(nret + ncmt) / nfan
        dic.setdefault(hashtag, [])
        dic[hashtag].append(er)
    for k, ers in dic.iteritems():
        average = sum(ers) * 1.0 / len(ers)
        tops.feed((average, k))
    res = tops.result()
    return res

def top_posts(n, uid, start, end):
    tops = topn.TopN(n)
    dic = {}
    for table in month_tables(start, end):
        cmd = 'select src_id, tasktype, count(1) from %s where uid<>src_uid and src_uid=%s and ' \
            % (INTERACT_TABLE + table, uid) + time_between('date(created_at)', start, end) + \
            ' group by src_id, tasktype'
        res = get_DB(cmd)
        for tid, tasktype, count in res:
            dic.setdefault(tid, {tasktype : 0})
            try:
                dic[tid][tasktype]
            except:
                dic[tid][tasktype] = 0
            dic[tid][tasktype] += count
    '''
    cmd = 'select tid, reposts_count, comments_count, followers_count from %s where uid = %s and ' % \
            (ACCOUNT_TWEET_TABLE, uid) + time_between('date(created_at)', start, end)
    tweets = get_DB(cmd)
    '''
    nfan = fan_growth(uid, start, end)[0]
    for tid, v in dic.iteritems():
        er = float(sum(v.values())) / nfan
        tops.feed((er, {'url':tweet_url(uid, tid), 'nret':v.get('reposts', 0), 'ncmt':v.get('comments', 0)}))
    res = tops.result()
    return res

def top_influencers(n, target_uid, start, end):
    tops = topn.TopN(n)
    dic = {}
    for table in month_tables(start, end):
        cmd = 'select uid, tasktype, count(tasktype) from %s where uid<>src_uid and src_uid=%s and ' \
            % (INTERACT_TABLE + table, target_uid) + time_between('date(created_at)', start, end) + \
            ' group by uid, tasktype'
        res = get_DB(cmd)
        for uid, tasktype, count in res:
            dic.setdefault(uid, {tasktype : 0})
            try:
                dic[uid][tasktype]
            except:
                dic[uid][tasktype] = 0
            dic[uid][tasktype] += count
    cmd = 'select uid, count(uid) from %s  where target_uid=%s and '\
         % (DIRECTAT_TABLE, target_uid) + \
          time_between('date(created_at)', start, end) + ' group by uid'
    res = get_DB(cmd)
    for uid, count in res:
        dic.setdefault(uid, {})
        dic[uid]['direct_at'] = count
    for uid, v in dic.iteritems():
        f = sum(v.values())
        v['uid'] = uid
        tops.feed((f, v))
    res = tops.result()
    return res

def time_between(field, start, end):
    return ' (%s between "%s" and "%s")' % (field, start, end)

def get1_DB(cmd):
    cursor = get_connect()
    cursor.execute(cmd)
    res = cursor.fetchone()
    cursor.connection.close()
    return res and res[0] or 0

def get_DB(cmd):
    cursor = get_connect()
    cursor.execute(cmd)
    res = cursor.fetchall()
    cursor.connection.close()
    return res

def response(uid, start, end):
    cmd = 'select count(1) from %s ' % DIRECTAT_TABLE + \
          ' where target_uid=%s and is_question=1 and' % uid + \
          time_between('date(created_at)', start, end)
    allnum = get1_DB(cmd)
    rescmd = 'select (response_time-created_at) from %s ' % DIRECTAT_TABLE + \
            'where target_uid=%s and response_time is not null  and  ' % uid + time_between('date(created_at)', start, end)
    resps = get_DB(rescmd)
    respnum = len(resps)
    mean = respnum > 0 and sum([i[0] for i in resps]) / respnum or 0.0
    return allnum, respnum, mean

def fan_active(uid, day):
    cmd = 'select %s,%s,%s from %s where uid=%s and day="%s"' % \
        ('active_follower', 'loyal_follower', 'follower_count', FANS_TREND, uid, day)
    cursor = get_connect()
    cursor.execute(cmd)
    res = cursor.fetchone()
    cursor.connection.close()
    act, interact, total = res and res or (0, 0, 0)
    res = 0.0, 0.0
    if total > 0:
        res = act * 1.0 / total, interact * 1.0 / total
    return res

def fans_day_activity(uid, ndayago=1):
    #根据时间修改表名
    day = daysago(datetime.date.today(), ndayago)
    cmd = 'select hour(created_at) from ' + INTERACT_TABLE + month_str(day) + \
          ' where src_uid=%s and date(created_at)=%s'
    cursor = get_connect()
    try:
        cursor.execute(cmd, (uid, day))
        res = cursor.fetchall()
    except:
        res = []
    hour_dist = [0, ] * 24
    for t in res:
        hour_dist[t[0]] += 1
    #统计每个小时有企业账号发了多少篇微博
    cmd = 'select hour(created_at), count(1) from %s ' % ACCOUNT_TWEET_TABLE + \
                  ' where uid=%s and date(created_at)=%s GROUP BY hour(created_at)'
    cursor.execute(cmd, (uid, day))
    res = cursor.fetchall()
    postnum = {}
    if res: [postnum.update({r[0]:r[1]}) for r in res]
    for i in range(len(hour_dist)):
        dic = {'hour':i, 'weekday':day.weekday(), 'ori_postnum':postnum.get(i, 0),
               'day':day, 'uid':uid, 'count': hour_dist[i],
             }
        insertDB(cursor, FANS_ACTIVITY_TABLE, dic, True, ('uid', 'day', 'hour'))
    cursor.connection.close()

def insertDB(cursor, tablename, dic, update=False, privatekeys=None):
    cmd = 'insert into %s (%s) value (%s) ' % (tablename,
                ','.join(dic.keys()), ','.join(('%s',) * len(dic)))
    if update and privatekeys:
        dic2 = copy.deepcopy(dic)
        for k in privatekeys:
            dic2.pop(k)
        s = ', '.join(['%s' % k + '=%s' for k in dic2])
        cmd += 'on duplicate key update %s' % s
    dataexist = False
    try:
        if update:
            cursor.execute(cmd, dic.values() + dic2.values())
        else:
            cursor.execute(cmd, dic.values())
        cursor.connection.commit()
        transaction.commit_unless_managed()
    except (MySQLdb.IntegrityError, IntegrityError):
        dataexist = True
        cursor.connection.rollback()
        transaction.rollback_unless_managed()
    except Exception, e:
        traceback.print_exc()
        print 'insert db error. e:%s, dic: %s' % (e, str(dic))
        cursor.connection.rollback()
        transaction.rollback_unless_managed()
    return dataexist

def distri_pos(n, lst):
    for i in xrange(len(lst)):
        if n < lst[i]:
            return i
    return len(lst)

def percent(lst):
    res = None
    if sum(lst) == 0:
        res = (0,) * len(lst)
    else:
        res = map(lambda x:float(x) / sum(lst), lst)
    return res

V_TYPES = ['normal', 'verified', 'daren']
def get_vtype(n):
    n = int(n)
    return (n >= 0, n >= 200).count(True)

def newfan_dist(uid, start, end):
    v_dist = [0, ] * len(V_TYPES)
    subfan_dist = [0, ] * (len(FANNUM_DISTRIBUTION) + 1)
    prov_dist = {}
    gender_dist = {}
    tag_dist = {}
    for table in month_tables(start, end):
        cmd = 'select verified_type, province, followers_count, tags, gender from %s where src_uid=%s and '\
             % (FANS_TABLE + table, uid) + time_between('follow_time', start, end)
        fans = get_DB(cmd)
        for vtype, province, follownum, tags, gender in fans:
            v_dist[get_vtype(vtype)] += 1
            prov_dist.setdefault(province, 0)
            prov_dist[province] += 1
            for tag in tags.split(','):
                if not tag:
                    continue
                tag_dist.setdefault(tag, 0)
                tag_dist[tag] += 1
            subfan_dist[distri_pos(follownum, FANNUM_DISTRIBUTION)] += 1
            gender_dist.setdefault(gender, 0)
            gender_dist[gender] += 1
    return v_dist, subfan_dist, top_distribution(prov_dist, 10, False), \
        top_distribution(gender_dist, len(gender_dist), False), \
        top_distribution(tag_dist, 10, False)
#     return percent(v_dist), percent(subfan_dist), top_distribution(prov_dist, 10), \
#            top_distribution(gender_dist, len(gender_dist)), top_distribution(tag_dist, 10)

# AGE_DISTRIBUTION = [18, 25, 30, 35, 40, 50, 60]

def newfan_age(uid, day, relative=True):
    cmd = 'select ages from %s where uid=%s and day="%s"' % (FANS_TREND, uid, day)
    ages = get1_DB(cmd)
    if not ages:
        print 'no ages data crawled on %s' % day
        return ''
    lst = ast.literal_eval(ages)
    dic = {}
    for i in lst:
        dic[i['age']] = i['count']
    total = sum(dic.values()) * 1.0
    if relative and total > 0:
        for k in dic:
            dic[k] /= total
    return dic

def fan_activity(uid, end, ndays):
    weekday_dist = [0, ] * 7
    hour_dist = [0, ] * 24
    ori_weekday, ori_hour = [0, ] * 7, [0, ] * 24
    for i in range(ndays):
        day = daysago(end, i)
        cmd = 'select count,weekday,hour,ori_postnum from %s where day="%s" and uid=%s' % \
            (FANS_ACTIVITY_TABLE, day, uid)
        res = get_DB(cmd)
        for count, weekday, hour, ori_postnum in res:
            weekday_dist[weekday] += count
            ori_weekday[weekday] += ori_postnum
            hour_dist[hour] += count
            ori_hour[hour] += ori_postnum
    return weekday_dist, hour_dist, ori_weekday, ori_hour

def top_distribution(dic, n, relative=True):
    total = float(sum(dic.values()))
    if relative and total > 0.0:
        for k in dic:
            dic[k] /= total
    return list(sortv_iter(dic))[:n]

@benchmark()
def test_insertdb():
    cursor = get_connect()
    cmd = 'insert into word_dict2 (doc_w,title_w,p) value (%s,%s,%s) ' + \
        'on duplicate key update p=%s'
    for i in range(1000):
        try:
            cursor.execute(cmd, [i, i, i * .1, i * .1])
            cursor.connection.commit()
            transaction.commit_unless_managed()
        except (MySQLdb.IntegrityError, IntegrityError):
            cursor.connection.rollback()
            transaction.rollback_unless_managed()
        except Exception, e:
            print e
            traceback.print_exc()
            cursor.connection.rollback()
            transaction.rollback_unless_managed()
    cursor.connection.close()

def allfan_dist(uid, start, end):
    cmd = '''select follower_count, v_followers_count, daren_followers_count, male, female, locations
                          from %s where uid=%s and day="%s"''' % (FANS_TREND, uid, end)
    allfans = get_DB(cmd)
    verified, gender, province = [], [], []
    if not allfans:
        print 'no fans data crawled on %s' % end
        return verified, gender, province
    follower_count, v_followers_count, daren_followers_count, male, female, locations = allfans[0]
    if daren_followers_count:
        verified = [follower_count - v_followers_count - daren_followers_count, v_followers_count, daren_followers_count]
    if male and female:
        gender = [('f', female), ('m', male)]
    if locations:
        locations = ast.literal_eval(locations)
        for loc in locations:
            province.append((loc['province'], loc['count']))
        province.sort(key=lambda x: x[1], reverse=True)
    return verified, gender, province[:10]

def response_share(uid, start, end):
    alls, accounts = 0, 0
    for table in month_tables(start, end):
        all_interact = 'select count(1) from %s where src_uid=%s and '% (INTERACT_TABLE + table, uid) \
                      + time_between('date(created_at)', start, end)
        account_interact = 'select count(1) from %s where src_uid=%s and uid=%s and '% (INTERACT_TABLE + table, uid, uid)\
                          + time_between('date(created_at)', start, end)
        alls += get1_DB(all_interact)
        accounts += get1_DB(account_interact)
    return float(accounts)/alls if alls else 0

if __name__ == '__main__':
    uid = '2240206400'
    end = datetime.date.today() + relativedelta(days= -1)
    start = end + relativedelta(months= -1)
    print tweets_stat(uid, start, end)
    er_nday(uid, 30, end)
    print top_influencers(5, uid, start, end)
