# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import os
import xlwt
from twisted.enterprise import adbapi
import MySQLdb.cursors

# import codecs
# gOutf = codecs.open('./out.data', 'w', encoding='utf-8')

class XlsPipeline(object):

    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('data')
        self.keys = ['url', 'title', 'desc', 'replys']
        self.create_headrow()
    
    def create_headrow(self):
        self.nrow = self.sheet.get_rows()
        if self.nows > 0:
            return
        for i, k in enumerate(self.keys):
            self.sheet.write(self.nrow, i, k)
        self.nrow += 1
                        
    def process_item(self, item, spider):
        for i, k in enumerate(self.keys):
            self.sheet.write(self.nrow, i, item.get(k, ''))
        self.workbook.save('%s.out.xls' % os.getpid())
        self.nrow += 1
        return item
    
    def __del__(self):
        print 'save workbook'
        self.workbook.save('%s.out.xls' % os.getpid())

class SQLStorePipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='crawl_cic',
                user='root', passwd='12345', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

         
class SQLiteStorePipeline(object):
    filename = 'data.sqlite'
    
    def __init__(self):
        from scrapy.core import signals
        from scrapy.xlib.pydispatch import dispatcher
        
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
 
    def process_item(self, item, spider):
        self.conn.execute('insert into question values(?,?,?,?)',
                          (item.url, item.title, item.desc, item.replys))
        return item
 
    def initialize(self):
        if os.path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
 
    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table question
                     (url primary key, title, desc, replys)""")
        conn.commit()
        return conn
    
