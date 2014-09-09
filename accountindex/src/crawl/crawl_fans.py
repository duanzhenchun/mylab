#coding=utf-8

from crawl import Base
from utils import *
from conf import *
import time

#获取全量粉丝

class CrawlFans(Base):
    # 爬取用户粉丝、关注信息
    def __init__(self, uid, tablename, client=None):
        Base.__init__(self, client)
        self.uid = uid
        #self.table_name = FANS_TABLE + month_str()
        self.table_name = tablename
    
    def save_user(self, tablename, weibouser, uidtags, timestamp):
        dic = {}
        fields = ('id', 'screen_name', 'province', 'city', 'location', 'gender',
                'profile_url', 'weihao', 'verified', 'verified_type', \
                'allow_all_act_msg', 'created_at', 'description', \
                'statuses_count', 'friends_count', 'followers_count', \
                'favourites_count')
        for k in fields:
            dic[k] = weibouser.get(k, '')
        #if not dic['verified']:
            #dic['verified'] = 0
        #if not dic['verified_type']:
            #dic['verified_type'] = -1
        uid = weibouser.get('id', '')
        dic['tags'] = ','.join(uidtags.get(uid, ''))
        dic['created_at'] = fmt_create_at(dic['created_at'])
        dic['follow_time'] = datetime.datetime.now()
        dic['uid'] = dic.pop('id')
        dic['description'] = self.get_normal_text(dic['description'])
        dic['src_uid'] = self.uid
        dic['follows'] = str(timestamp)[:-3] if timestamp else time.time()
        [dic.pop(i) for i in dic.copy() if dic[i]=='']
        return self.insertDB(tablename, dic)
        
    def get_tags(self, uids):
        self.client, weitags = loop_get_data(self.client, 'tags__tags_batch', uids=','.join(uids))
        if not weitags:
            return {}
        uidtags = {}
        for weitag in weitags:
            tags = weitag.get('tags', {})
            uidtag = [sorted(tag.items())[0][1] for tag in tags]
            uidtags[weitag['id']] = uidtag
        return uidtags
    
    def get_last_fans(self):
        #获取数据库中最后爬取的粉丝看是否是新添加粉丝。
        #last_fans_table = get_last_table(self.cursor)
        #if not last_fans_table: return []
        sqlcmd = 'select DISTINCT(uid) from ' + self.table_name + ' where src_uid=%s'
        self.execute_sql(sqlcmd, (self.uid, ))
        uids = self.cursor.fetchall()
        return [i[0] for i in uids]
    
    def get_fans(self):
        last_crawl = set(self.get_last_fans())
        create_follow(self.cursor, self.table_name)
        cursor = 0 # API下标
        existnum = 0  # 数据库中存在数据条数
        busclient = set_client(self.cursor, True, True, self.uid)
        #self.client.get.account__rate_limit_status()
        #exist_set = set()
        while True:
            # 对API请求3次 防止API请求成功没结果的,请求有结果就跳出循环
            busclient, weibotext = loop_get_data(busclient,
                                   'friendships__followers__all__ids', 'ids',
                                   count=2000, max_time=cursor)
            weiusers = weibotext.get('ids', '')
            if not weiusers:
                return True
            
            print self.uid, cursor, len(weiusers), weibotext.get('total_number', 0)
            uids = []
            uidtags = {}
            n = 0
            cursor = cursor if cursor else str(int(time.time())) + '000'
            for userid in weiusers:
                #if userid in last_crawl: continue
                # 获取后面20个UID的详细信息
                # 获取后面20个需要用到的UID的tag
                if n % 20 == 0:
                    uidtags = {}
                    uids = [weitag for weitag in weiusers[n:n + 20]]
                    uids = list(set(uids) - last_crawl)
                    if uids:
                        uidtags.update(self.get_tags([str(i) for i in uids]))
                n += 1
                self.client, userinfo = loop_get_data(self.client,
                                   'users__show', 'id', uid=userid)
                #last_crawl.add(userid)
                if not userinfo: 
                    userinfo['id'] = userid
                exist = self.save_user(self.table_name, userinfo, uidtags, cursor)
                if exist:
                    existnum += 1
                # 当数据库中存在的重复的数据超过10条 认为是已经抓过的数据 跳出抓取
                #if existnum >= 200:
                #    return True
            # 获取下一页游标
            cursor = weibotext.get('next_cursor', 0)
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
                
    def crawl_users(self, fname):
        f=open(fname)
        uids = []
        for l in f:
            uid = int(l.strip())
            uids.append(uid)
        self.crawl_uids(uids)

    def crawl_uids(self, weiusers):
        print len(weiusers)
        last_crawl=set()
        n=0
        existnum=0
        cursor = 0
        for userid in weiusers:
            #if userid in last_crawl: continue
            # 获取后面20个UID的详细信息
            # 获取后面20个需要用到的UID的tag
            if n % 20 == 0:
                uidtags = {}
                uids = [weitag for weitag in weiusers[n:n + 20]]
                uids = list(set(uids) - last_crawl)
                if uids:
                    uidtags.update(self.get_tags([str(i) for i in uids]))
            n += 1
            self.client, userinfo = loop_get_data(self.client,
                               'users__show', 'id', uid=userid)
            if not userinfo: 
                userinfo['id'] = userid
            exist = self.save_user(self.table_name, userinfo, uidtags, cursor)
            if exist:
                existnum += 1
                # 当数据库中存在的重复的数据超过10条 认为是已经抓过的数据 跳出抓取
                if existnum >= 200:
                    return True
 

if __name__ == '__main__':
    process = CrawlFans('876543210', 'fans_sex')
    process.crawl_users('coppertone.txt')
    #process.get_fans()
    #process.follower_trend()
    #process.account_daily()
    #process.fans_info()
