#coding=utf-8

import ast, time, urllib2, json
import crawl
from utils import get_connect, fmt_create_at

uids ='2667224511, 1928244585, 2242065150'
SVR_JUDGE_URL = 'http://192.168.4.145/spam/api_simple_judge'

def call_judge(data):
    SVR_SECRET = 'tryme'
    req = urllib2.Request(SVR_JUDGE_URL)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps({'secret': SVR_SECRET, 'data': data})).read()
    if not response:
        return {}
    res = json.loads(response)
    return res.get('result', {})

def update_sql(table_name, date):
    zombie = call_judge(date)
    for ruid, zom in zombie.items():
        insert_sql = 'update %s set real_followers_count=%s, zombie=%s where uid=%s and tasktype="reposts"' % \
                   (table_name, 0 if zom else date[int(ruid)][4], zom, ruid)
        try:
            cursor.execute(insert_sql)
            cursor.connection.commit()
        except Exception, e:
            print e
            
def update(cursor, table_name):
    cmd = 'select DISTINCT uid, raw_data from %s where tasktype="reposts" and src_uid in (%s)  and real_followers_count is null' % (table_name, uids)
    cursor.execute(cmd)
    result = cursor.fetchall()
    print len(result)
    n = 0
    date = {}
    tids = {}
    for res in result:
        uid, weitext = res
        weitext = ast.literal_eval(weitext)
        dic = {}
        fields = ['id', 'reposts_count', 'comments_count', 'pid']
        [dic.update({i:weitext.get(i, 0)}) for i in fields]
        user = weitext.get('user', {})
        user_fields = ['statuses_count', 'location', 'friends_count', 'profile_image_url', 'screen_name', 'verified_type',
                       'followers_count', 'favourites_count', 'bi_followers_count', 'gender']
        [dic.update({i:user.get(i, '')}) for i in user_fields]
        dic['description'] = user.get('description', '')
        dic['uid'] = user.get('id', '')
        dic['user_created_at'] = fmt_create_at(user.get('created_at', ''))
        days2now = int(time.mktime(dic['user_created_at'].timetuple()))
        date.update({dic['uid']: [dic['bi_followers_count'], dic['statuses_count'], dic['friends_count'], days2now, dic['followers_count'],
                             dic['favourites_count'], 0 if dic['verified_type'] == -1 else 1,  dic['verified_type'], 
                             0 if dic['gender'] == 'f' else 1, len(dic['description'])]})
        n += 1
        if n%200 == 0:
            update_sql(table_name, date)
            n = 0
            date = {}
            tids = {}
    update_sql(table_name, date)
            
if __name__ == "__main__":
    print 'start'
    cursor = get_connect()
    update(cursor, 'interact_tweet_2013_12')
    cursor.close()
    print 'end'
    