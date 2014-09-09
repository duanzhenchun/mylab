#coding=utf-8

import ast
import crawl
from utils import get_connect


def update(cursor, table_name):
    #cmd = 'select id, raw_data from %s where tasktype="reposts" and pid=0' % table_name 
    cmd = 'select id, raw_data from %s where tasktype="reposts" and followers_count is null limit 200' % table_name 
    cursor.execute(cmd)
    result = cursor.fetchall()
    for res in result:
        tid, raw_data = res
        raw_data = ast.literal_eval(raw_data)
        #pid = raw_data.get('pid', 0)
        followers_count = raw_data.get('user', {}).get('followers_count', 0)
        reposts_count = raw_data.get('reposts_count', 0)
        if followers_count or reposts_count:
            #insert_sql = 'update %s set pid=%s where id=%s'%(table_name, pid, tid)
            insert_sql = 'update %s set reposts_count=%s, followers_count=%s where id=%s' % \
                                        (table_name, reposts_count, followers_count, tid)
            try:
                cursor.execute(insert_sql)
                cursor.connection.commit()
            except Exception, e:
                print e
            print tid, followers_count, reposts_count

if __name__ == "__main__":
    cursor = get_connect()
    update(cursor, 'interact_tweet_2013_10')
    cursor.close()
    