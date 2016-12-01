"""
ref:
    http://en.wikipedia.org/wiki/Cron

crontab -e
# Minute   Hour   Day of Month       Month          Day of Week        Command

@hourly  cd /home/admin/accountindex/src && python scheduler.py hourly
@daily   cd /home/admin/accountindex/src && python scheduler.py daily
@weekly  cd /home/admin/accountindex/src && python scheduler.py weekly
@monthly cd /home/admin/accountindex/src && python scheduler.py monthly

"""

from multiprocessing import Pool
from dateutil.relativedelta import relativedelta
from analyse import statist
from crawl import crawl_txt, crawl_relation
from utils import *


TASK_TYPES = 'hourly, daily, weekly, monthly'
NUMBER_OF_PROCESSES = 15
TIMEOUT_HOURLY = 60 * 30

def hourly(uid):
    end = hours_ago(0)
    start = hours_ago(1)
    crawler = crawl_txt.CrawlTweet(uid)
    crawler.findall_tweets()
    crawler.direct_at(start, end)
    crawler.find_response()

    crawler = crawl_relation.CrawlRelation(uid)
    assert crawler.get_fans()
    return uid

def daily(uid):
    crawler = crawl_txt.CrawlTweet(uid)
    crawler.tweets_exposure()
    crawler2 = crawl_relation.CrawlRelation(uid)
    crawler2.account_daily()
    crawler2.follower_trend()
    crawler2.fans_info()
    for i in range(7):
        statist.fans_day_activity(uid, i + 1)

def weekly(uid, end=None):
    if not end:
        end = datetime.date.today() + relativedelta(days= -1)
    else:
        try:
            end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        except:
            traceback.print_exc()
    start = end + relativedelta(days= -6)
    dic = {'uid':uid, 'day':end, 'period':'weekly'}
    res = statist.fan_growth(uid, start, end)
    dic['fans'], dic['fan_growth'] = res[0], res[1]
    res = statist.tweets_stat(uid, start, end)
    dic.update(dict(zip(('tweets', 'retweets', 'comments', 'likes'), res)))
    dic['direct_at'] = statist.directat_num(uid, start, end)
    dic['impressions'] = statist.exposure_num(uid, start, end)
    for i in (30, 7):
        dic['er_%d' % i] = statist.er_nday(uid, i, end)
    dic['top_posts'] = repr(statist.top_posts(5, uid, start, end))
    dic['top_influencers'] = repr(statist.top_influencers(5, uid, start, end))
    dic['top_hashtags'] = repr(statist.top_hashtags(3, uid, start, end))
    res = statist.response(uid, start, end)
    dic.update(dict(zip(('questions', 'responds', 'mean_respond_time'), res)))
    res = statist.fan_active(uid, end)
    dic.update(dict(zip(('active', 'interactive'), res)))
    res = statist.newfan_dist(uid, start, end)
    fields = ('verified_dist', 'subfans_dist', 'province_dist', 'gender_dist', 'tag_dist')
    dic.update(dict(zip(fields, [repr(i) for i in res])))
    dic['age_dist'] = repr(statist.newfan_age(uid, end, False))
    res = statist.fan_activity(uid, end, 7)
    dic.update(dict(zip(('week_dist', 'hour_dist', 'brand_week', 'brand_hour'), [repr(i) for i in res])))
    res = statist.allfan_dist(uid, start, end)
    res = dict(zip(('verified_dist', 'gender_dist', 'province_dist'), [repr(i) if i else i for i in res]))
    [res.pop(i) for i in res.copy() if not res[i]]
    dic.update(res)
    dic['response_share'] = statist.response_share(uid, start, end)
    cursor = get_connect()
    statist.insertDB(cursor, REPORT_TABLE, dic)
    cursor.connection.close()

def monthly(uid):
    end = datetime.date.today() + relativedelta(days= -1)
    start = end + relativedelta(months= -1)
    pass

def taskfn(ttype):
    return eval(ttype)

def schedule(tasktype):
    pool = Pool(processes=NUMBER_OF_PROCESSES)
    uids = mysql_tool.taskuids()
    res = []
    r = pool.map_async(taskfn(tasktype), uids, callback=res.extend)
    r.wait(timeout=TIMEOUT_HOURLY)
    if not r.successful():
        print 'not completed'
    print res

def rand_account(i):
    crawler = crawl_txt.CrawlTweet(None)
    crawler.random_account()

def getresult(x):
    print 'getresult', x

def random_schedule():
    pool = Pool(processes=3)
    for i in range(100):
        pool.apply_async(rand_account, args=(i,), callback=getresult)
    pool.close()
    pool.join()

if __name__ == '__main__':
#     random_schedule()
#     uids = mysql_tool.taskuids()
#     for uid in uids:
#         hourly(uid)
#         daily(uid)
#         weekly(uid)
    if len(sys.argv) < 2 or sys.argv[1] not in [i.strip() for i in TASK_TYPES.split(',')]:
        sys.exit("""Usage:    %s [%s]""" % (sys.argv[0], TASK_TYPES))
    schedule(sys.argv[1])
