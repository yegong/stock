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

CREATE TABLE `stock_k_line_days` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`symbol` varchar(32) NOT NULL,
	`day` date NOT NULL,
	`open_price` decimal(15,4) NOT NULL,
	`close_price` decimal(15,4) NOT NULL,
	`low_price` decimal(15,4) NOT NULL,
	`high_price` decimal(15,4) NOT NULL,
	`delta_price` decimal(15,4) NOT NULL,
	`turn_rate` decimal(15,4) NOT NULL,
	`delta_percent` decimal(15,4) NOT NULL,
	`volume` decimal(20,2) NOT NULL,
	`ma5` decimal(15,4) NULL,
	`ma10` decimal(15,4) NULL,
	`ma20` decimal(15,4) NULL,
	`ma30` decimal(15,4) NULL,
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE KEY `ux_symbol_day` (`symbol`, `day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
