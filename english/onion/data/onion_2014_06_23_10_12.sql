-- MySQL dump 10.14  Distrib 5.5.32-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: onion
-- ------------------------------------------------------
-- Server version	5.5.30

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
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `email` varchar(75) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_4aacde5e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (1,2,'whille02@163.com',1,1),(2,1,'whille@163.com',1,1),(3,3,'whille.wang@cicdata.com',1,1),(4,4,'zg.whille@gmail.com',1,1),(5,5,'meng3r@qq.com',1,1);
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_address_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `sent` datetime DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirmation_a659cab3` (`email_address_id`),
  CONSTRAINT `email_address_id_refs_id_6ea1eea3` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
INSERT INTO `account_emailconfirmation` VALUES (1,1,'2014-06-16 03:02:25','2014-06-16 03:02:30','eb66479dab3f7d020ee15eef7e7542f86778739e4aa9e6b7afc3c413529d51dc'),(2,2,'2014-06-16 12:24:02','2014-06-16 12:24:08','2323006a07d0494776e0da9c286bed37db7ea6670385be40603409eb5473bd20'),(3,2,'2014-06-16 13:04:44','2014-06-16 13:04:49','8c6de38bcb8ea872fffc7b4becea9ae213919ea5cbf98b13dbc2359447435d73'),(4,3,'2014-06-16 13:07:44','2014-06-16 13:07:50','d5ce1756c3f7ba5b18590a4fe1982bba2cf1696f71ffb085cba4fcfa91408fb8'),(5,3,'2014-06-16 13:11:46','2014-06-16 13:11:51','8b9f51c0fb9847090cb53599aef5f6c14c3e8fb1d738e8fb4a4471668bcb5c8b'),(6,4,'2014-06-16 14:09:37','2014-06-16 14:09:44','519ba70d51d50f60160fb72168c7e99320d2a16ff2627cbff0cca1aa6210e238'),(7,5,'2014-06-21 12:02:53','2014-06-21 12:02:59','633fc5b746bc942fc610dcda7a6b592dc005290528b1199c194327011721c898');
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add captcha store',7,'add_captchastore'),(20,'Can change captcha store',7,'change_captchastore'),(21,'Can delete captcha store',7,'delete_captchastore'),(22,'Can add email address',8,'add_emailaddress'),(23,'Can change email address',8,'change_emailaddress'),(24,'Can delete email address',8,'delete_emailaddress'),(25,'Can add email confirmation',9,'add_emailconfirmation'),(26,'Can change email confirmation',9,'change_emailconfirmation'),(27,'Can delete email confirmation',9,'delete_emailconfirmation'),(28,'Can add social app',10,'add_socialapp'),(29,'Can change social app',10,'change_socialapp'),(30,'Can delete social app',10,'delete_socialapp'),(31,'Can add social account',11,'add_socialaccount'),(32,'Can change social account',11,'change_socialaccount'),(33,'Can delete social account',11,'delete_socialaccount'),(34,'Can add social token',12,'add_socialtoken'),(35,'Can change social token',12,'change_socialtoken'),(36,'Can delete social token',12,'delete_socialtoken'),(37,'Can add open id store',13,'add_openidstore'),(38,'Can change open id store',13,'change_openidstore'),(39,'Can delete open id store',13,'delete_openidstore'),(40,'Can add open id nonce',14,'add_openidnonce'),(41,'Can change open id nonce',14,'change_openidnonce'),(42,'Can delete open id nonce',14,'delete_openidnonce'),(43,'Can add log entry',15,'add_logentry'),(44,'Can change log entry',15,'change_logentry'),(45,'Can delete log entry',15,'delete_logentry'),(46,'Can add document',16,'add_document'),(47,'Can change document',16,'change_document'),(48,'Can delete document',16,'delete_document');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$10000$hmIaDIgIEH5N$yuSVRE7qkzCTtV03K+uwtuMqdJDYbhVLF1tDlNMUYXg=','2014-06-19 13:28:40',1,'root','','','whille@163.com',1,1,'2014-06-15 01:42:01'),(2,'!','2014-06-16 03:02:51',0,'whille.github','','','whille02@163.com',0,1,'2014-06-16 03:02:00'),(3,'pbkdf2_sha256$10000$DMKiVDoy9UUi$y4Ejq9Vm7XuN1zjWO4UFPDRYfP9xVn3ULm8OC5Fmun4=','2014-06-17 21:52:59',0,'whille.cicdata','','','whille.wang@cicdata.com',0,1,'2014-06-16 13:07:43'),(4,'pbkdf2_sha256$10000$XqrK8dysdd4h$jQvyBtDCDwvbs9cKzD/Dv5omurN8nuoWdrbgnsAjxZQ=','2014-06-18 21:42:36',0,'zg.whille','','','zg.whille@gmail.com',0,1,'2014-06-16 14:09:36'),(5,'pbkdf2_sha256$10000$cq4n92yQLpl0$kvho/RVsNGriIgjrwIwPHQxmGVxhCCXMhOocpvcnxVM=','2014-06-21 12:13:10',0,'meng3r','','','meng3r@qq.com',0,1,'2014-06-21 12:02:52');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `captcha_captchastore`
--

DROP TABLE IF EXISTS `captcha_captchastore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `captcha_captchastore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha_captchastore`
--

LOCK TABLES `captcha_captchastore` WRITE;
/*!40000 ALTER TABLE `captcha_captchastore` DISABLE KEYS */;
INSERT INTO `captcha_captchastore` VALUES (17,'EULZ','eulz','9a870c6756965830652139f0c29526f54c7da45c','2014-06-17 11:30:13');
/*!40000 ALTER TABLE `captcha_captchastore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2014-06-16 02:47:29',1,10,'1','github onion',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'captcha store','captcha','captchastore'),(8,'email address','account','emailaddress'),(9,'email confirmation','account','emailconfirmation'),(10,'social app','socialaccount','socialapp'),(11,'social account','socialaccount','socialaccount'),(12,'social token','socialaccount','socialtoken'),(13,'open id store','openid','openidstore'),(14,'open id nonce','openid','openidnonce'),(15,'log entry','admin','logentry'),(16,'document','src','document');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2l9w9idouedzqk91bta4ppbmf8lzz876','NmFiNTI4MTFlNmRhMjQzZjhjNTU4YjY4NWEyYmQ5NTI1ZTlhYTkwZTqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVTNhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEFVRZhY2NvdW50X3ZlcmlmaWVkX2VtYWlsTnUu','2014-07-05 12:13:10'),('56x7rmgx9vyu00dlfpnwkgfnag877x4a','NjUxNDI2ZGI3Yjg4YjZkYjZhOTM5ODE2NTIxZWUxMzY4YzU2NDgxMDqAAn1xAShYDwAAAF9zZXNzaW9uX2V4cGlyeXECSoCvGwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVTNhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmRxBFUNX2F1dGhfdXNlcl9pZHEFigEBdS4=','2014-07-10 13:28:40'),('58thmrgrd7gfom07z6nugkimeyh2vcsg','YmY0NDI3YThiOTdhMzgzNjViZjU3NDJlMTg5OGEwZTg0ZGZmYTU4ZTqAAn1xAShYDwAAAF9zZXNzaW9uX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVTNhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmRxBFUNX2F1dGhfdXNlcl9pZHEFigEEdS4=','2014-06-30 22:44:32'),('8m2jafblzowil0jefmnl8zd7h2od4rvu','MGJjODYwYjJlYTAxYjQ4ZWY5NWZmMDUzMzNjMTMzYzlhZWM1YmM4MTqAAn1xAShYDwAAAF9zZXNzaW9uX2V4cGlyeXECSoCvGwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVTNhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmRxBFUNX2F1dGhfdXNlcl9pZHEFigEEdS4=','2014-07-08 21:58:18'),('dsi95tqmwamlt87a4mg0y0e3zuosucty','MGJjODYwYjJlYTAxYjQ4ZWY5NWZmMDUzMzNjMTMzYzlhZWM1YmM4MTqAAn1xAShYDwAAAF9zZXNzaW9uX2V4cGlyeXECSoCvGwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVTNhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmRxBFUNX2F1dGhfdXNlcl9pZHEFigEEdS4=','2014-07-09 21:42:36'),('el29tek4909xht209pagl9rmy0bejq2g','OTMwMzhkYTMxZjhlNzZlMDk3N2JjZTQ3YTgyNDdkYjU1NTVmMzEwNDqAAn1xAShYDwAAAF9zZXNzaW9uX2V4cGlyeXECSoCvGwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVTNhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmRxBFUNX2F1dGhfdXNlcl9pZHEFigEDVRNzb2NpYWxhY2NvdW50X3N0YXRlfXEGVQdwcm9jZXNzWAUAAABsb2dpbnNYDAAAAEZBckFucHo3aElGdIZ1Lg==','2014-07-08 21:52:59'),('jepky0mp7g95pw6gjwttiaq8k1yphmzf','ZWE2MDExMGI0Y2FhODBhZTNjM2ExYTA2NjE2YjljNjYxZDAwNTIxMjqAAn1xAS4=','2014-06-29 13:05:42'),('yjghmv88vqg9cf3tuwmehmprxoo3qs5t','ZTEyYTIwMzZlOWRlMjkwYmYyYjMxMTZkNmE3NWE1NmFlMTQzODg0ZjqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==','2014-06-30 01:54:29');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `openid_openidnonce`
--

DROP TABLE IF EXISTS `openid_openidnonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `openid_openidnonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(255) NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `openid_openidnonce`
--

LOCK TABLES `openid_openidnonce` WRITE;
/*!40000 ALTER TABLE `openid_openidnonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `openid_openidnonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `openid_openidstore`
--

DROP TABLE IF EXISTS `openid_openidstore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `openid_openidstore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` longtext NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `openid_openidstore`
--

LOCK TABLES `openid_openidstore` WRITE;
/*!40000 ALTER TABLE `openid_openidstore` DISABLE KEYS */;
/*!40000 ALTER TABLE `openid_openidstore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `provider` varchar(30) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  `extra_data` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `provider` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_b4f0248b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
INSERT INTO `socialaccount_socialaccount` VALUES (1,2,'github','1240846','2014-06-16 03:02:25','2014-06-16 03:02:25','{\"public_repos\": 4, \"site_admin\": false, \"subscriptions_url\": \"https://api.github.com/users/whille/subscriptions\", \"gravatar_id\": \"93e1a384b2b30b5a3d58496037447c0b\", \"hireable\": false, \"id\": 1240846, \"followers_url\": \"https://api.github.com/users/whille/followers\", \"following_url\": \"https://api.github.com/users/whille/following{/other_user}\", \"blog\": \"whille\", \"followers\": 1, \"location\": \"beijing\", \"type\": \"User\", \"email\": \"whille@163.com\", \"bio\": null, \"gists_url\": \"https://api.github.com/users/whille/gists{/gist_id}\", \"company\": \"web\", \"events_url\": \"https://api.github.com/users/whille/events{/privacy}\", \"html_url\": \"https://github.com/whille\", \"updated_at\": \"2014-06-14T10:42:50Z\", \"received_events_url\": \"https://api.github.com/users/whille/received_events\", \"starred_url\": \"https://api.github.com/users/whille/starred{/owner}{/repo}\", \"public_gists\": 2, \"name\": \"whille\", \"organizations_url\": \"https://api.github.com/users/whille/orgs\", \"url\": \"https://api.github.com/users/whille\", \"created_at\": \"2011-12-05T03:54:39Z\", \"avatar_url\": \"https://avatars.githubusercontent.com/u/1240846?\", \"repos_url\": \"https://api.github.com/users/whille/repos\", \"following\": 1, \"login\": \"whille\"}');
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(100) NOT NULL,
  `secret` varchar(100) NOT NULL,
  `key` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
INSERT INTO `socialaccount_socialapp` VALUES (1,'github','github onion','8ef4e9893c45adb09fef','848336580c884a527ef9d74a365e23dccdd6f7f1','');
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialapp_id` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_f2973cd1` (`socialapp_id`),
  KEY `socialaccount_socialapp_sites_99732b5c` (`site_id`),
  CONSTRAINT `socialapp_id_refs_id_e7a43014` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `site_id_refs_id_05d6147e` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
INSERT INTO `socialaccount_socialapp_sites` VALUES (1,1,1);
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_id` (`app_id`,`account_id`),
  KEY `socialaccount_socialtoken_60fc113e` (`app_id`),
  KEY `socialaccount_socialtoken_93025c2f` (`account_id`),
  CONSTRAINT `account_id_refs_id_1337a128` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `app_id_refs_id_edac8a54` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
INSERT INTO `socialaccount_socialtoken` VALUES (1,1,1,'3476dfb0c9c699887b60f92de4b708fa24f98538','',NULL);
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `src_document`
--

DROP TABLE IF EXISTS `src_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `src_document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `docfile` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `src_document`
--

LOCK TABLES `src_document` WRITE;
/*!40000 ALTER TABLE `src_document` DISABLE KEYS */;
INSERT INTO `src_document` VALUES (2,'4:gone_with_the_wind.txt','documents/gone_with_the_wind.txt');
/*!40000 ALTER TABLE `src_document` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-06-23 10:12:53
