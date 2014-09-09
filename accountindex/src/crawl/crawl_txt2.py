# coding=utf-8

import crawl
from utils import *

class CrawlTweet(crawl.Base):
    def __init__(self, uid, begin, end, client=None):
        crawl.Base.__init__(self, client)
        self.uid=uid
        self.finishnum = {}
        # 爬取截止时间
        self.begin_deadline = begin
        self.end_deadline = end
       
    def process_weibodata(self, weibotext):
        if not isinstance(weibotext, dict):
            return True
        created_at = fmt_create_at(weibotext.get('created_at', ''))
        weiboid = weibotext.get('id')
        source = self.get_source(weibotext.get('source', ''))
        user = weibotext.get('user', {})
        if not user:
            return True
        uid = user.get('id', '')
        screen_name = user.get('name', '')
        screen_name = screen_name if screen_name else uid
        followers_count = user.get('followers_count', 0)
        text = self.get_normal_text(weibotext.get('text'))
        rt_text = self.get_normal_text(weibotext.get('retweeted_status', {}).get('text', ''))
        hashtag = re.findall(r'#(.*?)#', text)
        hashtag = hashtag[0] if hashtag else ''
        reposts_count = weibotext.get('reposts_count', 0)
        comments_count = weibotext.get('comments_count', 0)
        location, gender, verified, verified_type = [user.get(i, '') for i in ['location', 'gender', 'verified', 'verified_type']]
        attitudes_count = weibotext.get('attitudes_count', 0)
        text_data = [uid, screen_name, source, hashtag, reposts_count, comments_count, text, created_at,
                              self.nowtime, location, gender, verified_type, rt_text]
        text_str = ''' uid=%s, screen_name=%s, source=%s, hashtag=%s, reposts_count=%s, 
                              comments_count=%s, text=%s, created_at=%s, lastupdatetime=%s,
                              location=%s, gender=%s, verified_type=%s, rt_text=%s '''                         
        try:
            # 将微博插入到数据库
            insertsql = 'insert into ' + ACCOUNT_TWEET_TABLE + \
                        ' set tid=%s, crawl_created_at=%s, followers_count=%s, ' + text_str + \
                        'on duplicate key update ' + text_str
            self.execute_sql(insertsql, tuple([weiboid, self.nowtime, followers_count] + text_data + text_data))
            self.cursor.connection.commit()
        except Exception, e:
            # traceback.print_exc()
            errdata = '插入用户微博数据错误！ id: %s, screen_name: %s' % (weiboid, unicode_to_str(screen_name))
            print errdata
            send_err_to_mail(errdata,
                            '''错误信息:%s, 
                            错误SQL:%s''' % (repr(e), unicode_to_str(insertsql)))
            self.cursor.connection.rollback()
            
    def save_interact_tweet(self, weitext, weiboid, tasktype, table_name='interact_tweet'):
        if not isinstance(weitext, dict):
            return True
        dic = {}
        dic['created_at'] = fmt_create_at(weitext.get('created_at', ''))
        dic['id'] = weitext.get('id', '')
        user = weitext.get('user', {})
        if not user:
            return True
        dic['uid'] = user.get('id', '')
        screen_name = user.get('name', '')
        dic['screen_name'] = screen_name if screen_name else uid
        
        dic['source'] = self.get_source(weitext.get('source', ''))
        fields = ['province', 'location', 'gender', 'verified', 'verified_type', 'statuses_count', 
                  'friends_count', 'followers_count']
        for i in fields:
            dic[i] = user.get(i, '')
        for i in ['reposts_count', 'comments_count']:
            dic[i] = weitext.get(i, 0)
        dic['text'] = self.get_normal_text(weitext.get('text', ''))
        try:
            weitext.pop('retweeted_status')
        except:
            pass
        try:
            weitext.pop('status')
        except:
            pass
        #dic['raw_data'] = weitext
        dic['tasktype'] = tasktype
        dic['lastupdatetime'] = datetime.datetime.now()
        dic['src_uid'] = self.uid
        dic['src_id'] = weiboid
        self.insertDB(table_name, dic)
        """
        try:
            # 将评论转发插入到数据库
            insertsql = 'insert into ' + table_name + ''' (id, src_uid, src_id, uid, screen_name, created_at, tasktype, 
                                raw_data, lastupdatetime) value (%s, %s, %s, %s, %s, %s, %s, %s, %s )'''
            self.execute_sql(insertsql, (tid, self.uid, weiboid, uid, screen_name, created_at, tasktype, weitext, datetime.datetime.now()))
            self.cursor.connection.commit()
        except Exception, e:
#             print e
            self.cursor.connection.rollback()
            """
    
    def crawl_task(self, tid, tasktype=REPOST_TASK, page=1,
                   lastfinishnum=0, stop_uid=None):
        self._get_cursor()
        args = TASK_API_ARG[tasktype]
        tasknum = 0
        allnum = 0
        while True:
            self.client, data = loop_get_data(self.client, args[0], args[1],
                                              id=tid, count=200, page=page)
            tweets = data.get(args[1], '')
            allnum = data.get('total_number', 0)
            if not tasknum and allnum:
                tasknum = allnum
            if not allnum: allnum = tasknum
            # 请求3次还是没有结果的当爬取完成计算
            if not tweets:
                # 当api没有请求到数据 判断是否已爬取完成，如果爬取完成，跳出爬取，爬取没有完成继续
                # return
                print 'uid: %s tid: %s 没有数据! page: %s allnum: %s' % \
                    (unicode_to_str(self.uid), unicode_to_str(tid), page, allnum)
            for tweet in tweets:
                # 分析单条记录  
                try:
                    if stop_uid:
                        self.save_response(tweet, tid, stop_uid)
                    else:
                        created_at = fmt_create_at(tweet.get('created_at', ''))
                        if not created_at: continue
                        table_name = INTERACT_TABLE + '_'.join((str(created_at.year), str(created_at.month)))
                        create_repost(self.cursor, table_name)
                        self.save_interact_tweet(tweet, tid, tasktype, table_name)
                except Exception, e:
                    print e
            if allnum < 200 * page + lastfinishnum:
                if stop_uid:
                    self.save_finishnum(DIRECTAT_TABLE, tid, allnum)
                else:
                    self.save_finishnum(ACCOUNT_TWEET_TABLE, tid, allnum,
                                        finish_field=tasktype + '_finishnum')
                return
            page += 1
    
    def get_weibo_name(self, url):
        parse = urlparse.urlparse(url)
        path = parse.path
        if not path:
            return
        if path.startswith('/u/'):
            self.uid = path[3:]
        else:
            # 统一使用uid进行处理
            self.screen_name = path[1:]
            self.client, uiddata = loop_get_data(self.client, 'users__domain_show',
                                                 '', domain=self.screen_name)
            self.uid = uiddata.get('id', '')
        return path
    
    def user_timeline(self):
        # 抓取用户最近发的微博
        totalnum = 0
        page = 1
        while True:
            self.client, timelines = loop_get_data(self.client, 'statuses__user_timeline',
                               'statuses', uid=self.uid, page=page, count=100)
            if not totalnum: 
                totalnum = timelines.get('total_number', 101)
            print self.uid, totalnum, page
            timelines = timelines.get('statuses', '')
            for timeline in timelines:
                created_at = fmt_create_at(timeline.get('created_at', ''))
                if created_at < self.begin_deadline:
                    return 
                weiboid = timeline.get('id', '')
                reposts_count = timeline.get('reposts_count', 0)
                comments_count = timeline.get('comments_count', 0)
                finishnum = self.finishnum.get(weiboid, [0, 0])
                # 更新微博数据
                self.process_weibodata(timeline)
                # 当有新的评论转发，进行爬取
                '''
                if reposts_count - finishnum[0] > 0:
                    self.crawl_task(weiboid, 'reposts', lastfinishnum=finishnum[0])
                if comments_count - finishnum[1] > 0:
                    self.crawl_task(weiboid, 'comments', lastfinishnum=finishnum[1])
                    '''
            if totalnum < page*100: return
            page += 1
            
    def tweet_user_timeline(self, uid, maxcount=200):
        page = 1
        doc = []
        while maxcount > 0 and page < 4:
            self.client, timelines = loop_get_data(self.client, 'statuses__user_timeline',
                               'statuses', uid=uid, page=page, count=100,
                               feature=1, trim_user=1)
            timelines = timelines.get('statuses', '')
            page += 1
            for timeline in timelines:
                maxcount -= 1
                if maxcount <= 0:
                    break
                dic = dict(
                           tid=timeline.get('id', ''),
                           uid=uid,
                           text=self.get_normal_text(timeline.get('text')),
                           created_at=fmt_create_at(timeline.get('created_at', '')),
                         )
                doc += list(gen_nounword(dic['text']))
                self.insertDB(ORI_TWEETS, dic)
        return doc
            
    def random_account(self):
        self.client, res = loop_get_data(self.client, 'statuses__public_timeline',
                            count=200,)
        timelines = res.get('statuses', '')
        for timeline in timelines:
            user = timeline.get('user')
            followers_count = user.followers_count
            if followers_count < 100 and not 200 <= user.verified_type < 400:
                continue
            uid = user.id
            if self.existed(uid):
                print '%s is existed' % uid
                continue
            print uid, user.screen_name
            dic = dict(
                uid=uid,
                screen_name=user.screen_name,
                followers_count=followers_count,
                friends_count=user.friends_count,
                doc=u' '.join(self.tweet_user_timeline(uid)),
                verified_type=user.verified_type,
                raw_data=user,
                )
            self.insertDB(ACCOUNT_LAB, dic)   
    
    def existed(self, uid):
        cmd = 'select count(1) from %s ' % ACCOUNT_LAB + 'where uid=%s' % uid
        self.cursor.execute(cmd)
        res = self.cursor.fetchone()
        return res[0] > 0
        
    def tweets_exposure(self):
#         mysql_tool.create_exposure(self.cursor)
        sqlcmd = 'select tid from ' + ACCOUNT_TWEET_TABLE + ' where uid=%s and created_at>%s'
        self.execute_sql(sqlcmd, (self.uid, datetime.datetime.now() - datetime.timedelta(14)))
        tids = self.cursor.fetchall()
        bclient = set_client(self.cursor, isbuss=True, needAuth=True, uid=self.uid)
        for tid in tids:
            if bclient.is_expires(): return
            bclient = self.exposure(tid[0], bclient)
            
    def exposure(self, tid, bclient):
        """
        http://open.weibo.com/wiki/C/2/statuses/exposure
        daily
        last 30 days
        JsonObject: {'id': 3579684631322498, 
        'result': [{'exposure_count': u'6641', 'day': u'2013-05-19'}, 
        {'exposure_count': u'1350', 'day': u'2013-05-20'}, 
        {'exposure_count': u'774', 'day': u'2013-05-21'}, 
        {'exposure_count': u'642', 'day': u'2013-05-22'}]}
        """    
        bclient, res = loop_get_data(bclient, 'statuses__exposure', id=tid)
        for dic in res.get('result', ''):
            dic['uid'] = self.uid
            dic['tid'] = tid
            self.insertDB(EXPOSURE_TALBE, dic)
        return bclient

    def insert_task(self, weiboid):
        # 将转发评论任务放到任务列表数据库
        insertsql = 'insert into%s ' + TASKLIST_TABLE + ''' (weiboid, uid, create_at) value (%s, %s, %s) '''
        try:
            self.execute_sql(insertsql, (weiboid, self.uid, datetime.datetime.now()))
            self.cursor.connection.commit()
        except:
            print 'insert task errer! task: %s uid: %s' % (weiboid, self.uid)
    
    def findall_tweets(self):
        if not self.uid:
            return
        sqlcmd = 'select tid, reposts_finishnum, comments_finishnum from ' + \
                 ACCOUNT_TWEET_TABLE + ' where uid=%s and created_at>%s'
        self.execute_sql(sqlcmd, (self.uid, self.begin_deadline))
        res = self.cursor.fetchall()
        # 存放已经爬取过的评论转发数据数量
        [self.finishnum.update({i[0]:i[1:]}) for i in res]
        self.user_timeline()
        
    def direct_at(self, start, end):
        """
        http://open.weibo.com/wiki/2/search/statuses
        q = request.GET.get('q', '').strip()
        count = request.GET.get('count', 50)
        filter_ori = request.GET.get('filter_ori', 0)
        """
        uname = self.username(self.uid)
        if not uname: return
        q = '@%s' % uname
        count = 50
        filter_ori = 1
        start = time.mktime(self.begin_deadline.timetuple())
        bclient = set_client(self.cursor, isbuss=True, needAuth=True)
        if bclient.is_expires(): return
        bclient, res = loop_get_data(bclient, 'search__statuses__limited',
                               q=q, count=count, filter_ori=filter_ori,
                               starttime=start, needcount=True)
        count = 0
        for tweet in res.get('statuses', ''):
            if is_at(tweet, uname):
                self.save_directat(tweet)
                count += 1

    def save_directat(self, tweet):
        dic = {'raw_data':tweet,
               'tid':tweet['id'],
               'uid':tweet['user']['id'],
               'target_uid':self.uid,
               'created_at':fmt_create_at(tweet['created_at']),
               'text':self.get_normal_text(tweet.get('text', '')),
               'is_question':is_question(tweet.get('text', ''))}
        return self.insertDB(DIRECTAT_TABLE, dic)

    def load_directat(self):
        findsql = '''select tid, finish_num from %s where target_uid=%s
                and is_question=True and response_time is NULL and created_at>(%s)'''\
                % (DIRECTAT_TABLE, self.uid,
                   daysago(datetime.datetime.now().date(), 7).strftime('%Y%m%d'))
        self.cursor.execute(findsql)  # , (self.uid)),
        rows = self.cursor.fetchall()
        return rows

    def find_response(self):
        tids = self.load_directat()
        for (tid, finish_num) in tids:
            finish_num = finish_num and int(finish_num) or 0
            self.crawl_task(tid, COMMENT_TASK, lastfinishnum=finish_num, stop_uid=self.uid)
 
    def save_response(self, tweet, tid, stop_uid):
        user = tweet.get('user', {})
        if not user:
            return False
        if user.get('id', '') != stop_uid:
            return False
        # save DB
        updatesql = 'update %s' % DIRECTAT_TABLE + \
                  ''' set response_time=%s, response_raw_data=%s where tid=%s'''
        self.execute_sql(updatesql,
                (fmt_create_at(tweet.get('created_at', tid)), tweet, tid))
        self.cursor.connection.commit()
        return True

    def save_finishnum(self, tblname, tid, n, finish_field='finish_num'):
        cmd = 'update %s ' % tblname + 'set %s' % finish_field + '=%s where tid=%s'
        try:
            self.execute_sql(cmd, (n, tid))
            self.cursor.connection.commit()
        except:
            self.cursor.connection.rollback()
        return True
 

def is_at(tweet, uname):
    txt = tweet.get('text', '')
    # following: space or end of line
    return len(re.findall('(?<!//)@%s(?:\s+|$)' % uname, txt)) > 0

def is_question(txt):
    if not txt:
        return False
    for i in QUESTION_KEYWORDS:
        if i in txt:
            return True
    else:
        return False
    
if __name__ == '__main__':
    f=open('./uids.txt')
    ACCOUNT_TWEET_TABLE = 'account_tweet_copperstone'
    begin = datetime.datetime(2014, 2, 1, 0, 0, 0)
    end  = datetime.datetime(2014, 5, 12, 0, 0, 0)
    for uid in f:
        uid = uid.strip()
        print uid
        crawl_tweet = CrawlTweet(uid,begin,end)
        crawl_tweet.findall_tweets()
    print 'Done!'
