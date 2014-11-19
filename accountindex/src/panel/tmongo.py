import MySQLdb 
import random
import time

dbname = 'WeiboPanel'
dbpwd = 'cicdata'
dbhost, dbport, dbuser = '182.92.218.82', 3306, 'root'


def timestamp_int(dt):
        return int(time.mktime(dt.timetuple()))

Dic_nfol={}
Sql = {'friend_type': 1, 'projectid': 'BD13050057'}

def org_nfollow(col, uid):
    if uid not in Dic_nfol:
        sql = {'uid':uid}
        sql.update(Sql)
        user = col.find_one(sql)
        Dic_nfol[int(user['uid'])] = user['followers_count']
    return Dic_nfol[uid]

def candidates():
    cur=get_connect()
    cmd='select id, original_uid from Weibo_User_Relationship'
    db.cursor.execute(cmd)
    while True:
        info = db.cursor.fetchone()
        if not info:
            print 'over'
            break

    cur.execute(sql)
    col=db['Sina_User_Friend']
    for user in col.find(Sql):
        orguid, uid=[int(user[i]) for i in ('original_uid', 'uid')]
        nfol=user['followers_count'] 
        org_nfol = org_nfollow(col, orguid)
        if nfol < org_nfol or random.uniform(0, 1) < org_nfol/float(nfol):
            print uid#, nfol, orguid, org_nfol 
       
       
def get_connect():
    try:
        conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpwd,
                               db=dbname, port=int(dbport), charset='utf8')
        cursor = conn.cursor()
        return cursor
    except Exception, e:
        print 'connect mysql error: %s' % e
        sys.exit()
 
    
if __name__ == '__main__':
    candidates()
    #sample()

#python tmongo.py |tee out.txt
