-- MySQL dump 10.11
--
-- Host: localhost    Database: audiowikibeta
-- ------------------------------------------------------
-- Server version	5.0.45-Debian_1ubuntu3.3-log

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
-- Current Database: `audiowikibeta`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `audiowikibeta` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `audiowikibeta`;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL auto_increment,
  `key` int(2) default NULL,
  `description` longtext,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,1,'Test comments'),(6,2,'Stories');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL auto_increment,
  `key` int(2) NOT NULL,
  `skip_count` int(11) default '0',
  `time` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `commenter` varchar(20) default NULL,
  `description` longtext,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=127 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (32,1,14,'2009-07-11 15:59:33','Anonymous','Obama inauguration!'),(34,1,16,'2009-07-11 01:55:02','Anonymous','John McCain on Neda, an Iranian woman shot by a government sniper.'),(63,1,2,'2009-07-18 19:26:12','6305422481',NULL),(41,2,15,'2009-07-11 17:22:12','9082087783','A long time ago...'),(47,2,3,'2009-07-14 14:48:59','6095053297','Itinerary'),(92,52843,5,'2009-07-27 12:53:54','6095053297','continuation of conv. with graham'),(48,2,-1,'2009-07-14 20:46:59','6095053297','T'),(49,2,-3,'2009-07-15 03:26:35','6095053297','Th'),(61,1,7,'2009-07-18 15:18:33','6095053297',NULL),(60,1,6,'2009-07-18 09:33:29','pratik','Alexander Nehamas on Symposium'),(57,2,2,'2009-07-17 02:54:47','6095053297','This'),(67,2,2,'2009-07-19 01:42:33','2155006938',NULL),(64,1,2,'2009-07-18 19:32:18','6305422481','Test, how much information can you store?'),(65,1,4,'2009-07-18 19:37:59','6305422481',NULL),(66,2,1,'2009-07-19 01:30:21','2155006938',NULL),(62,1,6,'2009-07-18 15:30:50','pratik',NULL),(68,2,3,'2009-07-19 01:42:35','pratik',NULL),(59,2,1,'2009-07-17 13:52:03','6095053297','Boston'),(69,1,5,'2009-07-19 02:03:56','pratik','jiji'),(120,2008,-4,'2009-08-27 20:01:26','2395958156','Tess Liegeios\'s Summer'),(70,2,0,'2009-07-19 15:49:37','pratik',NULL),(71,2,1,'2009-07-19 15:54:22','pratik',NULL),(72,1,-1,'2009-07-20 20:15:09','6095053297',NULL),(83,2008,-70,'2009-07-24 02:05:13','6092409195','Nick Liu\'s Summer in Washington'),(74,1,1,'2009-07-21 18:33:52','6095053297','Test comment'),(84,2008,-46,'2009-07-24 02:49:41','Unavailable','Anish Sarma\'s Summer in Providence'),(81,2,1,'2009-07-23 21:00:50','4077010475',NULL),(85,2008,-94,'2009-07-24 15:21:31','6173248245','File Not Found'),(87,52843,7,'2009-07-26 18:38:59','pratik','First Post! About audio wiki!'),(88,52843,6,'2009-07-26 18:41:55','pratik','On a conversation with Will, Keshav, Najah and Liz'),(75,1,-1,'2009-07-22 21:48:40','6095053297','again'),(91,52843,6,'2009-07-27 12:53:04','6095053297','spoke to graham'),(93,52843,5,'2009-07-28 17:48:33','6173248245','Conv. with Krishna'),(94,52843,5,'2009-07-28 17:50:04','6173248245','cont. with Krishna'),(95,5243327,-1,'2009-07-29 04:39:07','6095053297','Inaugural Comment, Balloon Story'),(96,5243327,-1,'2009-07-29 04:43:00','8328634138','What if you were the only one in the world who could see?'),(97,5243327,0,'2009-07-29 05:40:23','6095053297','Audio Wiki can be used to release serial audio novels.'),(98,5243327,0,'2009-07-29 05:45:55','8328634138','Using voice actors, these stories could be access by the illiterate, those without internet access. You could even record them in any language.'),(100,52843,3,'2009-07-29 23:15:50','6095053297','With Adam testing out Audio Wikipedia'),(101,52843,5,'2009-07-30 05:12:00','6095053297','L o L'),(102,52843,5,'2009-07-30 05:16:51','6095053297','Thoughts on this summer'),(103,52843,-3,'2009-07-30 21:23:28','6095053297','Story from Margin of Safety'),(104,1,0,'2009-08-03 13:53:39','pratik',NULL),(105,1,0,'2009-08-03 14:17:18','pratik',NULL),(106,2455,1,'2009-08-07 13:43:35','4258828080','Bill\'s introduction to the forum'),(107,2455,1,'2009-08-07 13:44:12','4258828080','Bill\'s first comment'),(108,1,0,'2009-08-07 19:02:11','6173248245',NULL),(109,738475,-3,'2009-08-07 19:08:54','6095053297','What\'s up?'),(110,52843,0,'2009-08-12 16:20:54','3212528439',NULL),(111,52843,0,'2009-08-12 20:34:38','6095053297',NULL),(112,68742,0,'2009-08-18 00:09:42','pratik',NULL),(113,52843,0,'2009-08-18 01:12:24','6095053297','Latif and Arsha'),(114,2008,-74,'2009-08-18 01:20:51','6095053297','File Not Found'),(115,1,0,'2009-08-20 21:56:36','6095053297',NULL),(116,2008,-74,'2009-08-21 12:55:50','6095053297','File Not Found'),(117,52843,0,'2009-08-23 20:58:54','6095053297','Cabron numero uno'),(118,2008,-27,'2009-08-24 18:55:37','6173248245','Latif is at Lawrenceville (Demo from YouTube Video)'),(119,2008,-14,'2009-08-24 19:02:46','6173248245','Latif Alam\'s Summer in Boston'),(121,2008,-7,'2009-08-28 16:04:47','81339437899','Hiro Shimoto\'s Summer in Japan'),(122,2008,15,'2009-08-28 16:46:31','9176704548','Lizi Myers\' Summer'),(123,2455,2,'2009-09-01 18:08:53','6095053297','music file converted from lame'),(125,2455,-2,'2009-09-03 07:40:11','4258828080','just added comment'),(124,2,-1,'2009-09-03 07:22:22','4258828080',NULL),(126,2008,-1,'2009-09-03 16:49:27','2154601687',NULL);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `privateForums`
--

DROP TABLE IF EXISTS `privateForums`;
CREATE TABLE `privateForums` (
  `id` int(11) NOT NULL auto_increment,
  `forumKey` text,
  `introFileName` text,
  `name` text,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `privateForums`
--

LOCK TABLES `privateForums` WRITE;
/*!40000 ALTER TABLE `privateForums` DISABLE KEYS */;
INSERT INTO `privateForums` VALUES (3,'24473308','from-latif','Lawrenceville Stories \'08'),(4,'52843','from-latif','Latif\'s Audio Blog'),(5,'5243327','None','Latif and Ahmed\'s Story Ideas'),(7,'123','None','123'),(8,'2538308','None','Cleve \'08'),(9,'key','None','latif'),(10,'6095053297','None','name'),(11,'1234','None','ali'),(12,'1234251','None','ali'),(13,'556867','None','Lotor'),(14,'2526','None','Alam Blog'),(15,'2455','None','Bill\'s Forum'),(16,'738475','None','Seth\'s Blog'),(17,'68742','None','Music'),(18,'27742','None','Arsha\'s Blog'),(19,'2008','None','Class of 2008'),(20,'869','None','vox'),(21,'546626','None','Kinnan'),(22,'546626','None','Kinnan');
/*!40000 ALTER TABLE `privateForums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL auto_increment,
  `phone_number` varchar(20) default NULL,
  `thread_cursor` varchar(4000) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'pratik','1:34,2455:107,24473308:84,52843:103,'),(2,'6095053297','738475:109,2455:107,2008:119,24473308:84,52843:88,'),(3,'6093693557','2:25,'),(4,'unavailable','2008:119,52843:103,'),(5,'2155007386','1:60,2008:122,24473308:80,'),(6,'6093332184','1:30,2008:119,'),(7,'Anonymous','2008:121,24473308:78,'),(8,'9082087783','1:40,2008:119,'),(9,'2155006938',NULL),(10,'4258828080','1:56,2455:125,2:124,'),(11,'3012725861','1:34,'),(12,'3212528439',NULL),(13,'7704719775',NULL),(14,'6305422481',NULL),(15,'6174919700',NULL),(22,'4848884762','24473308:85,'),(16,'9173744299',NULL),(17,'4077010475','2:47,'),(18,'6099471643','2008:122,24473308:78,'),(19,'6092409195','24473308:83,'),(20,'6172538879','24473308:84,'),(21,'6173248245','2455:107,2008:122,2:66,52843:103,'),(23,'9148067277','24473308:85,'),(24,'8328634138','5243327:96,'),(25,'9879565765',NULL),(26,'6098655111','2008:122,24473308:83,'),(27,'8458536993','2008:119,'),(28,'2395958156','2008:122,'),(29,'6095326976','2008:120,'),(30,'6099379227','2008:83,'),(31,'3473871391','2008:120,'),(32,'2524129270','2008:118,'),(33,'6098658314','2008:120,'),(34,'6099475318','2008:83,'),(35,'3025286424','2008:120,'),(36,'7786687281','2008:120,'),(37,'6095774598','2008:120,'),(38,'6176975100','2008:120,'),(39,'7039660560','2008:120,'),(40,'6177174240','2008:120,'),(41,'6462963921','2008:120,'),(42,'5302191230','2008:121,2:48,'),(43,'6098656455','2008:122,'),(44,'81339437899','2008:83,'),(45,'9176704548','2008:121,'),(46,'2176528547','2008:122,'),(47,'9083048493','2008:122,'),(48,'6092161647','2008:122,'),(49,'6094391629','2008:122,'),(50,'2154601687','2008:126,'),(51,'2178999077','2008:122,'),(52,'2154992470','2008:122,'),(53,'2035244405','2008:121,'),(54,'6092404987','2008:122,'),(55,'8477320995','2008:83,'),(56,'5717650263',NULL),(57,'9143840417','2008:122,'),(58,'2032730298','2008:122,'),(59,'2154992758','2008:122,'),(60,'9175457683','2008:122,');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2009-09-03 20:41:49
