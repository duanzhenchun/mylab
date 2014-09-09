# coding=utf-8

import sys, MySQLdb
import settings
from django.db.backends.mysql.base import CursorWrapper
from conf import *


def get_connect():
    # 创建mysql连接
    try:
        conn = MySQLdb.connect(host=settings.dbhost, user=settings.dbuser, passwd=settings.dbpwd,
                               db=settings.dbname, port=int(settings.dbport), charset='utf8')
        cursor = conn.cursor()
        # return CursorWrapper(cursor)
        return cursor
    except Exception, e:
        print 'connect mysql error: %s' % e
        sys.exit()
        
def taskuids():
    """
    get uids of all account 
    """
    cursor = get_connect()
    sqlcmd = 'select uid from ' + TASKLIST_TABLE 
    cursor.execute(sqlcmd)
    res = cursor.fetchall()
    cursor.connection.close()
    uids = [i[0] for i in res]
    return uids

def get_last_table(cursor, prefix=FANS_TABLE):
    # 选择最后一个最新的表从中取数据
    create_new = False
    prefix += '20%'
    statussql = 'show table status from ' + settings.dbname + ' like %s'
    cursor.execute(statussql, (prefix,))
    dbstatus = cursor.fetchall()
    db_tasktables = {}
    for status in dbstatus:
        if status[4] != 0:
            db_tasktables[status[0]] = status[4]
    if not db_tasktables: return
    return sorted(db_tasktables)[-1]

def create_repost(cursor, table_name):
    # 新建原始数据表
    create_sql = '''CREATE TABLE IF NOT EXISTS `%s` (
                    `id` bigint(20) NOT NULL COMMENT '转发ID',
                    `src_uid` bigint(20) DEFAULT NULL COMMENT '发帖人ID',
                    `src_id` bigint(20) DEFAULT NULL COMMENT '被转发微博ID',
                    `uid` bigint(20) NOT NULL COMMENT '用户ID',
                    `screen_name` varchar(100) DEFAULT NULL COMMENT '转发人名称',
                    `pid` bigint(20) DEFAULT '0',
                    `created_at` datetime DEFAULT NULL COMMENT '转发时间',
                    `tasktype` VARCHAR(20) DEFAULT NULL COMMENT '任务类型 ',
                    `raw_data` text COMMENT '原始数据',
                    `lastupdatetime` datetime DEFAULT NULL COMMENT '最后一次更新时间',
                    `reposts_count` int(11) DEFAULT NULL,
                    `followers_count` int(11) DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    KEY `src_uid` (`src_uid`),
                    KEY `created_at` (`created_at`)
                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博原始数据表';
         ''' % table_name
    try:
        cursor.execute(create_sql)
    except:
        pass

def create_follow(cursor, table_name):
    # 创建粉丝原始数据表
    create_sql = '''CREATE TABLE  IF NOT EXISTS `%s` (
                           `uid` bigint(20) NOT NULL COMMENT '用户ID',
                           `src_uid` bigint(20) NOT NULL COMMENT '被关注用户ID',
                           `screen_name` varchar(100) DEFAULT NULL COMMENT '用户名称',
                           `province` int(11) DEFAULT NULL COMMENT '用户所在省级ID',
                           `city` int(11) DEFAULT NULL COMMENT '用户所在城市ID',
                           `location` varchar(150) DEFAULT NULL COMMENT '用户所在地',
                           `gender` varchar(5) DEFAULT NULL COMMENT '性别，m：男、f：女、n：未知',
                           `profile_url` varchar(100) DEFAULT NULL COMMENT '用户微博地址',
                           `weihao` varchar(50) DEFAULT NULL COMMENT '用户的微号',
                           `verified` tinyint(1) DEFAULT NULL COMMENT '是否是微博认证用户',
                           `verified_type` int(11) DEFAULT NULL,
                           `allow_all_act_msg` tinyint(1) DEFAULT NULL COMMENT '是否允许所有人给我发私信',
                           `created_at` datetime DEFAULT NULL COMMENT '用户创建（注册）时间',
                           `description` varchar(255) DEFAULT NULL COMMENT '描述',
                           `statuses_count` int(11) DEFAULT NULL COMMENT '微博数',
                           `friends_count` int(11) DEFAULT NULL COMMENT '关注数',
                           `followers_count` int(11) DEFAULT NULL COMMENT '粉丝数',
                           `favourites_count` int(11) DEFAULT NULL COMMENT '收藏数',
                           `tags` varchar(500) DEFAULT NULL COMMENT '用户tags',
                           `follow_time` datetime DEFAULT NULL COMMENT '开始关注的时间，这里用爬取到的时间表示',
                           PRIMARY KEY (`uid`, `src_uid`),
                           key `follow_time` (`follow_time`)
                           ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                           ''' % table_name
    try:
        cursor.execute(create_sql)
    except:
        pass

def create_tweet(cursor, table_name=ACCOUNT_TWEET_TABLE):
    create_sql = '''CREATE TABLE  IF NOT EXISTS `%s` (
                          `tid` bigint(20) NOT NULL DEFAULT '0' COMMENT '微博id',
                          `uid` bigint(20) DEFAULT NULL COMMENT '发微薄用户id',
                          `screen_name` varchar(50) DEFAULT NULL,
                          `hashtag` varchar(100) DEFAULT NULL,
                          `source` varchar(50) DEFAULT NULL,
                          `created_at` datetime DEFAULT NULL,
                          `text` varchar(1000) DEFAULT NULL,
                          `reposts_count` int(11) DEFAULT '0' COMMENT '转发数',
                          `reposts_finishnum` int(11) DEFAULT '0' COMMENT '完成任务数量',
                          `reposts_finishtype` tinyint(4) DEFAULT NULL COMMENT '完成任务类型 0为未开始 1为开始未完成 2为已完成 3为任务出错',
                          `comments_count` int(11) DEFAULT '0' COMMENT '评论数',
                          `comments_finishnum` int(11) DEFAULT '0',
                          `comments_finishtype` tinyint(4) DEFAULT NULL,
                          `attitudes_count` int(11) DEFAULT '0',
                          `taskerr` varchar(500) DEFAULT NULL COMMENT '任务出错信息',
                          `crawl_create_at` datetime DEFAULT NULL COMMENT '创建时间',
                          `lastupdatetime` datetime DEFAULT NULL COMMENT '最后更新时间',
                          PRIMARY KEY (`tid`),
                          KEY `uid` (`uid`),
                          key `created_at` (`created_at`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                         ''' % table_name
    try:
        cursor.execute(create_sql)
    except:
        pass
    
def create_exposure(cursor):
    create_sql = '''CREATE TABLE IF NOT EXISTS `%s` (
                    `tid` bigint(20) NOT NULL,
                    `uid` bigint(20) NOT NULL,
                    `day` date DEFAULT NULL,
                    `exposure_count` bigint(20) DEFAULT 0,
                    PRIMARY KEY (`uid`, `day`)
                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
         ''' % EXPOSURE_TALBE
    try:
        cursor.execute(create_sql)
    except:
        pass

def create_fans_activity(cursor):
    create_sql = '''CREATE TABLE IF NOT EXISTS `%s` (
                    `uid` bigint(20) NOT NULL,
                    `day` date NOT NULL,
                    `hour` int(2) NOT NULL,
                    `weekday` int(2) DEFAULT NULL,
                    `ori_postnum` bigint(10) DEFAULT 0,
                    `count` int(10) DEFAULT NULL,
                    PRIMARY KEY (`uid`, `day`, `hour`)
                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
         ''' % FANS_ACTIVITY_TABLE
    try:
        cursor.execute(create_sql)
    except:
        pass
