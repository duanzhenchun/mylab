#!/usr/bin/env python
# encoding: utf-8

from crawl import Base
from utils import *
from conf import *


TABLE_SUFIX=False

class CrawlRelation(Base):
    def __init__(self, uid, client=None, table=FANS_TABLE):
        Base.__init__(self, client)
        self.uid = uid
        self.table_name = table #+ month_str()

    def save_user(self, tablename, weibouser):
        dic = {}
        for k in USER_FIELDS:
            dic[k] = weibouser.get(k,'')
        dic['idstr']=str(dic['id'])
        dic['created_at'] = fmt_create_at(dic['created_at'])
        dic['description'] = self.get_normal_text(dic['description'])
        last_tweet = weibouser.get('status')
        if last_tweet:
            pre='last_tweet_'
            dic[pre+'id'] = last_tweet.get('id','')
            dic[pre+'text'] = self.get_normal_text(last_tweet['text'])
            dic[pre+'source'] = self.get_normal_text(last_tweet.get('source',''))
            dic[pre+'publish_time']= fmt_create_at(last_tweet['created_at'])
            dic[pre+'rt']= last_tweet.get('reposts_count',0)
            dic[pre+'ct']= last_tweet.get('comments_count',0)
            dic[pre+'attitudes']= last_tweet.get('attitudes_count',0)
        apx = TABLE_SUFIX and '_%c' %(str(dic['id'])[-1]) or ''
        return self.insertDB(tablename+apx, dic)

    def save_relation(self, id, original_uid):
        dic = {'id':int(id), 'original_uid': original_uid}
        print original_uid, id
        #apx = TABLE_SUFIX and '_%c' %(str(id)[-1]) or ''
        return self.insertDB(RELATION_TABLE, dic)

    def get_last_uids(self, table=FANS_TABLE):
        last_table = get_last_table(self.cursor, table)
        if not last_table: return []
        sqlcmd = 'select DISTINCT(uid) from ' + last_table + ' where src_uid=%s ORDER BY follow_time DESC limit 200'
        self.execute_sql(sqlcmd, (self.uid, ))
        uids = self.cursor.fetchall()
        return [i[0] for i in uids]

    def get_fans(self):
        last_crawl = set(self.get_last_uids())
        create_follow(self.cursor, self.table_name)
        cursor = 0  # API下标
        existnum = 0  # 数据库中存在数据条数
        while True:
            # 对API请求3次 防止API请求成功没结果的,请求有结果就跳出循环
            self.client, weibotext = loop_get_data(self.client,
                                   'friendships__followers', 'users',
                                   uid=self.uid, count=199, cursor=cursor)
            weiusers = weibotext.get('users', '')
            if not weiusers:
                return True
            # 获取下一页游标
            cursor = weibotext.get('next_cursor', 0)
            print self.uid, cursor, len(weiusers), weibotext.get('total_number', 0)
            uids = []
            n = 0
            for weiuser in weiusers:
                # 获取后面20个需要用到的UID的tag
                if n % 20 == 0:
                    uids = [weitag['id'] for weitag in weiusers[n:n + 20]]
                    uids = list(set(uids) - last_crawl)
                n += 1
                if weiuser['id'] in last_crawl:
                    exist = True
                else:
                    exist = self.save_user(self.table_name, weiuser)
                if exist:
                    existnum += 1
                # 当数据库中存在的重复的数据超过10条 认为是已经抓过的数据 跳出抓取
                #if existnum >= 30:
                   # return True
            # 当获取到的数据中没有下一页了 表示抓取完成
            if cursor == 0:
                return True


    def get_friends(self,trim_status=1, save_self=True):
        last_crawl = set(self.get_last_uids(FRIENDS_TABLE))
        cursor = 0  # API下标
        existnum = 0  # 数据库中存在数据条数
        self.client, userinfo = loop_get_data(self.client,
                                   'users__show', 'id', uid=self.uid)
        if not userinfo:
            return
        if save_self:
            self.save_user(self.table_name, userinfo)
        while True:
            # 对API请求3次 防止API请求成功没结果的,请求有结果就跳出循环
            self.client, weibotext = loop_get_data(self.client,
                                   'friendships__friends', 'users',
                                   uid=self.uid, count=199, trim_status=trim_status, cursor=cursor)
            weiusers = weibotext.get('users', '')
            if not weiusers:
                return True
            # 获取下一页游标
            cursor = weibotext.get('next_cursor', 0)
            #print self.uid, cursor, len(weiusers), weibotext.get('total_number', 0)
            uids = []
            n = 0
            for weiuser in weiusers:
                # 获取后面20个需要用到的UID的tag
                if n % 20 == 0:
                    uids = [weitag['id'] for weitag in weiusers[n:n + 20]]
                    uids = list(set(uids) - last_crawl)
                n += 1
                exist = True
                if weiuser['id'] not in last_crawl:
                    exist = self.save_user(self.table_name, weiuser)
                    self.save_relation(weiuser['id'], self.uid)
                if exist:
                    existnum += 1


    def get_bilateral_ids(self,trim_status=1, save_self=True):
        last_crawl = set(self.get_last_uids(FRIENDS_TABLE))
        cursor = 0  # API下标
        existnum = 0  # 数据库中存在数据条数
        while True:
            # 对API请求3次 防止API请求成功没结果的,请求有结果就跳出循环
            self.client, weibotext = loop_get_data(self.client,
                                   'friendships__friends__bilateral_ids', 'users',
                                   uid=self.uid, count=1999, cursor=cursor)
            weiusers = weibotext.get('users', '')
            if not weiusers:
                return True
            # 获取下一页游标
            cursor = weibotext.get('next_cursor', 0)
            #print self.uid, cursor, len(weiusers), weibotext.get('total_number', 0)
            uids = []
            n = 0
            for weiuser in weiusers:
                # 获取后面20个需要用到的UID的tag
                if n % 20 == 0:
                    uids = [weitag['id'] for weitag in weiusers[n:n + 20]]
                    uids = list(set(uids) - last_crawl)
                n += 1
                exist = True
                if weiuser['id'] not in last_crawl:
                    exist = self.save_user(self.table_name, weiuser)
                    self.save_relation(weiuser['id'], self.uid)
                if exist:
                    existnum += 1
                # 当数据库中存在的重复的数据超过10条 认为是已经抓过的数据 跳出抓取
                #if existnum >= 30:
                   # return True
            # 当获取到的数据中没有下一页了 表示抓取完成
            if cursor == 0:
                return True               # 当数据库中存在的重复的数据超过10条 认为是已经抓过的数据 跳出抓取
                #if existnum >= 30:
                   # return True
            # 当获取到的数据中没有下一页了 表示抓取完成
            if cursor == 0:
                return True

    def account_daily(self):
        tablename = ACCOUNT_GROWTH_TABLE
        self.client, res = loop_get_data(self.client,
                                   'users__counts',
                                   uids=self.uid)
        for dic in res:
            dic.pop('private_friends_count')
            dic['uid'] = dic.pop('id')
            dic['day'] = datetime.datetime.now().date().strftime('%Y%m%d')
            return self.insertDB(tablename, dic)

    def follower_trend(self):
        """
        http://open.weibo.com/wiki/C/2/friendships/followers/trend_count
        latest 30 days
        to yesterday
        {
            uid: 2240206400,
            result: [
            {
                follower_count: "312027",
                active_follower: "63513",    //活跃粉丝数
                days: "2013-04-02",
                loyal_follower: "15121",    //互动粉丝数
                follower_count_online: "314038" //粉丝数
            },
            ...
        """
        """
        http://open.weibo.com/wiki/C/2/friendships/followers/age_group_count
        {
            uid: 2240206400,
            result: {
                total_count: 159430,
                ages: [
                {
                count: 1362,
                age: "0-17"
                ...
        },
        """
        api_cmd = ['friendships__followers__trend_count', 'friendships__followers__age_group_count']
        client = set_client(self.cursor, True, True, self.uid)
        #client.get.account__rate_limit_status()
        if client.is_expires(): return
        for cmd in api_cmd:
            client, results = loop_get_data(client, cmd, 'result')
            if not results:
                break
            uid = results.get('uid', -1)
            results = results.get('result', '')
            if isinstance(results, dict):
                self.insert_trend(uid, results)
            else:
                for result in results:
                    self.insert_trend(uid, result)

    def insert_trend(self, uid, result):
        field_dic = {}
        day = result.get('days', '')
        if not day: day = daysago(self.nowtime, 1).date()
        fields = ['follower_count', 'follower_count_online', 'active_follower', 'loyal_follower', 'ages']
        for field in fields:
            field_dic[field] = result.get(field, '')
        field_dic['age_count'] = result.get('total_count', '')
        field_dic['ages'] = repr(field_dic['ages']) if field_dic['ages'] else ''
        field_dic = dict(filter(lambda x: x[1] != '', field_dic.items()))
        if not field_dic: return
        keys = ','.join([i + '=%s' for i in field_dic.keys()])
        insertsql = 'insert into %s ' % FANS_TREND + 'set uid=%s, day=%s,' + \
                    keys + ' on duplicate key update ' + keys
        try:
            self.execute_sql(insertsql, tuple([uid, day] + field_dic.values() + field_dic.values()))
            self.cursor.connection.commit()
        except Exception, e:
            print e
            self.cursor.connection.rollback()

    def fans_info(self):
        """
        http://open.weibo.com/wiki/C/2/users/behavior_trend
        这个里面可以得到认证粉丝数和达人粉丝数，然后可以计算出认证比例，达人比例和普通用户比例
        http://open.weibo.com/wiki/2/friendships/followers/gender_count
        性别
        http://open.weibo.com/wiki/2/friendships/followers/location_count
        省份
        """
        api_cmd = {'users__behavior_trend': ['v_followers_count', 'daren_followers_count'],
                   'friendships__followers__gender_count': ['male', 'female'],
                   'friendships__followers__location_count': ['locations']}
        client = set_client(self.cursor, True, True, self.uid)
        if client.is_expires(): return
        for cmd in api_cmd:
            client, results = loop_get_data(client, cmd, 'result')
            if not results:
                break
            uid = results.get('uid', -1)
            results = results.get('result', '')
            if isinstance(results, dict):
                self.insert_fans_trend(uid, results, api_cmd[cmd])
            else:
                for result in results:
                    self.insert_fans_trend(uid, result, api_cmd[cmd])

    def insert_fans_trend(self, uid, result, fields):
        field_dic = {}
        day = daysago(self.nowtime, 1).date()
        for field in fields:
            field_dic[field] = result.get(field, '')
        field_dic['follower_count'] = result.get('followers_count', '')
        field_dic = dict(filter(lambda x: x[1] != '', field_dic.items()))
        if field_dic.has_key('locations'):
            field_dic['locations'] = repr(field_dic['locations'])
        if not field_dic: return
        keys = ','.join([i + '=%s' for i in field_dic.keys()])
        insertsql = 'insert into %s ' % FANS_TREND + 'set uid=%s, day=%s,' + \
                    keys + ' on duplicate key update ' + keys
        try:
            self.execute_sql(insertsql, tuple([uid, day] + field_dic.values() + field_dic.values()))
            self.cursor.connection.commit()
        except Exception, e:
            print e
            self.cursor.connection.rollback()


def seed_uids(fname):
    f=open(fname) #'../../data/filter_uniq.txt')
    for l in f:
        uid = l.strip()
        yield int(uid)

@benchmark()
def main(seedfname, tbl_sfx=''):
    for uid in seed_uids(seedfname):
        if not uid:
            continue
        process = CrawlRelation(uid, table=FRIENDS_TABLE+tbl_sfx)
#        start = time.time()
#        process.execute_sql('start transaction')
        process.get_friends(trim_status=0, save_self=False)
#        process.execute_sql('commit')
#        duration = time.time()-start
#        print duration
#        process.execute_sql('select count(1) from %s' %RELATION_TABLE)
#        newcount = process.cursor.fetchone()[0]
#        print 'speed: %.2f/sec' %(1.*(newcount-last)/duration), 'duration:%.2f sec' %duration
#        last = newcount
#        fw.flush()
#    fw.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 1:
        sys.exit("""
Usage:
    %s seedfname
""" % sys.argv[0])
    main(sys.argv[1], sys.argv[2])
