# coding=utf-8


import os, sys
#sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.split(os.getcwd())[0])
sys.path.insert(0, os.path.split(os.path.split(os.getcwd())[0])[0])

from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
from utils import *
from conf import *
from django.db import DatabaseError, IntegrityError, transaction
import MySQLdb


class Base(object):
    def __init__(self, client):
        self.cursor = None
        self.nowtime = datetime.datetime.now()
        self.lastupdate = datetime.datetime.min
        self._get_cursor()
        if client:
            self.client = client
        else:
            self.client = set_client(self.cursor)
        
    def execute_sql(self, sql, params=()):
        # 执行sql语句 当连接超时 自动重新连接重新执行
        for i in range(3):
            try:
                self.cursor.execute(sql, params)
                return
            except (MySQLdb.OperationalError, MySQLdb.InterfaceError), e:
                if self.cursor:
                    print self.cursor.messages
                # print 'num: %s db errer:%s %s'%(i, sql, e)
                self.cursor.close()
                self.cursor = get_connect()

    def username(self, uid):
        namesql = 'select screen_name from ' + TASKLIST_TABLE + ' where uid=%s'
        self.execute_sql(namesql, (uid, ))
        name = self.cursor.fetchone()
        if name: return name[0]
        self.client, usershow = loop_get_data(self.client, 'users__show', 'id', uid=uid)
        screen_name = usershow.get('screen_name', '')
        return screen_name
    
    def get_weiboid(self, querymid, wtype=1):
        self.client, weiboid = loop_get_data(self.client, 'statuses__queryid', 'id', mid=querymid, type=wtype, isBase62=1)
        try:
            weiboid = weiboid.get('id')
        except:
            return None
        weiboid = None if weiboid in ['-1', -1] else weiboid
        return weiboid

    def get_source(self, source):
        source = re.findall('<\S*a.*?>(.*?)<', source)
        if source:
            return source[0]
        return ''

    def get_normal_text(self, text):
        # 格式化字符串，去掉4字节的utf-8编码字符
        text_repr = repr(text)
        if text_repr.find('\\U000') != -1:
            text = re.sub('(\\\\U000\w+)', '', text_repr)
            text = eval(text)
            return text
        else:
            return text
        
    def _get_cursor(self):
        if not self.cursor:
            self.cursor = get_connect()
                
    def insertDB(self, tablename, dic):
        cmd = 'insert into %s (%s) value (%s)' % (tablename,
                    ','.join(dic.keys()), ','.join(('%s',) * len(dic)))
        dataexist = False
        try:
            self.execute_sql(cmd, dic.values())
            self.cursor.connection.commit()
            transaction.commit_unless_managed()
        except (MySQLdb.IntegrityError, IntegrityError), e:
            dataexist = True
            self.cursor.connection.rollback()
            transaction.rollback_unless_managed()
        except Exception, e:
            traceback.print_exc()
            print 'insert db error. dic:', str(dic)
            self.cursor.connection.rollback()
            transaction.rollback_unless_managed()
        return dataexist
