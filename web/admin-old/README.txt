In a database called 'audiowikiIndia', there needs to be a comments table, created by the following script:

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL auto_increment,
  `skip_count` int(11) NOT NULL default '0',
  `time` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `user` text NOT NULL,
  `description` text,
  `archived` tinyint(1) NOT NULL default '1',
  `edited` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
