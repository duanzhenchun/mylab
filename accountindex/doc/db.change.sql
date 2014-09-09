#2013-05-17
# whille

use accountindex;

CREATE TABLE `fans` (
  `uid` bigint(20) NOT NULL COMMENT '用户ID',
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
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `direct_at` (
  `tid` bigint(20) NOT NULL COMMENT 'tweet ID',
  `uid` bigint(20) NOT NULL,
  `target_uid` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `is_question` tinyint(1) DEFAULT NULL,
  `response_time` datetime DEFAULT NULL COMMENT 'account response time',
  `finish_num` int(11) DEFAULT 0 COMMENT 'last time crawled number',
  `text` varchar(1000) DEFAULT NULL,
  `raw_data` text COMMENT '原始数据',
  `response_raw_data` text COMMENT 'response tweet',
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `account_tweet` (
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
  `taskerr` varchar(500) DEFAULT NULL COMMENT '任务出错信息',
  `crawl_created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `lastupdatetime` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`tid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `account_growth` (
  `uid` bigint(20) DEFAULT NULL,
  `day` date DEFAULT NULL,
  `followers_count` int(11) DEFAULT '0',
  `friends_count` int(11) DEFAULT '0',
  `statuses_count` int(11) DEFAULT '0',
  PRIMARY KEY (`uid`, `day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `report` (
  `uid` bigint(20) NOT NULL DEFAULT '0',
  `day` date DEFAULT NULL,
  `period` varchar(64) DEFAULT NULL COMMENT 'weekly, monthly',
  `fans` int(11) DEFAULT NULL,
  `fan_growth` int(11) DEFAULT NULL,
  `tweets` int(11) DEFAULT NULL,
  `retweets` int(11) DEFAULT NULL,
  `comments` int(11) DEFAULT NULL,
  `direct_at` int(11) DEFAULT NULL,
  `impressions` int(11) DEFAULT NULL,
  `er_30` float(9,2) DEFAULT NULL,
  `er_7` float(9,2) DEFAULT NULL,
  `top_posts` varchar(1000) DEFAULT NULL,
  `top_influencers` varchar(1000) DEFAULT NULL,
  `top_hashtags` varchar(1000) DEFAULT NULL,
  `questions` int(11) DEFAULT NULL,
  `responds` int(11) DEFAULT NULL,
  `mean_respond_time` int(11) DEFAULT NULL COMMENT 'in seconds',
  `active` float(9,2) DEFAULT NULL COMMENT '%',
  `interactive` float(9,2) DEFAULT NULL COMMENT '%',
  `verified_dist` varchar(100) DEFAULT NULL,
  `subfans_dist` varchar(1000) DEFAULT NULL,
  `province_dist` varchar(1000) DEFAULT NULL,
  `gender_dist` varchar(100) DEFAULT NULL,
  `age_dist` varchar(1000) DEFAULT NULL,
  `tag_dist` varchar(1000) DEFAULT NULL,
  `week_dist` varchar(1000) DEFAULT NULL,
  `hour_dist` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`uid`, `day`, `period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `account_lab` (
  `uid` bigint(20) DEFAULT NULL,
  `screen_name` varchar(50) DEFAULT NULL,
  `followers_count` int(11) DEFAULT '0',
  `friends_count` int(11) DEFAULT '0',
  `doc` MEDIUMTEXT DEFAULT NULL,
  `verified_type` int(11) DEFAULT NULL,
  `raw_data` text,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `original_tweets` (
  `tid` bigint(20) NOT NULL DEFAULT '0',
  `uid` bigint(20) DEFAULT NULL,
  `text` varchar(1000) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`tid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `word_dict` (
  `doc_w` varchar(100) DEFAULT NULL,
  `title_w` varchar(100) DEFAULT NULL,
  `p` float DEFAULT 0.0,
  PRIMARY KEY ( `doc_w`, `title_w`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
