CREATE TABLE `stocks` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `symbol` varchar(32) NOT NULL,
	  `name` varchar(32) NOT NULL,
	  `market` varchar(8) NOT NULL,
	  `catelog` varchar(24) NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `ux_symbol` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
