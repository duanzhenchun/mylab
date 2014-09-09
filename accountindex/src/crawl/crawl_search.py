#coding=utf-8
import crawl
from utils import *
import datetime

class CrawlSearch(crawl.Base):
    def __init__(self, uid, begin, end, client=None):
        crawl.Base.__init__(self, client)
        self.uid = uid
        self.finishnum = {}
        self.begin_deadline = begin
        self.end_deadline = end
             
    def process_weibodata(self, weibotext, search_text=''):
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
        text_data = [uid, screen_name, source, hashtag, reposts_count, comments_count, text, created_at,
                              self.nowtime, search_text, location, gender, verified_type, rt_text]
        text_str = ''' uid=%s, screen_name=%s, source=%s, hashtag=%s, reposts_count=%s, 
                              comments_count=%s, text=%s, created_at=%s, lastupdatetime=%s, search_text=%s,
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
        created_at = fmt_create_at(weitext.get('created_at', ''))
        tid = weitext.get('id', '')
        user = weitext.get('user', {})
        if not user:
            return True
        uid = user.get('id', '')
        screen_name = user.get('name', '')
        screen_name = screen_name if screen_name else uid
        try:
            weitext.pop('retweeted_status')
        except:
            pass
        try:
            weitext.pop('status')
        except:
            pass
        try:
            # 将评论转发插入到数据库
            insertsql = 'insert into ' + table_name + ''' (id, src_uid, src_id, uid, screen_name, created_at, tasktype, 
                                raw_data, lastupdatetime) value (%s, %s, %s, %s, %s, %s, %s, %s, %s )'''
            self.execute_sql(insertsql, (tid, self.uid, weiboid, uid, screen_name, created_at, tasktype, weitext, datetime.datetime.now()))
            self.cursor.connection.commit()
        except Exception, e:
#             print e
            self.cursor.connection.rollback()
    
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
            if not totalnum: totalnum = timelines.get('total_number', 101)
            print 'uid:%s, totalnum:%d, page:%d' %(self.uid, totalnum, page)
            timelines = timelines.get('statuses', '')
            for timeline in timelines:
                created_at = fmt_create_at(timeline.get('created_at', ''))
                if created_at < datetime.datetime(2013, 3, 31, 23, 59, 59):
                    return
                weiboid = timeline.get('id', '')
                reposts_count = timeline.get('reposts_count', 0)
                comments_count = timeline.get('comments_count', 0)
                finishnum = self.finishnum.get(weiboid, [0, 0])
                # 更新微博数据
                self.process_weibodata(timeline)
                # 当有新的评论转发，进行爬取
                #if reposts_count - finishnum[0] > 0:
                    #self.crawl_task(weiboid, 'reposts', lastfinishnum=finishnum[0])
                #if comments_count - finishnum[1] > 0:
                    #self.crawl_task(weiboid, 'comments', lastfinishnum=finishnum[1])
            if totalnum and totalnum < page*100: return
            page += 1
        
    def search_text(self, text):
        """
        http://open.weibo.com/wiki/2/search/statuses
        q = request.GET.get('q', '').strip()
        count = request.GET.get('count', 50)
        filter_ori = request.GET.get('filter_ori', 0)
        filter_ori	false	int	过滤器，是否为原创，0：全部、1：原创、2：转发，默认为0。
        """
        count = 50
        filter_ori = 1
        page = 1
        tasknum, allnum = 0, 0
        start = time.mktime(self.begin_deadline.timetuple())
        end = time.mktime(self.end_deadline.timetuple())
        bclient = set_client(self.cursor, isbuss=True, needAuth=True)
        if bclient.is_expires(): return
        while True:
            bclient, res = loop_get_data(bclient, 'search__statuses__limited',
                                   q=text, count=count, filter_ori=filter_ori,
                                   starttime=start, endtime=end, needcount=True, page=page)
            allnum = res.get('total_number', 1)
            if not tasknum and allnum:
                tasknum = allnum
            tweet = 0
            end_err = 0
            tweets = res.get('statuses','')
            for tweet in tweets:
                self.process_weibodata(tweet, text)
            if tweet: 
                end_err = time.mktime(fmt_create_at(tweet.get('created_at', '')).timetuple()) - 0.1
            end = end_err
            print 'allnum:', allnum, 'end:', end, time.ctime(end)
            if allnum<=1 or end - start < 60*60*24: #less than 1day
                return

    def save_directat(self, tweet):
        dic = {'raw_data':tweet,
               'tid':tweet['id'],
               'uid':tweet['user']['id'],
               'target_uid':self.uid,
               'created_at':fmt_create_at(tweet['created_at']),
               'text':self.get_normal_text(tweet.get('text', '')),
               'is_question':is_question(tweet.get('text', ''))}
        return self.insertDB(DIRECTAT_TABLE, dic)

    def save_finishnum(self, tblname, tid, n, finish_field='finish_num'):
        cmd = 'update %s ' % tblname + 'set %s' % finish_field + '=%s where tid=%s'
        try:
            self.execute_sql(cmd, (n, tid))
            self.cursor.connection.commit()
        except:
            self.cursor.connection.rollback()
        return True
 
if __name__ == '__main__':
    uid = '2683531895'
    begin = datetime.datetime(2013, 11, 11, 0, 0, 0)
    end  = datetime.datetime(2014, 5, 11, 0, 0, 0)
    crawl_search = CrawlSearch(uid,begin, end)
    txts=u'张靓颖 周笔畅 何洁 刘亦菲 张含韵 陈好 尚雯婕 汤唯 张筱雨 韩雪 孙菲菲 张嘉倪 霍思燕 陈紫函 朱雅琼 江一燕 厉娜 许飞 胡灵 郝菲尔 刘力扬 reborn 章子怡'
    #txts = u'LUX力士 七匹狼 贵人鸟 阿迪达斯 Levis'
    ACCOUNT_TWEET_TABLE = 'account_tweet_ryan'
    kws = ('恋上TA~恋上一种味道', 
            '恋上TA的金牌醇香', 
            '恋上金牌男神',
            '和金牌男神约会',
            '金牌法式烘焙',
            '雀巢金牌咖啡')
    for txt in txts.split():
        print txt
        crawl_search.search_text(txt)
    #crawl_tweet.findall_tweets()
