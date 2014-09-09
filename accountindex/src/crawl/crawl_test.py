# coding=utf-8
# 爬取用户粉丝、关注数据

from crawl import Base
from utils import *
from conf import *


class CrawlTest(Base):
    # 爬取用户粉丝、关注信息
    def __init__(self, uid, client=None):
        Base.__init__(self, client)
        self.uid = uid
        self.table_name = FANS_TABLE + month_str()
    
    def save_user(self, tablename, weibouser, uidtags):
        dic = {}
        
        dic['uid'] = weibouser
        dic['src_uid'] = self.uid
        dic['tags'] = ' '.join(uidtags)
        dic['follow_time'] = datetime.datetime.now()
        return self.insertDB(tablename, dic)
        
    def get_tags(self, uids):
        self.client, weitags = loop_get_data(self.client, 'tags__tags_batch', uids=','.join(uids))
        if not weitags:
            return {}
        uidtags = {}
        for weitag in weitags:
            tags = weitag.get('tags', {})
            uidtag = [tag.values()[0] for tag in tags]
            uidtags[weitag['id']] = uidtag
        return uidtags
    
    def get_last_fans(self):
        sqlcmd = 'select DISTINCT(uid) from tasklist'
        self.execute_sql(sqlcmd)
        uids = self.cursor.fetchall()
        return [i[0] for i in uids]
    
    def get_fans(self):
        weiusers = self.get_last_fans()
        create_follow(self.cursor, self.table_name)
        cursor = 0  # API下标
        existnum = 0  # 数据库中存在数据条数
        n = 0
        while True:
            uids = []
            uidtags = {}
            if n % 20 == 0:
                uids = weiusers[n:n + 20]
                if uids:
                    uidtags.update(self.get_tags([str(i) for i in uids]))
                else: return
            n += 1
            for user, tag in uidtags.items():
                exist = self.save_user(self.table_name, user, tag)

if __name__ == '__main__':
    print 'Start!'
    process = CrawlTest('2240206400')
    process.get_fans()
    print 'Done!'
