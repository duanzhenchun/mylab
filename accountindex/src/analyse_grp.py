# coding=utf-8

import sys, os, datetime, time, ast
import traceback, re, json, itertools
from dateutil.relativedelta import relativedelta
from crawl import crawl
import zlib, struct
from operator import itemgetter, attrgetter
from utils import *
import repost

class Analyse(crawl.Base):
    def __init__(self, tid=None, kol=[]):
        self.cursor = get_connect()
        self.tid = tid
        self.kol = kol
        
    def __get_basic_info(self):
        findsql = '''select tid, uid, screen_name, text, followers_count, 
                            created_at, reposts_count from account_tweet where tid=%s'''
        self.execute_sql(findsql, (self.tid, ))
        info = self.cursor.fetchone()
        return info

    @benchmark(getcost=True)
    def _get_alldata(self, table_time):
        if not self.tid:
            return
        lastdata = table_time + relativedelta(months=-1)
        table_names = [INTERACT_TABLE + '_'.join((str(lastdata.year), str(lastdata.month))), ]
                      # INTERACT_TABLE + '_'.join((str(table_time.year), str(table_time.month)))]
        alldatas = []
        for table_name in table_names:
            datasql = '''select uid, screen_name, reposts_count, created_at, real_followers_count, id, pid from %s 
                                 where src_id="%s" and tasktype='reposts' ''' % (table_name, self.tid)
            self.execute_sql(datasql)
            alldata = self.cursor.fetchall()
            alldatas.extend(alldata)
        alldatas = sorted(alldatas, key=itemgetter(3))
        return alldatas
    
    def set_account_fans(self, allfans):
        accfans = {}
        for fans in allfans:
            accfans.setdefault(fans[1], set())
            accfans[fans[1]].add(fans[0])
        return accfans
    
    def get_follower_num(self, alldata):
        follwers_num = {}
        account_info = {}
        for info in alldata:
            follwers_num.update({info[0]:info[4]})
            if info[0] in self.kol:
                if account_info.has_key(info[0]): continue
                account_info[info[0]] = info[1:5]
        return follwers_num, account_info
    
    def get_total_fans(self, repostpath, follwers_num, uid):
        reposts = repostpath.get(uid, '')
        repost_user = reposts[-2]
        direct_num = 0
        indirect_num = 0
        direct_num += follwers_num.get(uid, 0)
        for user in repost_user:
            detail = repostpath.get(user)
            if detail:
                if user in self.kol: continue
            if repostpath.has_key(user):
                rec_direct, rec_indirect = self.get_total_fans(repostpath, follwers_num, user)
                indirect_num += rec_direct
                indirect_num += rec_indirect
            else:
                #direct_num += follwers_num.get(user, 0)
                indirect_num += follwers_num.get(user, 0)
        #print indirect_num, direct_num
        return direct_num, indirect_num
    
    def count_digit(self, dic):
        count = {}
        for i, j in dic.iteritems():
            count.setdefault(j, 0)
            count[j] += 1
        return count
    
    def get_exposure(self):
        query = 'select sum(exposure_count) from tweet_exposure where tid=%s'
        self.cursor.execute(query, (self.tid, ))
        res = self.cursor.fetchone()
        return  res[0] if res[0] else 0 
        
    def gen_repostdata(self, alldata):
        for i in alldata:
            # count, userid, user, txt, id, pid
            yield i[2], i[0], i[1], i[5], i[6]

    @benchmark(getcost=True)
    def dispose(self, table_time):
        info = self.__get_basic_info()
        if not info: return
        tid, uid, screen_name, text, follwers, created_at, reposts_count = info
        print 'analyse start, %s, %s' % (self.tid, uid)
        poster = screen_name if screen_name else str(uid)
        try:
            lastdata = table_time + relativedelta(months=-1)
            get_alldata_time, alldata = self._get_alldata(table_time)
        except Exception, e:
            print '获取数据，分析每个小时数据错误！ %s' % e
            
        if not alldata: return
        taskid = lastdata.strftime('%Y%m')
        follwers_num, account_info = self.get_follower_num(alldata)
        follwers_num.update({uid:follwers})
        account_info.update({uid:(screen_name, reposts_count, created_at, follwers)})
        analysis_time, (repostpath, maxlvl, lvlsum, topn) = repost.build(uid, poster, alldata, self.gen_repostdata)
        contribute = []
        
        direct_num, indirect_num = self.get_total_fans(repostpath, follwers_num, uid)
        contribute.append([uid, screen_name, reposts_count, direct_num, indirect_num])
        for top in topn:
            if top[1] == uid or top[1] in self.kol:
                direct_num, indirect_num = self.get_total_fans(repostpath, follwers_num, top[1])
                contribute.append([top[1], top[2], top[0], direct_num, indirect_num])
        alltotalnum = sum(follwers_num.values())
        exposure = self.get_exposure()
        if not exposure: exposure = alltotalnum * 0.12
        result = {'result':{}}
        result['lvlsum'] = lvlsum
        for con in contribute:
            c_name, c_repost, c_created, c_follower = account_info.get(con[0], ('', 0, '', 0))
            result['result'].setdefault(con[0], {})
            result['result'][con[0]]['name'] = con[1]
            result['result'][con[0]]['offer'] = con[2]
            result['result'][con[0]]['exposure'] = int(exposure)
            result['result'][con[0]]['created_at'] = format_datetime(c_created)
            result['result'][con[0]]['repost_num'] = c_repost
            owned, viral = con[3] * exposure / alltotalnum, con[4] * exposure / alltotalnum 
            result['result'][con[0]]['owned'] = int(round(owned))
            result['result'][con[0]]['viral'] = int(round(viral))
            
        import pprint
        pprint.pprint(result)
        
        cmd_str = '''uid=%s, screen_name=%s, weibo_created_at=%s, text=%s, followers_count=%s, 
                               reposts_count=%s, reckon_result=%s, lastupdatetime=%s '''
        text_data = [uid, screen_name, created_at, text, follwers, reposts_count, repr(result), datetime.datetime.now()]
        update_sql = 'insert into result set tid=%s, taskid=%s, ' + cmd_str + \
                        'on duplicate key update ' + cmd_str
        try:
            self.execute_sql(update_sql, tuple([self.tid, taskid] + text_data + text_data))
            self.cursor.connection.commit()
            #self.save_finishnum(taskid)
        except Exception, e:
            err = 'update result error : %s' % repr(e)
            print err
            #send_err_to_mail('update result error', err)
        self.cursor.close()
        return result
        
    def stat_dispose(self):
        result = self.dispose()
        update_sql = '''update resulit set table_name=%s, crawlnum=%s, get_all_date_time=%s, hour_date_time=%s, 
                            analysis_time=%s, draw_time=%s, get_index_time=%s, hotwords_time=%s, dispose_time=%s where runid=%s'''
        try:
            self.execute_sql(update_runtime_sql,
                             (self.table_name, crawlnum, get_alldata_time, hour_date_time,
                              analysis_time, draw_time, get_index_time, hotwords_time,
                              dispose_time, runid))
            self.cursor.connection.commit()
        except Exception, e:
            err = 'update run_time_statistics error : %s' % repr(e)
            print err
            send_err_to_mail('update run_time_statistics error', err)
        self.cursor.close()

def topnodes(topn, root, N=10):
    if not topn:
        return {}, []
    lst = topn[:N]
    dic = {}  # {parent:{uid:uname}}
    for i in lst:
        if i[0] >= repost.imagedraw.BIGNODE_LIMIT or i[1] == root:
            dic.setdefault(i[3], {})
            dic[i[3]][i[1]] = i[2]
    return dic, lst  # cut tails

def format_datetime(times):
    if isinstance(times, str):
        return str
    try:
        return times.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return ''

def get_between_date(now_time):
    lastdata = now_time + relativedelta(months=-1)
    return lastdata.replace(day=1), now_time.replace(day=1)
    
if __name__ == '__main__': 
    #2667224511 惠氏启赋会
    #1928244585 多美滋1000日计划
    #2242065150 巢妈团
    uids = [2667224511, 1928244585, 2242065150]
    #uids = [2242065150]
    cursor = get_connect()
    now = datetime.datetime.now().date()
    lastdate, nextdate = get_between_date(now)
    #kol = [1661647485, 1796604070, 2244959874, 1682168362, 1857570982, 3047610375,
    #       1659679980, 2097614922, 1661673967, 1784993260, 1792759374, 1654761757, 2163350734, 1890884784]
    for uid in uids:
        cmd = '''select  tid from account_tweet where date(created_at)>=%s and DATE(created_at)<%s and uid=%s'''
        cursor.execute(cmd, (lastdate, nextdate, uid))
        result = cursor.fetchall()
        kols = []
        #if uid == 2242065150: kols = kol
        for res in result:
            analyse = Analyse(res[0], kols)
            analyse.dispose(now)
    cursor.close()
    """
    kol = [1661647485, 1796604070, 2244959874, 1682168362, 1857570982, 3047610375,
           1659679980, 2097614922, 1661673967, 1784993260, 1792759374, 1654761757, 2163350734, 1890884784]
    now = datetime.datetime.now().date()
    analyse = Analyse(3638375812404693, kol)
    analyse.dispose(now)
    """
    