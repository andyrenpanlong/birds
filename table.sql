-- 创建相关数据库
CREATE TABLE if not EXISTS `spider`.`birds` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bird_name` varchar(128) DEFAULT NULL,
  `url` varchar(128) DEFAULT NULL,
  `num` varchar(45) DEFAULT NULL,
  `date_time` varchar(45) DEFAULT NULL,
  `author` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE if not EXISTS `spider`.`detail_1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(128) DEFAULT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `second_name` varchar(128) DEFAULT NULL,
  `bird_type` varchar(45) DEFAULT NULL,
  `descript` varchar(4096) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE if not EXISTS `spider`.`detail_2` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(128) DEFAULT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `second_name` varchar(128) DEFAULT NULL,
  `bird_type` varchar(45) DEFAULT NULL,
  `descript` varchar(4096) DEFAULT NULL,
  `img_url` varchar(1280) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE if not EXISTS `spider`.`pic_message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `keywords_1` varchar(128) DEFAULT NULL,
  `assetId` varchar(128) DEFAULT NULL,
  `category` varchar(128) DEFAULT NULL,
  `comName` varchar(128) DEFAULT NULL,
  `reportAs` varchar(128) DEFAULT NULL,
  `sciName` varchar(128) DEFAULT NULL,
  `speciesCode` varchar(128) DEFAULT NULL,
  `userDisplayName` varchar(256) DEFAULT NULL,
  `userId` varchar(128) DEFAULT NULL,
  `countryCode` varchar(128) DEFAULT NULL,
  `countryName` varchar(128) DEFAULT NULL,
  `bird_name` varchar(128) DEFAULT NULL,
  `bird_imgs_url_480` varchar(128) DEFAULT NULL,
  `bird_imgs_url_640` varchar(128) DEFAULT NULL,
  `bird_imgs_url_900` varchar(128) DEFAULT NULL,
  `bird_imgs_url_1200` varchar(128) DEFAULT NULL,
  `bird_imgs_url_1800` varchar(128) DEFAULT NULL,
  `bird_imgs_url_2400` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


bird_name, url, date_time, author
url, first_name, second_name, bird_type, descript
url, first_name, second_name, bird_type, descript, img_url
pdata = [keywords, assetId, category, comName, reportAs, sciName, speciesCode, userDisplayName, userId, countryCode, countryName, bird_name, bird_imgs_url_480, bird_imgs_url_640, bird_imgs_url_900, bird_imgs_url_1200, bird_imgs_url_1800, bird_imgs_url_2400]
