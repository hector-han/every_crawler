CREATE DATABASE bj_house;
use bj_house;

CREATE TABLE `future_stat` (
  `day` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `total_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '可售房屋套数',
  `total_area` float not null default 0.0 COMMENT '可售房屋面积',
  `residential_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '住宅套数',
  `residential_area` float not null default 0.0 COMMENT '住宅面积',
  `commertial_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '商业单元',
  `commertial_area` float not null default 0.0 COMMENT '商业单元面积',
  `office_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '办公单元',
  `office_area` float not null default 0.0 COMMENT '办公单元面积',
  `parking_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '车位个数',
  `parking_area` float not null default 0.0 COMMENT '车位面积',

  PRIMARY KEY (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '可售期房统计';

CREATE TABLE `future_deal` (
  `day` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `total_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '网上签约套数',
  `total_area` float not null default 0.0 COMMENT '网上签约面积',
  `residential_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '住宅套数',
  `residential_area` float not null default 0.0 COMMENT '住宅面积',
  `commertial_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '商业单元',
  `commertial_area` float not null default 0.0 COMMENT '商业单元面积',
  `office_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '办公单元',
  `office_area` float not null default 0.0 COMMENT '办公单元面积',
  `parking_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '车位个数',
  `parking_area` float not null default 0.0 COMMENT '车位面积',

  PRIMARY KEY (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '期房网上签约';

CREATE TABLE `completed_stat` (
  `day` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `total_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '未签约套数',
  `total_area` float not null default 0.0 COMMENT '未签约面积',
  `residential_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '住宅套数',
  `residential_area` float not null default 0.0 COMMENT '住宅面积',
  `commertial_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '商业单元',
  `commertial_area` float not null default 0.0 COMMENT '商业单元面积',
  `office_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '办公单元',
  `office_area` float not null default 0.0 COMMENT '办公单元面积',
  `parking_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '车位个数',
  `parking_area` float not null default 0.0 COMMENT '车位面积',

  PRIMARY KEY (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '未签约现房统计';

CREATE TABLE `completed_deal` (
  `day` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `total_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '网上签约套数',
  `total_area` float not null default 0.0 COMMENT '网上签约面积',
  `residential_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '住宅套数',
  `residential_area` float not null default 0.0 COMMENT '住宅面积',
  `commertial_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '商业单元',
  `commertial_area` float not null default 0.0 COMMENT '商业单元面积',
  `office_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '办公单元',
  `office_area` float not null default 0.0 COMMENT '办公单元面积',
  `parking_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '车位个数',
  `parking_area` float not null default 0.0 COMMENT '车位面积',

  PRIMARY KEY (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '现房网上签约';


CREATE TABLE `stock_deal` (
  `day` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `total_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '网上签约套数',
  `total_area` float not null default 0.0 COMMENT '网上签约面积',
  `residential_number` int(9) unsigned NOT NULL DEFAULT '0' COMMENT '住宅套数',
  `residential_area` float not null default 0.0 COMMENT '住宅面积',
  PRIMARY KEY (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '存量房网上签约';