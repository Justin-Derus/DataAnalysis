CREATE DATABASE IF NOT EXISTS 'photosdbmanager';
USE 'photosdbmanager';

DROP TABLE IF EXISTS `tagged`;
DROP TABLE IF EXISTS `images`;
DROP TABLE IF EXISTS `cameras`;
DROP TABLE IF EXISTS `tags`;

CREATE TABLE `cameras` (
    `cameraname` varchar(255) NOT NULL PRIMARY KEY
);

CREATE TABLE `tags` (
    `tagname` varchar(255) NOT NULL,
    PRIMARY KEY (`tagname`)
);

CREATE TABLE `images` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `abspath` varchar(255) DEFAULT NULL,
    `relpath` varchar(255) DEFAULT NULL,
    `dateandtime` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'YYYY-MM-DD HH:MM:SS',
    `cameraname` varchar(255) DEFAULT NULL,
    `location` varchar(255) DEFAULT NULL COMMENT 'City, State, (Country)',
    `caption` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`cameraname`) REFERENCES `cameras` (`cameraname`) ON UPDATE CASCADE
);

CREATE TABLE `tagged` (
    `id` INT(11) NOT NULL,
    `tagname` varchar(255) NOT NULL,
    PRIMARY KEY(`id`,`tagname`),
    FOREIGN KEY (`id`) REFERENCES `images` (`id`),
    FOREIGN KEY (`tagname`) REFERENCES `tags` (`tagname`) ON UPDATE CASCADE
);