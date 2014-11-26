import sys
import MySQLdb
import MySQLdb.cursors
import random

dbname = 'WeiboPanel'
dbpwd = 'cicdata'
dbhost, dbport, dbuser = 'localhost', 3306, 'root'
 

def get_connect(cursor=None):
    try:
        conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpwd,
                               db=dbname, port=int(dbport), charset='utf8')
        cur= conn.cursor(cursor)
        return cur
    except Exception, e:
        print 'connect mysql error: %s' % e
        sys.exit()

def get_follow(cur, Id, date_limit=None):
    lim = date_limit and 'and last_tweet_publish_time>"%s"' %date_limit or ''
    cmd="select followers_count from Weibo_User_Profile_%d where id=%d and (followers_count<200000 or friends_count<2000) %s" %(Id%10, Id, lim)
    cur.execute(cmd)
    nfol=-1
    res = cur.fetchone()
    if res:
        nfol=res[0]
    return nfol


def candidates():
    for i in range(10):
        candidates_table('Weibo_User_Relationship_%d' %i)

def candidates_table(tblname):

    date_limit = '2014-07-28'

    cur=get_connect(MySQLdb.cursors.SSCursor)
    cur2=get_connect()
    cmd='select id, original_uid from %s' %tblname
    cur.execute(cmd)
    f_err = open('./err.txt','a')
    err_uids=set()
    visited=set()

    while True:
        info = cur.fetchone()
        if not info:
            print 'over'
            break
        uid, orguid = info[0],info[1]
        if uid in visited:
            continue
        if uid in err_uids or orguid in err_uids:
            continue
        try:
            nfol = get_follow(cur2, uid, date_limit) 
            org_nfol = get_follow(cur2, orguid) 
            wrong = False
            for n,Id in (zip((nfol,org_nfol),(uid,orguid))):
                if n<0:
                    err_uids.add(Id)
                    wrong = True
                break
            if wrong:
#                raw_input('wrong: %s, %s' %(uid, orguid))
                continue
        except Exception,e:
            f_err.write('%s,%s,%s\n' %(uid,orguid,e))
            continue
        if nfol < org_nfol or (nfol>0 and random.uniform(0, 1) < org_nfol/float(nfol)):
            print uid#, nfol, orguid, org_nfol 
            visited.add(uid)    #memory error
    f_err.close()
    f=open('./err_uids.txt','a')
    for Id in err_uids:
        f.write('%s\n' %Id)
    f.close()

def candidate_by_profile():
#    cur=get_connect(MySQLdb.cursors.SSCursor)
    cur2=get_connect()#MySQLdb.cursors.SSCursor)

#    cmd='select id, followers_count from Weibo_User_Profile'
#    cur.execute(cmd)
    f_err = open('./err.txt','a')
    f=open('./uid_nfol.txt')
    for l in f:
        uid, nfol = [int(i) for i in l.strip().split()]
        try:
            #cmd2= 'select original_uid from Weibo_User_Relationship where id=%d and original_uid>rand()*10000000000 limit 1' %uid
            cmd2='select original_uid from Weibo_User_Relationship where id=%d limit 1' %uid

            cur2.execute(cmd2)
            res = cur2.fetchone()
            if not res:
                continue
            orguid=res[0]
            org_nfol = get_follow(cur2,orguid) 
            for n,Id in (zip((nfol,org_nfol),(uid,orguid))):
                if n<0:
                    continue
        except Exception,e:
            f_err.write('%s,%s,%s\n' %(uid,orguid,e))
            continue
        if nfol < org_nfol or (nfol>0 and random.uniform(0, 1) < org_nfol/float(nfol)):
            print uid#, nfol, orguid, org_nfol 
    f_err.close()
    f.close()         
    
def filter_lasttweet(fname='./out_new2.txt'):
    cur=get_connect()
    f=open(fname)
    for l in f:
        uid = l.strip()    
        cmd = 'select 1 from Weibo_User_Profile where id=%s and last_tweet_publish_time>"%s" limit 1' %(uid, date_limit)
        cur.execute(cmd)
        res = cur.fetchone()
        print uid,',', res and 1 or 0

def copy_dbrow(fname):
    cur=get_connect()
    f=open(fname)
    for l in f:
        uid = int(l.strip())
        cmd = 'insert ignore into Weibo_filter_User_Profile (select * from Weibo_User_Profile_%d where id=%d)' %(uid%10, uid)
        cur.execute(cmd)
        cur.connection.commit()


if __name__ == '__main__':
    candidates()
    """
    fname=sys.argv[1]
    print fname
#    filter_lasttweet(fname)
    copy_dbrow(fname)
    """

#nohup python tmysql.py > out.txt &
