CREATE TABLE `newusers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `exchange_id` varchar(255) DEFAULT NULL,
  `api_key` varchar(255) DEFAULT NULL,
  `secret` varchar(255) DEFAULT NULL,
  `password_app` varchar(255) DEFAULT NULL,
  `asset_name` varchar(255) DEFAULT NULL,
  `trade_type` varchar(255) DEFAULT NULL,
  `trade_size` float DEFAULT NULL,
  `timeframe` varchar(255) DEFAULT NULL,
  `indicator` varchar(255) DEFAULT NULL,
  `payment_status` varchar(255) DEFAULT NULL,
  `payment_amount` decimal(10, 2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
