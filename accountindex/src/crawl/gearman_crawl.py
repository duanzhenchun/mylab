import gearman
import datetime
import json
from crawl_relation import *
from crawl_txt import *
from crawl_fans import CrawlFans

Servers=['localhost:4730',]
workfn='crawl_fans'
Queue_num=50


def task_relation(worker, job):
    uid = job.data
#    print worker.worker_client_id, uid
    process = CrawlRelation(uid, table=FRIENDS_TABLE)
    process.get_friends(trim_status=0)
    return 'done'


def task_tweet(worker, job):
    uid=job.data
    begin = datetime.datetime(2014, 11, 1, 0, 0, 0)
    end  = datetime.datetime(2014, 11, 30, 23, 59, 59)
    crawl_tweet = CrawlTweet(uid,begin,end)
    crawl_tweet.user_timeline(False)
    return 'done'

def task_fans(worker,job):
    (uid, prob, tbl2)=json.loads(job.data)
    process = CrawlFans(uid)
    fn=None
    if prob>1-PROB:
        fn=process.gen_friends_ids
    elif prob<PROB-1:
        fn=process.gen_followers_ids
    if fn:
        prob *=PROB
        for id in fn():
            insert_prob(process,id,prob,tbl2)
    return 'done'


def init_phase1(nfea=10, fname='/home/whille/svnsrc/spamer/1/spamer/src/training_data.txt'):
    import ast
    with open(fname) as f:
        process = CrawlFans(123)
        for i in f:
            line = i.strip().split(' : ')
            if len(line) != 3:
                continue
            try:
                uid, isspam, features = [ast.literal_eval(i) for i in line]
            except:
                print i
                raise
            prob = isspam and -1.0 or 1.0
            insert_prob(process,uid,prob,'user_phase1')

def insert_prob(process,uid,prob,tblname):
    sqlcmd = 'insert into %s set id=%s, prob=%s on duplicate key update prob=prob+%s' %(
            tblname, uid, prob, prob>0.0 and PROB or -PROB)
    exe_sql(process, sqlcmd)  

def exe_sql(process, cmd):
    try:
        process.execute_sql(cmd)
        process.cursor.connection.commit()
    except Exception, e:
        print e
        process.cursor.connection.rollback()


def dowork():
    import os
    gw = gearman.GearmanWorker(Servers)
    gw.set_client_id('work_%s' %os.getpid())   #optional
    gw.register_task(workfn, task_fans)
    # Enter our work loop
    gw.work()


def gen_probs(tblname):
    process = CrawlFans(123)
    sqlcmd = 'select id, prob from %s where prob not between %s and %s' %(tblname, PROB-1, 1-PROB)
    process.execute_sql(sqlcmd)
    res = process.cursor.fetchall()
    for id,prob in res:
        yield id, prob

def cli_use(tblname, tbl2):
    process = CrawlFans(123)
    exe_sql(process, 'create table IF NOT EXISTS %s like %s' %(tbl2,tblname))

    cli = gearman.GearmanClient(Servers)
    lst=[]
    for uid,prob in gen_probs(tblname):
        lst.append(dict(task=workfn, data=json.dumps((uid, prob, tbl2))))
        if len(lst)>=Queue_num:
            send_work(cli,lst)
            lst=[]
    if lst:
        send_work(cli,lst)

def send_work(cli,lst):
    reqs= cli.submit_multiple_jobs(lst, wait_until_complete=False)
    res = cli.wait_until_jobs_completed(reqs)

def main():
    from optparse import OptionParser
    parser = OptionParser(usage='Usage: %prog [options] tablename tblname2')
    parser.add_option('-w', 
                      action='store_true', dest='workermode', default=None,
                      help='worker mode')
    parser.add_option('-c', 
                      action='store_false', dest='workermode', 
                      help='client mode')
    (options, args) = parser.parse_args()
    is_worker = options.workermode
    if not is_worker and len(args)<2:
        parser.print_help()
        exit(-1)
    if is_worker:
        dowork()
    else:
        cli_use(args[0], args[1])
    

if __name__ == '__main__':
#    init_phase1(fname='/home/whille/bak/data/zombie_neil.txt')
    sys.exit(main())


