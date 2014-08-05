# coding: utf-8

import sys
import MySQLdb
import copy

sys.path.append('../')
import settings


def get_connect():
    try:
        conn = MySQLdb.connect(host=settings.MYSQL_HOST, port=int(settings.MYSQL_PORT),
                               user=settings.MYSQL_USER, passwd=settings.MYSQL_PASS,
                               db=settings.MYSQL_DB, charset='utf8')
        cursor = conn.cursor()
        return cursor
    except Exception, e:
        print 'connect mysql error: %s' % e
        sys.exit()
       

class mysqlStorer(object):
    def __init__(self):
        self.cursor = get_connect()
    
    def __del__(self):
        self.cursor.close()

    def get1_DB(self, cmd):
        try:
            self.cursor.execute(cmd)
            res = self.cursor.fetchone()
            return res or None
        except Exception, e:
            print e
            return None
    
    def get_DB(self, cmd):
        self.cursor.execute(cmd)
        res = self.cursor.fetchall()
        return res

    def execute(self, cmd):
        self.cursor.execute(cmd)
        self.cursor.connection.commit() 
       
if __name__ == '__main__':
    pass

