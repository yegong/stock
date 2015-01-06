CREATE TABLE `stocks` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`symbol` varchar(32) NOT NULL,
	`name` varchar(32) NOT NULL,
	`market` varchar(8) NOT NULL,
	`catelog` varchar(24) NOT NULL,
	`xq_category` varchar(24) NULL,
	`zjh_category` varchar(24) NULL,
	`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE KEY `ux_symbol` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `stock_days` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`symbol` varchar(32) NOT NULL,
	`day` date NOT NULL,
	`open_price` decimal(10,2) NOT NULL,
	`close_price` decimal(10,2) NOT NULL,
	`high_price` decimal(10,2) NOT NULL,
	`low_price` decimal(10,2) NOT NULL,
	`volumn` decimal(10,2) NOT NULL,
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE KEY `ux_symbol_day` (`symbol`, `day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
