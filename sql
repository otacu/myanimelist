CREATE TABLE `tb_myanimelist_anime` (
  `idx` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `anime_id` int(10) unsigned DEFAULT NULL COMMENT '动画的站内id',
  `en_name` varchar(255) DEFAULT NULL COMMENT '英文名',
  `jp_name` varchar(255) DEFAULT NULL COMMENT '日文名',
  `pic` varchar(255) DEFAULT NULL COMMENT '图片链接',
  `type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '播出类型',
  `episodes` int(10) unsigned DEFAULT NULL COMMENT '集数',
  `premiered` varchar(30) DEFAULT NULL COMMENT '首播时间',
  `producers` varchar(255) DEFAULT NULL COMMENT '制片方',
  `studios` varchar(255) DEFAULT NULL COMMENT '工作室',
  `source` varchar(255) DEFAULT NULL COMMENT '原作类型',
  PRIMARY KEY (`idx`),
  UNIQUE KEY `unique_anime_id` (`anime_id`) USING BTREE,
  KEY `index_en_name` (`en_name`) USING BTREE,
  KEY `index_jp_name` (`jp_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tb_myanimelist_anime_character` (
  `idx` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `anime_id` int(10) unsigned DEFAULT NULL COMMENT '动画的站内id',
  `anime_en_name` varchar(255) DEFAULT NULL COMMENT '动画英文名',
  `anime_jp_name` varchar(255) DEFAULT NULL COMMENT '动画日文名',
  `name` varchar(255) DEFAULT NULL COMMENT '动画角色名',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Main：主角，Supporting：配角',
  `voice_actor` varchar(255) DEFAULT NULL COMMENT '声优名',
  PRIMARY KEY (`idx`),
  UNIQUE KEY `unique_anime_id_and_name` (`anime_id`,`name`) USING BTREE,
  KEY `index_anime_en_name` (`anime_en_name`) USING BTREE,
  KEY `index_anime_jp_name` (`anime_jp_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tb_myanimelist_anime_staff` (
  `idx` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `anime_id` int(10) unsigned DEFAULT NULL COMMENT '动画的站内id',
  `anime_en_name` varchar(255) DEFAULT NULL COMMENT '动画英文名',
  `anime_jp_name` varchar(255) DEFAULT NULL COMMENT '动画日文名',
  `name` varchar(255) DEFAULT NULL COMMENT '名字',
  `roles` varchar(255) DEFAULT NULL COMMENT '职责',
  PRIMARY KEY (`idx`),
  UNIQUE KEY `unique_anime_id_and_name` (`anime_id`,`name`) USING BTREE,
  KEY `index_anime_en_name` (`anime_en_name`) USING BTREE,
  KEY `index_anime_jp_name` (`anime_jp_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tb_myanimelist_anime_themesong` (
  `idx` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `anime_id` int(10) unsigned DEFAULT NULL COMMENT '动画的站内id',
  `anime_en_name` varchar(255) DEFAULT NULL COMMENT '动画英文名',
  `anime_jp_name` varchar(255) DEFAULT NULL COMMENT '动画日文名',
  `name` varchar(255) DEFAULT NULL COMMENT '名字',
  `singer` varchar(255) DEFAULT NULL COMMENT '演唱者',
  `type` varchar(10) DEFAULT NULL COMMENT '类型',
  PRIMARY KEY (`idx`),
  UNIQUE KEY `unique_index` (`anime_id`,`name`,`type`,`singer`) USING BTREE,
  KEY `index_anime_en_name` (`anime_en_name`) USING BTREE,
  KEY `index_anime_jp_name` (`anime_jp_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
