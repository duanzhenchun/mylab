-- MySQL dump 10.15  Distrib 10.0.12-MariaDB, for Linux (x86_64)
--
-- Host: 118.25.206.182    Database: WeiboPanel
-- ------------------------------------------------------
-- Server version	5.6.15-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Weibo_User_Profile`
--

DROP TABLE IF EXISTS `Weibo_User_Profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Weibo_User_Profile` (
  `id` bigint(20) NOT NULL DEFAULT '0',
  `idstr` varchar(300) DEFAULT NULL COMMENT '字符串型的用户UID',
  `screen_name` varchar(300) DEFAULT NULL COMMENT '用户昵称',
  `name` varchar(300) DEFAULT NULL COMMENT '友好显示名称',
  `province` int(11) DEFAULT NULL COMMENT '用户所在省级ID',
  `city` int(11) DEFAULT NULL COMMENT '用户所在城市ID',
  `location` varchar(100) DEFAULT NULL COMMENT '用户所在地',
  `description` varchar(2000) DEFAULT NULL COMMENT '用户个人描述',
  `url` varchar(500) DEFAULT NULL COMMENT '用户博客地址',
  `profile_image_url` varchar(200) DEFAULT NULL COMMENT '用户头像地址（中图），50×50像素',
  `profile_url` varchar(500) DEFAULT NULL COMMENT '用户的微博统一URL地址',
  `domain` varchar(500) DEFAULT NULL COMMENT '用户的个性化域名',
  `weihao` varchar(100) DEFAULT NULL COMMENT '用户的微号',
  `gender` varchar(6) DEFAULT NULL COMMENT '性别，m：男、f：女、n：未知',
  `followers_count` int(11) DEFAULT NULL COMMENT '粉丝数',
  `friends_count` int(11) DEFAULT NULL COMMENT '关注数',
  `statuses_count` int(11) DEFAULT NULL COMMENT '微博数',
  `favourites_count` int(11) DEFAULT NULL COMMENT '收藏数',
  `created_at` datetime DEFAULT NULL COMMENT '用户创建（注册）时间',
  `following` tinyint(1) DEFAULT NULL COMMENT '暂未支持',
  `allow_all_act_msg` tinyint(1) DEFAULT NULL COMMENT '是否允许所有人给我发私信，true：是，false：否',
  `geo_enabled` tinyint(1) DEFAULT NULL COMMENT '是否允许标识用户的地理位置，true：是，false：否',
  `verified` tinyint(1) DEFAULT NULL COMMENT '是否是微博认证用户，即加V用户，true：是，false：否',
  `verified_type` int(11) DEFAULT NULL COMMENT '暂未支持',
  `remark` varchar(300) DEFAULT NULL COMMENT '用户备注信息，只有在查询用户关系时才返回此字段',
  `allow_all_comment` tinyint(1) DEFAULT NULL COMMENT '是否允许所有人对我的微博进行评论，true：是，false：否',
  `avatar_large` varchar(200) DEFAULT NULL COMMENT '用户头像地址（大图），180×180像素',
  `avatar_hd` varchar(200) DEFAULT NULL COMMENT '用户头像地址（高清），高清头像原图',
  `verified_reason` varchar(500) DEFAULT NULL COMMENT '认证原因',
  `follow_me` tinyint(1) DEFAULT NULL COMMENT '该用户是否关注当前登录用户，true：是，false：否',
  `online_status` int(11) DEFAULT NULL COMMENT '用户的在线状态，0：不在线、1：在线',
  `bi_followers_count` int(11) DEFAULT NULL COMMENT '用户的互粉数',
  `lang` varchar(10) DEFAULT NULL COMMENT '用户当前的语言版本，zh-cn：简体中文，zh-tw：繁体中文，en：英语',
  `last_tweet_id` bigint(20) DEFAULT '0',
  `last_tweet_text` varchar(2000) DEFAULT NULL COMMENT '用户的最近一条微博内容',
  `last_tweet_source` varchar(100) DEFAULT NULL COMMENT '用户的最近一条微博来源',
  `last_tweet_publish_time` datetime DEFAULT NULL COMMENT '用户的最近一条微博发布时间',
  `last_tweet_rt` int(11) DEFAULT NULL COMMENT '用户的最近一条微博转发数',
  `last_tweet_ct` int(11) DEFAULT NULL COMMENT '用户的最近一条微博评论数',
  `last_tweet_attitudes` int(11) DEFAULT NULL COMMENT '用户的最近一条微博表态数',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Weibo_User_Profile_test`
--

DROP TABLE IF EXISTS `Weibo_User_Profile_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Weibo_User_Profile_test` (
  `id` bigint(20) NOT NULL DEFAULT '0',
  `idstr` varchar(300) CHARACTER SET utf8 DEFAULT NULL COMMENT '字符串型的用户UID',
  `screen_name` varchar(300) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户昵称',
  `name` varchar(300) CHARACTER SET utf8 DEFAULT NULL COMMENT '友好显示名称',
  `province` int(11) DEFAULT NULL COMMENT '用户所在省级ID',
  `city` int(11) DEFAULT NULL COMMENT '用户所在城市ID',
  `location` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户所在地',
  `description` varchar(2000) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户个人描述',
  `url` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户博客地址',
  `profile_image_url` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户头像地址（中图），50×50像素',
  `profile_url` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的微博统一URL地址',
  `domain` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的个性化域名',
  `weihao` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的微号',
  `gender` varchar(6) CHARACTER SET utf8 DEFAULT NULL COMMENT '性别，m：男、f：女、n：未知',
  `followers_count` int(11) DEFAULT NULL COMMENT '粉丝数',
  `friends_count` int(11) DEFAULT NULL COMMENT '关注数',
  `statuses_count` int(11) DEFAULT NULL COMMENT '微博数',
  `favourites_count` int(11) DEFAULT NULL COMMENT '收藏数',
  `created_at` datetime DEFAULT NULL COMMENT '用户创建（注册）时间',
  `following` tinyint(1) DEFAULT NULL COMMENT '暂未支持',
  `allow_all_act_msg` tinyint(1) DEFAULT NULL COMMENT '是否允许所有人给我发私信，true：是，false：否',
  `geo_enabled` tinyint(1) DEFAULT NULL COMMENT '是否允许标识用户的地理位置，true：是，false：否',
  `verified` tinyint(1) DEFAULT NULL COMMENT '是否是微博认证用户，即加V用户，true：是，false：否',
  `verified_type` int(11) DEFAULT NULL COMMENT '暂未支持',
  `remark` varchar(300) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户备注信息，只有在查询用户关系时才返回此字段',
  `allow_all_comment` tinyint(1) DEFAULT NULL COMMENT '是否允许所有人对我的微博进行评论，true：是，false：否',
  `avatar_large` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户头像地址（大图），180×180像素',
  `avatar_hd` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户头像地址（高清），高清头像原图',
  `verified_reason` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '认证原因',
  `follow_me` tinyint(1) DEFAULT NULL COMMENT '该用户是否关注当前登录用户，true：是，false：否',
  `online_status` int(11) DEFAULT NULL COMMENT '用户的在线状态，0：不在线、1：在线',
  `bi_followers_count` int(11) DEFAULT NULL COMMENT '用户的互粉数',
  `lang` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户当前的语言版本，zh-cn：简体中文，zh-tw：繁体中文，en：英语',
  `last_tweet_id` bigint(20) DEFAULT '0',
  `last_tweet_text` varchar(2000) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的最近一条微博内容',
  `last_tweet_source` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的最近一条微博来源',
  `last_tweet_publish_time` datetime DEFAULT NULL COMMENT '用户的最近一条微博发布时间',
  `last_tweet_rt` int(11) DEFAULT NULL COMMENT '用户的最近一条微博转发数',
  `last_tweet_ct` int(11) DEFAULT NULL COMMENT '用户的最近一条微博评论数',
  `last_tweet_attitudes` int(11) DEFAULT NULL COMMENT '用户的最近一条微博表态数',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Weibo_User_Relationship`
--

DROP TABLE IF EXISTS `Weibo_User_Relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Weibo_User_Relationship` (
  `id` bigint(20) DEFAULT NULL,
  `original_uid` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `access_token`
--

DROP TABLE IF EXISTS `access_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_token` (
  `uid` bigint(20) NOT NULL,
  `access_token` varchar(50) NOT NULL COMMENT '访问令牌',
  `refresh_token` varchar(50) DEFAULT NULL,
  `expires_in` int(11) DEFAULT NULL COMMENT '过期时间',
  `create_at` int(11) DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-29 12:36:51
