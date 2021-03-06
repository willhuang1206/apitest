/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50710
 Source Host           : localhost:3306
 Source Schema         : apitest

 Target Server Type    : MySQL
 Target Server Version : 50710
 File Encoding         : 65001

 Date: 31/05/2020 15:08:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for api_test_apiautomationcoverage
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apiautomationcoverage`;
CREATE TABLE `api_test_apiautomationcoverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `automations` varchar(1024) NOT NULL,
  `description` longtext,
  `lastUpdateTime` datetime NOT NULL,
  `api_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apiautomationcoverage_api_id_cf30a37e` (`api_id`) USING BTREE,
  KEY `api_test_apiautomationcoverage_project_id_b9370edb` (`project_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_apigrouplevelfirst
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apigrouplevelfirst`;
CREATE TABLE `api_test_apigrouplevelfirst` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `project_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apigrouplev_project_id_41653c61_fk_api_test_` (`project_id`) USING BTREE,
  KEY `api_test_apigrouplev_parent_id_abf105d6_fk_api_test_` (`parent_id`) USING BTREE,
  CONSTRAINT `api_test_apigrouplevelfirst_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `api_test_apigrouplevelfirst` (`id`),
  CONSTRAINT `api_test_apigrouplevelfirst_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_apigrouplevelfirst
-- ----------------------------
BEGIN;
INSERT INTO `api_test_apigrouplevelfirst` VALUES (41, '默认', 5, NULL);
COMMIT;

-- ----------------------------
-- Table structure for api_test_apihead
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apihead`;
CREATE TABLE `api_test_apihead` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `value` varchar(1024) DEFAULT NULL,
  `api_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apihead_api_id_a31f1998_fk_api_test_apiinfo_id` (`api_id`) USING BTREE,
  CONSTRAINT `api_test_apihead_ibfk_1` FOREIGN KEY (`api_id`) REFERENCES `api_test_apiinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1384 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_apiinfo
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apiinfo`;
CREATE TABLE `api_test_apiinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `httpType` varchar(50) NOT NULL,
  `requestType` varchar(50) NOT NULL,
  `apiAddress` varchar(1024) NOT NULL,
  `requestParameterType` varchar(50) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `mockStatus` tinyint(1) NOT NULL,
  `mockCode` varchar(50) DEFAULT NULL,
  `data` longtext,
  `lastUpdateTime` datetime NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `apiGroupLevelFirst_id` int(11) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `userUpdate_id` int(11) DEFAULT NULL,
  `type` varchar(50) NOT NULL,
  `params` varchar(1024) NOT NULL,
  `publish` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apiinfo_apiGroupLevelFirst_i_a43de3ee_fk_api_test_` (`apiGroupLevelFirst_id`) USING BTREE,
  KEY `api_test_apiinfo_project_id_a31d2482_fk_api_test_project_id` (`project_id`) USING BTREE,
  KEY `api_test_apiinfo_userUpdate_id_18d80d7c_fk_auth_user_id` (`userUpdate_id`) USING BTREE,
  CONSTRAINT `api_test_apiinfo_ibfk_1` FOREIGN KEY (`apiGroupLevelFirst_id`) REFERENCES `api_test_apigrouplevelfirst` (`id`),
  CONSTRAINT `api_test_apiinfo_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_apiinfo_ibfk_3` FOREIGN KEY (`userUpdate_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1851 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_apiinfo
-- ----------------------------
BEGIN;
INSERT INTO `api_test_apiinfo` VALUES (1850, '项目列表', 'HTTP', 'GET', 'http://${envApiHost}/api/project/project_list?page=1&name=&businessline=', 'application/json', 1, 0, '', '', '2020-05-27 19:47:22', '项目列表', 41, 5, 1, 'http', '{\"\":\"\"}', NULL);
COMMIT;

-- ----------------------------
-- Table structure for api_test_apioperationhistory
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apioperationhistory`;
CREATE TABLE `api_test_apioperationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `api_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apioperatio_api_id_cf909df7_fk_api_test_` (`api_id`) USING BTREE,
  KEY `api_test_apioperationhistory_user_id_2c79a96d_fk_auth_user_id` (`user_id`) USING BTREE,
  CONSTRAINT `api_test_apioperationhistory_ibfk_1` FOREIGN KEY (`api_id`) REFERENCES `api_test_apiinfo` (`id`),
  CONSTRAINT `api_test_apioperationhistory_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=491 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_apioperationhistory
-- ----------------------------
BEGIN;
INSERT INTO `api_test_apioperationhistory` VALUES (485, '2020-05-27 13:13:36', '新增接口“项目列表”', 1850, 1);
INSERT INTO `api_test_apioperationhistory` VALUES (486, '2020-05-27 13:14:12', '修改接口\"项目列表\"', 1850, 1);
INSERT INTO `api_test_apioperationhistory` VALUES (487, '2020-05-27 13:14:56', '修改接口\"项目列表\"', 1850, 1);
INSERT INTO `api_test_apioperationhistory` VALUES (488, '2020-05-27 13:41:05', '修改接口\"项目列表\"', 1850, 1);
INSERT INTO `api_test_apioperationhistory` VALUES (490, '2020-05-27 19:47:22', '修改接口\"项目列表\"', 1850, 1);
COMMIT;

-- ----------------------------
-- Table structure for api_test_apiparameter
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apiparameter`;
CREATE TABLE `api_test_apiparameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `_type` varchar(1024) NOT NULL,
  `value` longtext,
  `required` tinyint(1) NOT NULL,
  `restrict` varchar(1024) DEFAULT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `api_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apiparameter_api_id_cae3a9ce_fk_api_test_apiinfo_id` (`api_id`) USING BTREE,
  CONSTRAINT `api_test_apiparameter_ibfk_1` FOREIGN KEY (`api_id`) REFERENCES `api_test_apiinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6634 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_apiparameterraw
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apiparameterraw`;
CREATE TABLE `api_test_apiparameterraw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` longtext,
  `api_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `api_id` (`api_id`) USING BTREE,
  CONSTRAINT `api_test_apiparameterraw_ibfk_1` FOREIGN KEY (`api_id`) REFERENCES `api_test_apiinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_apirequesthistory
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apirequesthistory`;
CREATE TABLE `api_test_apirequesthistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `requestTime` datetime NOT NULL,
  `requestType` varchar(50) NOT NULL,
  `requestAddress` varchar(1024) NOT NULL,
  `httpCode` varchar(50) NOT NULL,
  `api_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apirequesth_api_id_bdc7fbb3_fk_api_test_` (`api_id`) USING BTREE,
  CONSTRAINT `api_test_apirequesthistory_ibfk_1` FOREIGN KEY (`api_id`) REFERENCES `api_test_apiinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_apiresponse
-- ----------------------------
DROP TABLE IF EXISTS `api_test_apiresponse`;
CREATE TABLE `api_test_apiresponse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `_type` varchar(1024) NOT NULL,
  `value` longtext,
  `required` tinyint(1) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `api_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_apiresponse_api_id_ee52ef9e_fk_api_test_apiinfo_id` (`api_id`) USING BTREE,
  CONSTRAINT `api_test_apiresponse_ibfk_1` FOREIGN KEY (`api_id`) REFERENCES `api_test_apiinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_automation
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automation`;
CREATE TABLE `api_test_automation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `type` varchar(50) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `updateTime` datetime NOT NULL,
  `group_id` int(11) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `params` longtext,
  `publish` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_automation_group_id_8ea05a7c_fk_api_test_group_id` (`group_id`) USING BTREE,
  KEY `api_test_automation_project_id_049f9999_fk_api_test_project_id` (`project_id`) USING BTREE,
  KEY `api_test_automation_user_id_19ed7fd3_fk` (`user_id`) USING BTREE,
  CONSTRAINT `api_test_automation_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_automation_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `api_test_group` (`id`),
  CONSTRAINT `api_test_automation_user_id_19ed7fd3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1013 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_automation
-- ----------------------------
BEGIN;
INSERT INTO `api_test_automation` VALUES (38, '表达式', 'case', '执行表达式', '2020-05-31 13:57:20', 7, 5, 43, '{\"id\": \"66\"}', NULL);
INSERT INTO `api_test_automation` VALUES (39, '条件判断', 'case', '使用条件判断if,else的样例', '2019-11-04 01:57:43', 7, 5, 1, '{}', NULL);
INSERT INTO `api_test_automation` VALUES (40, '循环执行', 'case', '循环执行for, while, loop样例', '2020-05-27 19:47:31', 7, 5, 1, '{}', NULL);
INSERT INTO `api_test_automation` VALUES (41, '自动化用例集', 'list', '批量执行多个用例', '2019-11-04 02:41:11', 7, 5, 1, '{}', NULL);
INSERT INTO `api_test_automation` VALUES (1012, '测试执行接口', 'case', '', '2020-05-31 13:57:20', 7, 5, 1, '{\"id\": \"66\"}', NULL);
COMMIT;

-- ----------------------------
-- Table structure for api_test_automation2step
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automation2step`;
CREATE TABLE `api_test_automation2step` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order` int(11) DEFAULT NULL,
  `automation_id` int(11) NOT NULL,
  `step_id` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_automation2_automation_id_358e51e2_fk_api_test_` (`automation_id`) USING BTREE,
  KEY `api_test_automation2_step_id_f833a1f5_fk_api_test_` (`step_id`) USING BTREE,
  CONSTRAINT `api_test_automation2step_ibfk_1` FOREIGN KEY (`automation_id`) REFERENCES `api_test_automation` (`id`),
  CONSTRAINT `api_test_automation2step_ibfk_2` FOREIGN KEY (`step_id`) REFERENCES `api_test_automationstep` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3163 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_automation2step
-- ----------------------------
BEGIN;
INSERT INTO `api_test_automation2step` VALUES (123, 1, 38, 61, 1);
INSERT INTO `api_test_automation2step` VALUES (124, 2, 38, 62, 1);
INSERT INTO `api_test_automation2step` VALUES (125, 4, 38, 63, 1);
INSERT INTO `api_test_automation2step` VALUES (127, 7, 39, 62, 1);
INSERT INTO `api_test_automation2step` VALUES (128, 8, 39, 64, 1);
INSERT INTO `api_test_automation2step` VALUES (129, 2, 40, 65, 1);
INSERT INTO `api_test_automation2step` VALUES (130, 3, 40, 66, 1);
INSERT INTO `api_test_automation2step` VALUES (131, 1, 40, 67, 1);
INSERT INTO `api_test_automation2step` VALUES (2548, 3, 38, 2450, 0);
INSERT INTO `api_test_automation2step` VALUES (2914, 5, 38, 2753, 1);
INSERT INTO `api_test_automation2step` VALUES (3011, 6, 38, 1904, 1);
INSERT INTO `api_test_automation2step` VALUES (3162, 1, 1012, 2845, 1);
COMMIT;

-- ----------------------------
-- Table structure for api_test_automation_apis
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automation_apis`;
CREATE TABLE `api_test_automation_apis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `automation_id` int(11) NOT NULL,
  `apiinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `api_test_automation_apis_automation_id_apiinfo_id_ac2a89a9_uniq` (`automation_id`,`apiinfo_id`) USING BTREE,
  KEY `api_test_automation__apiinfo_id_2f81c030_fk_api_test_` (`apiinfo_id`) USING BTREE,
  CONSTRAINT `api_test_automation_apis_ibfk_1` FOREIGN KEY (`apiinfo_id`) REFERENCES `api_test_apiinfo` (`id`),
  CONSTRAINT `api_test_automation_apis_ibfk_2` FOREIGN KEY (`automation_id`) REFERENCES `api_test_automation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_automationlist2automation
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automationlist2automation`;
CREATE TABLE `api_test_automationlist2automation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order` int(11) DEFAULT NULL,
  `automationParent_id` int(11) NOT NULL,
  `automationStep_id` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_automationl_automationParent_id_26087872_fk_api_test_` (`automationParent_id`) USING BTREE,
  KEY `api_test_automationl_automationStep_id_3f7d5243_fk_api_test_` (`automationStep_id`) USING BTREE,
  CONSTRAINT `api_test_automationlist2automation_ibfk_1` FOREIGN KEY (`automationParent_id`) REFERENCES `api_test_automation` (`id`),
  CONSTRAINT `api_test_automationlist2automation_ibfk_2` FOREIGN KEY (`automationStep_id`) REFERENCES `api_test_automation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=421 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_automationlist2automation
-- ----------------------------
BEGIN;
INSERT INTO `api_test_automationlist2automation` VALUES (28, 1, 41, 40, 1);
INSERT INTO `api_test_automationlist2automation` VALUES (29, 2, 41, 39, 1);
INSERT INTO `api_test_automationlist2automation` VALUES (30, 3, 41, 38, 1);
INSERT INTO `api_test_automationlist2automation` VALUES (420, 4, 41, 1012, 1);
COMMIT;

-- ----------------------------
-- Table structure for api_test_automationresult
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automationresult`;
CREATE TABLE `api_test_automationresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` longtext,
  `details` longtext,
  `result` varchar(50) NOT NULL,
  `testTime` varchar(50) DEFAULT NULL,
  `automation_id` int(11) DEFAULT NULL,
  `step_id` int(11) DEFAULT NULL,
  `description` text,
  `name` varchar(1024) DEFAULT NULL,
  `trace` varchar(25) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `api_id` int(11) DEFAULT NULL,
  `env` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_automationr_automation_id_409065cd_fk_api_test_` (`automation_id`) USING BTREE,
  KEY `api_test_automationr_step_id_2c749513_fk_api_test_` (`step_id`) USING BTREE,
  KEY `api_test_automationr_project_id_347150f1_fk_api_test_` (`project_id`) USING BTREE,
  KEY `api_test_automationresult_api_id_c7de4a41_fk_api_test_apiinfo_id` (`api_id`) USING BTREE,
  KEY `api_test_automationresult_user_id_bafd3d2e_fk_auth_user_id` (`user_id`) USING BTREE,
  CONSTRAINT `api_test_automationr_automation_id_409065cd_fk_api_test_` FOREIGN KEY (`automation_id`) REFERENCES `api_test_automation` (`id`),
  CONSTRAINT `api_test_automationresult_ibfk_2` FOREIGN KEY (`step_id`) REFERENCES `api_test_automationstep` (`id`),
  CONSTRAINT `api_test_automationresult_ibfk_3` FOREIGN KEY (`api_id`) REFERENCES `api_test_apiinfo` (`id`),
  CONSTRAINT `api_test_automationresult_ibfk_4` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_automationresult_user_id_bafd3d2e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94372 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_automationresultfaildetail
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automationresultfaildetail`;
CREATE TABLE `api_test_automationresultfaildetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  `severity` varchar(50) NOT NULL,
  `cause` varchar(256) DEFAULT NULL,
  `detail` longtext,
  `bug` varchar(50) DEFAULT NULL,
  `action` varchar(256) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `result_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_test_automationr_project_id_1b024c29_fk_api_test_` (`project_id`),
  KEY `api_test_automationr_result_id_ef8d6bad_fk_api_test_` (`result_id`),
  CONSTRAINT `api_test_automationr_project_id_1b024c29_fk_api_test_` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_automationr_result_id_ef8d6bad_fk_api_test_` FOREIGN KEY (`result_id`) REFERENCES `api_test_automationresult` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_automationstep
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automationstep`;
CREATE TABLE `api_test_automationstep` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `type` varchar(50) NOT NULL,
  `steps` longtext NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `updateTime` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `params` longtext,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_automationstep_user_id_bd488817_fk` (`user_id`) USING BTREE,
  KEY `api_test_automations_project_id_f3520f00_fk_api_test_` (`project_id`) USING BTREE,
  CONSTRAINT `api_test_automationstep_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_automationstep_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2846 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_automationstep
-- ----------------------------
BEGIN;
INSERT INTO `api_test_automationstep` VALUES (61, '内置表达式', 'normal', '[]', '1、输出##${num}+1##\n2、输出##int(\'111\')##', '2019-11-04 01:50:00', NULL, '{\"num\":1}', 5);
INSERT INTO `api_test_automationstep` VALUES (62, '获取当前时间', 'global', '[]', '1、执行表达式from datetime import datetime;currentTime=datetime.now().strftime(\'%Y-%m-%d %H:%M:%S\')名称为计算trace\n2、输出当前时间: ${currentTime}', '2019-11-04 01:53:37', NULL, '{}', 5);
INSERT INTO `api_test_automationstep` VALUES (63, '打印获取的时间', 'normal', '[]', '1、输出${currentTime}', '2019-11-04 01:54:07', NULL, '{}', 5);
INSERT INTO `api_test_automationstep` VALUES (64, '条件判断', 'normal', '[]', '如果${num}==5\n输出${currentTime}\n否则\n输出不满足条件\n结束条件\n输出最后一步', '2019-11-04 02:02:56', NULL, '{\"num\":6}', 5);
INSERT INTO `api_test_automationstep` VALUES (65, '次数循环', 'normal', '[]', '#执行次数循环\n1、循环次数${count}\n2、输出${for_index}\n3、如果${for_index}==3\n4、继续\n5、结束条件\n6、输出执行continue会跳过\n7、如果${for_index}==4\n8、退出\n9、结束条件\n10、结束次数循环\n11、输出你好啊', '2019-11-04 02:23:03', NULL, '{\"count\":6}', 5);
INSERT INTO `api_test_automationstep` VALUES (66, '条件循环', 'normal', '[]', '#执行条件循环\n1、保存数据1为参数count\n2、循环条件${count}<5\n3、输出${count}\n4、保存数据##${count}+1##为参数count\n5、结束条件循环', '2019-11-04 02:29:05', NULL, '{}', 5);
INSERT INTO `api_test_automationstep` VALUES (67, '数组循环', 'normal', '[]', '#使用数组执行循环\n1、循环数组${array}\n2、输出${id}\n3、结束数组循环', '2019-11-04 02:30:27', NULL, '{\"array\": [{\"id\": 1}, {\"id\": 2}, {\"id\": 3}]}', 5);
INSERT INTO `api_test_automationstep` VALUES (1904, '获取不重复字符串', 'project', '[]', '1、执行表达式import datetime;import time;datetime_object = datetime.datetime.now();timestamp=str(int(time.mktime(datetime_object.timetuple())*1000 + datetime_object.microsecond/1000))名称为获取13位时间戳\n2、保存数据${timestamp}为参数no_repeat_character', '2019-11-26 06:08:10', NULL, '{}', NULL);
INSERT INTO `api_test_automationstep` VALUES (2450, '执行sql', 'normal', '[{\"type\":\"common\",\"name\":\"runSql\",\"actionId\":0,\"params\":\"{\\\"host\\\": \\\"101.132.5.106\\\",\\\"port\\\":\\\"3306\\\", \\\"database\\\": \\\"db_funds_account\\\", \\\"username\\\": \\\"sdxsit\\\", \\\"password\\\": \\\"Ftsit18WSX\\\", \\\"sql\\\": \\\"select * FROM db_funds_account.`t_account` WHERE cust_id=\'1234\'\\\"}\",\"description\":\"执行sql\",\"disable\":\"False\"},{\"type\":\"common\",\"name\":\"storeResultVariable\",\"actionId\":0,\"params\":\"{\\\"locator\\\": \\\"[0]\\\", \\\"name\\\": \\\"result\\\"}\",\"description\":\"保存结果\",\"disable\":\"False\"},{\"type\":\"common\",\"name\":\"assertResultEquals\",\"actionId\":0,\"params\":\"{\\\"expected\\\": \\\"142\\\", \\\"locator\\\": \\\"[0].id\\\"}\",\"description\":\"验证结果相等\",\"disable\":\"False\"}]', '', '2020-03-02 14:55:45', NULL, '{}', 5);
INSERT INTO `api_test_automationstep` VALUES (2753, '保存用例参数', 'normal', '[]', '1、保存数据##${id}+1##为用例参数id', '2020-03-10 19:16:10', NULL, '{\"id\":\"\"}', 5);
INSERT INTO `api_test_automationstep` VALUES (2845, '执行接口', 'normal', '[]', '1、执行接口项目列表,使用参数{}', '2020-05-28 11:16:40', NULL, '{}', 5);
COMMIT;

-- ----------------------------
-- Table structure for api_test_automationtask
-- ----------------------------
DROP TABLE IF EXISTS `api_test_automationtask`;
CREATE TABLE `api_test_automationtask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `env` varchar(1024) NOT NULL,
  `params` longtext,
  `crontab` varchar(50) NOT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `sendEmail` int(11) DEFAULT NULL,
  `emails` varchar(1024) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `automations` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_automationt_project_id_886d9e3d_fk_api_test_` (`project_id`) USING BTREE,
  CONSTRAINT `api_test_automationtask_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_automationtask
-- ----------------------------
BEGIN;
INSERT INTO `api_test_automationtask` VALUES (9, '自动化任务样例', '集成', '{}', '*/5 * * * *', NULL, NULL, 0, 1, '[]', 5, '[41]');
COMMIT;

-- ----------------------------
-- Table structure for api_test_globalconfig
-- ----------------------------
DROP TABLE IF EXISTS `api_test_globalconfig`;
CREATE TABLE `api_test_globalconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `value` varchar(1024) NOT NULL,
  `type` varchar(50) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_globalconfig
-- ----------------------------
BEGIN;
INSERT INTO `api_test_globalconfig` VALUES (16, 'fail.retry', '0', 'config', '用例集的用例执行失败后默认重试的次数', 1);
INSERT INTO `api_test_globalconfig` VALUES (18, 'action.interval', '0', 'config', '用例集中用例执行间隔时间', 1);
INSERT INTO `api_test_globalconfig` VALUES (19, 'step.interval', '1', 'config', '用例中步骤执行间隔时间', 1);
INSERT INTO `api_test_globalconfig` VALUES (30, '高优先级', '', 'tag', '', 1);
INSERT INTO `api_test_globalconfig` VALUES (31, '中优先级', '', 'tag', '', 1);
INSERT INTO `api_test_globalconfig` VALUES (32, '低优先级', '', 'tag', '', 1);
INSERT INTO `api_test_globalconfig` VALUES (66, 'api.interval', '0.5', 'config', '调用接口的间隔时间，主要用于生产环境，单位秒', 1);
INSERT INTO `api_test_globalconfig` VALUES (68, 'thread.2', 'true', 'config', '', 1);
COMMIT;

-- ----------------------------
-- Table structure for api_test_group
-- ----------------------------
DROP TABLE IF EXISTS `api_test_group`;
CREATE TABLE `api_test_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `project_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_group_project_id_868ece87_fk_api_test_project_id` (`project_id`) USING BTREE,
  KEY `api_test_group_parent_id_515cd754_fk_api_test_group_id` (`parent_id`) USING BTREE,
  CONSTRAINT `api_test_group_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_group_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `api_test_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_group
-- ----------------------------
BEGIN;
INSERT INTO `api_test_group` VALUES (7, '样例', 5, NULL);
COMMIT;

-- ----------------------------
-- Table structure for api_test_project
-- ----------------------------
DROP TABLE IF EXISTS `api_test_project`;
CREATE TABLE `api_test_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `version` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `LastUpdateTime` datetime NOT NULL,
  `createTime` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `businessline` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_project_user_id_42720ccc_fk` (`user_id`) USING BTREE,
  CONSTRAINT `api_test_project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_project
-- ----------------------------
BEGIN;
INSERT INTO `api_test_project` VALUES (5, '样例项目', '1.0', 'Web', '各种接口和自动化用例的样例', 1, '2020-05-06 13:50:36', '2019-09-23 06:43:49', 1, '其他');
COMMIT;

-- ----------------------------
-- Table structure for api_test_projectconfig
-- ----------------------------
DROP TABLE IF EXISTS `api_test_projectconfig`;
CREATE TABLE `api_test_projectconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `value` varchar(1024) NOT NULL,
  `type` varchar(50) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_projectconfig_project_id_a2a607f2` (`project_id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_projectconfig
-- ----------------------------
BEGIN;
INSERT INTO `api_test_projectconfig` VALUES (11, '集成', '{\"envApiHost\":\"127.0.0.1:8092\",\"env\":\"测试环境\"}', 'env', '', 1, 5);
COMMIT;

-- ----------------------------
-- Table structure for api_test_projectdynamic
-- ----------------------------
DROP TABLE IF EXISTS `api_test_projectdynamic`;
CREATE TABLE `api_test_projectdynamic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `type` varchar(50) NOT NULL,
  `operationObject` varchar(50) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_projectdyna_project_id_7799a12d_fk_api_test_` (`project_id`) USING BTREE,
  KEY `api_test_projectdynamic_user_id_f34f87ae_fk_auth_user_id` (`user_id`) USING BTREE,
  CONSTRAINT `api_test_projectdynamic_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_projectdynamic_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7006 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_projectdynamic
-- ----------------------------
BEGIN;
INSERT INTO `api_test_projectdynamic` VALUES (817, '2019-09-23 06:43:49', '添加', '项目', '测试', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (876, '2019-11-04 01:41:32', '修改', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (877, '2019-11-04 01:47:09', '新增', '自动化', '新增自动化\"表达式\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (878, '2019-11-04 01:57:43', '新增', '自动化', '新增自动化\"条件判断\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (879, '2019-11-04 02:19:52', '新增', '自动化', '新增自动化\"循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (880, '2019-11-04 02:41:11', '新增', '自动化', '新增自动化\"自动化用例集\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (881, '2019-11-04 02:44:50', '新增', '自动化任务', '新增自动化任务\"自动化任务样例\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (882, '2019-11-04 03:09:03', '禁用', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (971, '2019-11-21 10:41:45', '修改', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (977, '2019-11-22 08:15:40', '修改', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1178, '2019-12-04 16:54:47', '新增', '接口', '新增接口“手机登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1179, '2019-12-04 16:55:27', '修改', '接口', '修改接口“手机登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1180, '2019-12-04 17:04:53', '新增', '自动化', '新增自动化\"测试\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1181, '2019-12-04 17:13:22', '删除', '自动化', '删除自动化\"测试\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1182, '2019-12-04 17:13:27', '删除', '接口', '删除接口分组，列表“[\'手机登录\']”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1183, '2019-12-04 17:29:38', '新增', '接口', '新增接口“登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1184, '2019-12-04 17:35:13', '修改', '接口', '修改接口“登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1185, '2019-12-04 17:38:08', '新增', '自动化', '新增自动化\"登录测试\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1186, '2019-12-04 17:41:34', '修改', '接口', '修改接口“登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1187, '2019-12-04 17:44:24', '修改', '接口', '修改接口“登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1190, '2019-12-04 18:49:05', '修改', '接口', '修改接口“登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1191, '2019-12-04 18:51:01', '修改', '接口', '修改接口“登录”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1195, '2019-12-04 19:49:22', '删除', '自动化', '删除自动化\"登录测试\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1196, '2019-12-04 19:49:31', '删除', '接口', '删除接口分组，列表“[\'登录\']”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1319, '2019-12-13 16:06:25', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1320, '2019-12-13 16:06:27', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1344, '2019-12-13 16:50:08', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1345, '2019-12-13 16:50:20', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1346, '2019-12-13 16:50:36', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1347, '2019-12-13 16:50:52', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1359, '2019-12-13 17:26:06', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1360, '2019-12-13 17:26:08', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1363, '2019-12-13 17:27:05', '修改', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1364, '2019-12-13 17:27:08', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1365, '2019-12-13 17:27:10', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1368, '2019-12-13 17:30:14', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1369, '2019-12-13 17:30:16', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1376, '2019-12-13 18:48:40', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1381, '2019-12-16 09:32:30', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (1382, '2019-12-16 09:32:32', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (2686, '2020-02-19 17:27:21', '新增', '接口', '新增接口“语音听写”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (2814, '2020-02-23 16:47:58', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (2815, '2020-02-23 16:48:01', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3322, '2020-02-27 19:01:23', '修改', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3348, '2020-02-28 11:31:43', '删除', '接口分组', '删除接口分组“测试”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3349, '2020-02-28 11:32:19', '修改', '接口', '修改接口“语音听写”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3641, '2020-03-02 14:54:22', '修改', '自动化', '修改自动化\"表达式\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3642, '2020-03-02 14:56:10', '添加', '配置', '集成', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3643, '2020-03-02 14:56:16', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3644, '2020-03-02 14:57:37', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3649, '2020-03-02 15:08:56', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3664, '2020-03-02 15:22:44', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3709, '2020-03-02 17:44:27', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3835, '2020-03-03 15:47:21', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3836, '2020-03-03 15:48:17', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3837, '2020-03-03 15:49:12', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (3838, '2020-03-03 15:52:30', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (4767, '2020-03-09 16:06:25', '执行', '自动化用例', '执行自动化用例[表达式]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (4768, '2020-03-09 16:09:47', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (4936, '2020-03-10 19:15:21', '删除', '自动化', '删除自动化\"001、个人用户正常开户并绑卡\"', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4937, '2020-03-10 19:16:15', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4938, '2020-03-10 19:18:21', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4939, '2020-03-10 19:19:07', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4940, '2020-03-10 19:19:43', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4941, '2020-03-10 19:31:41', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4942, '2020-03-10 19:35:47', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4943, '2020-03-10 19:44:56', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (4949, '2020-03-11 09:41:45', '执行', '自动化用例', '执行自动化用例[表达式]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (5415, '2020-03-12 15:34:58', '执行', '自动化用例', '执行自动化用例[表达式]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (5416, '2020-03-12 15:36:00', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5931, '2020-03-18 13:59:45', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5933, '2020-03-18 14:00:52', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5934, '2020-03-18 14:01:24', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5935, '2020-03-18 14:02:59', '修改', '自动化', '修改自动化\"表达式\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5936, '2020-03-18 14:03:20', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5937, '2020-03-18 14:03:35', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5938, '2020-03-18 14:04:04', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5939, '2020-03-18 14:05:44', '修改', '自动化', '修改自动化\"表达式\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5940, '2020-03-18 14:05:48', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5941, '2020-03-18 14:06:01', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5942, '2020-03-18 14:06:33', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (5943, '2020-03-18 14:06:43', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6349, '2020-03-20 18:57:52', '执行', '接口', '执行接口[查看项目]失败', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6350, '2020-03-20 18:58:05', '执行', '接口', '执行接口[登录1234]成功', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6351, '2020-03-20 18:58:13', '执行', '接口', '执行接口[02-商品类目-请求所有数据-生产1234]成功', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6726, '2020-03-26 20:07:28', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (6731, '2020-03-27 10:23:37', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6734, '2020-03-27 10:26:47', '执行', '自动化用例', '执行自动化用例[表达式]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6735, '2020-03-27 14:54:11', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6767, '2020-04-01 15:43:53', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6768, '2020-04-01 16:01:42', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6770, '2020-04-01 18:11:41', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6777, '2020-04-02 11:08:34', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6778, '2020-04-02 11:39:48', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6779, '2020-04-02 11:43:24', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6780, '2020-04-02 11:46:16', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6789, '2020-04-02 13:55:37', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6790, '2020-04-02 13:56:02', '执行', '自动化用例', '执行自动化用例[表达式]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6791, '2020-04-02 13:56:36', '执行', '自动化用例', '执行自动化用例[表达式]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6792, '2020-04-02 14:02:00', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6793, '2020-04-02 14:06:01', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6794, '2020-04-02 14:07:13', '执行', '自动化用例', '执行自动化用例[表达式]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6796, '2020-04-02 15:00:15', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6819, '2020-04-02 16:16:19', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, NULL);
INSERT INTO `api_test_projectdynamic` VALUES (6831, '2020-04-09 16:51:42', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (6832, '2020-04-22 11:19:03', '修改', '自动化', '修改自动化\"表达式\"', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (6833, '2020-04-22 11:19:09', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (6834, '2020-04-22 13:10:26', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (6836, '2020-04-28 11:26:37', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6837, '2020-04-28 11:26:40', '启用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6838, '2020-04-28 12:50:53', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6839, '2020-04-28 12:50:56', '启用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6840, '2020-04-28 12:53:19', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6841, '2020-04-28 12:53:22', '启用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6842, '2020-04-28 12:57:34', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6843, '2020-04-28 12:57:36', '启用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6844, '2020-04-28 12:58:19', '修改', '项目', '样例项目1', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6845, '2020-04-28 12:58:29', '修改', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6846, '2020-05-06 13:50:34', '禁用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6847, '2020-05-06 13:50:36', '启用', '项目', '样例项目', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6857, '2020-05-07 10:25:10', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6858, '2020-05-07 10:26:32', '修改', '自动化', '修改自动化\"循环执行1\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6859, '2020-05-07 10:26:45', '修改', '自动化', '修改自动化\"循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6860, '2020-05-07 10:26:57', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6861, '2020-05-07 10:51:53', '新增', '自动化', '新增自动化\"循环执行1\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6862, '2020-05-07 10:52:01', '删除', '自动化', '删除自动化\"循环执行1\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6866, '2020-05-07 12:47:16', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6867, '2020-05-07 15:43:03', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6868, '2020-05-07 15:56:53', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6869, '2020-05-07 16:38:02', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6870, '2020-05-08 15:26:29', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6871, '2020-05-08 17:37:26', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6874, '2020-05-09 12:42:43', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6875, '2020-05-09 13:19:20', '新增', '自动化', '新增自动化\"自动化用例集1\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6878, '2020-05-09 13:21:55', '删除', '分组', '删除分组“2”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6879, '2020-05-09 13:22:07', '新增', '自动化', '新增自动化\"222222222\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6880, '2020-05-09 13:22:10', '删除', '自动化', '删除自动化\"222222222\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6881, '2020-05-09 13:22:14', '删除', '自动化', '删除自动化\"自动化用例集1\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6882, '2020-05-22 16:13:41', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6883, '2020-05-22 17:21:08', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6884, '2020-05-23 14:05:08', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6885, '2020-05-25 14:11:58', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6886, '2020-05-25 16:58:16', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6889, '2020-05-26 12:50:04', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6890, '2020-05-26 13:00:46', '禁用', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6891, '2020-05-26 14:35:23', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6892, '2020-05-26 16:50:03', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6893, '2020-05-27 12:22:16', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6894, '2020-05-27 13:03:53', '执行', '接口', '执行接口[http://127.0.0.1:8092/api/project/project_list?page=1&name=&businessline=]成功', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6895, '2020-05-27 13:13:36', '新增', '接口', '新增接口“项目列表”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6896, '2020-05-27 13:13:47', '执行', '接口', '执行接口[项目列表]成功', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6897, '2020-05-27 13:14:12', '修改', '接口', '修改接口“项目列表”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6898, '2020-05-27 13:14:21', '执行', '接口', '执行接口[项目列表]成功', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6899, '2020-05-27 13:14:56', '修改', '接口', '修改接口“项目列表”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6900, '2020-05-27 13:15:32', '修改', '配置', '集成', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6901, '2020-05-27 13:15:42', '执行', '接口', '执行接口[项目列表]成功', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6902, '2020-05-27 13:16:28', '执行', '接口', '执行接口[02-商品类目-请求所有数据-生产1234]成功', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6903, '2020-05-27 13:37:20', '执行', '接口', '执行接口[登录1234]失败', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6904, '2020-05-27 13:37:41', '删除', '接口', '删除接口分组，列表“[\'登录1234\']”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6905, '2020-05-27 13:37:44', '删除', '接口', '删除接口分组，列表“[\'查看项目\']”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6906, '2020-05-27 13:37:47', '删除', '接口', '删除接口分组，列表“[\'语音听写\']”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6907, '2020-05-27 13:41:05', '修改', '接口', '修改接口“项目列表”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6908, '2020-05-27 13:41:29', '修改', '接口', '修改接口“02-商品类目-请求所有数据-生产1234”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6909, '2020-05-27 13:41:42', '删除', '接口分组', '删除接口分组“测试”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6910, '2020-05-27 13:42:05', '删除', '分组', '删除分组“222”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6911, '2020-05-27 13:47:43', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6912, '2020-05-27 13:54:13', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6913, '2020-05-27 13:54:47', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6914, '2020-05-27 13:55:59', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6915, '2020-05-27 13:56:41', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6916, '2020-05-27 14:09:17', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6917, '2020-05-27 14:42:17', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6918, '2020-05-27 14:56:45', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6919, '2020-05-27 15:40:49', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6920, '2020-05-27 15:44:12', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6921, '2020-05-27 15:45:56', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6922, '2020-05-27 15:50:24', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6923, '2020-05-27 16:03:39', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6924, '2020-05-27 16:04:08', '新增', '自动化', '新增自动化\"测试循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6925, '2020-05-27 16:05:43', '修改', '自动化', '修改自动化\"测试循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6926, '2020-05-27 16:05:48', '执行', '自动化用例', '执行自动化用例[测试循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6927, '2020-05-27 16:16:32', '执行', '自动化用例', '执行自动化用例[测试循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6928, '2020-05-27 16:24:40', '执行', '自动化用例', '执行自动化用例[测试循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6929, '2020-05-27 16:27:26', '执行', '自动化用例', '执行自动化用例[测试循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6930, '2020-05-27 16:28:11', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6931, '2020-05-27 17:24:06', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6932, '2020-05-27 17:45:57', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6933, '2020-05-27 17:46:25', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6934, '2020-05-27 18:44:50', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6935, '2020-05-27 19:40:17', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6936, '2020-05-27 19:47:22', '修改', '接口', '修改接口“项目列表”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6937, '2020-05-27 19:47:31', '修改', '自动化', '修改自动化\"循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6938, '2020-05-27 20:01:58', '禁用', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6939, '2020-05-28 10:45:15', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6940, '2020-05-28 10:52:29', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6941, '2020-05-28 11:08:33', '修改', '自动化', '修改自动化\"测试循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6942, '2020-05-28 11:09:41', '修改', '自动化', '修改自动化\"测试循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6943, '2020-05-28 11:15:56', '新增', '自动化', '新增自动化\"111\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6944, '2020-05-28 11:16:10', '修改', '自动化', '修改自动化\"测试执行接口\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6945, '2020-05-28 11:16:46', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6946, '2020-05-28 11:18:07', '修改', '配置', '集成', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6947, '2020-05-28 11:18:16', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6948, '2020-05-28 11:19:04', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6949, '2020-05-28 11:21:52', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6950, '2020-05-28 11:30:26', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6951, '2020-05-28 11:33:08', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6952, '2020-05-28 11:36:32', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6953, '2020-05-28 11:36:46', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6954, '2020-05-28 11:54:18', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6955, '2020-05-28 12:04:35', '执行', '自动化用例', '执行自动化用例[测试循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6956, '2020-05-28 12:32:57', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6957, '2020-05-29 12:00:50', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6958, '2020-05-29 12:03:40', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6959, '2020-05-29 12:22:05', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6960, '2020-05-29 12:27:04', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6961, '2020-05-29 12:32:35', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6962, '2020-05-29 12:57:00', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6963, '2020-05-29 12:58:18', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6964, '2020-05-29 13:02:09', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6965, '2020-05-29 13:09:12', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6966, '2020-05-29 13:10:33', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6967, '2020-05-29 13:14:57', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6968, '2020-05-29 13:36:28', '删除', '自动化', '删除自动化\"测试循环执行\"', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6969, '2020-05-29 13:36:39', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6970, '2020-05-29 13:42:10', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6971, '2020-05-29 13:56:59', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6972, '2020-05-29 14:02:02', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6973, '2020-05-29 14:03:03', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6974, '2020-05-29 14:04:22', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6975, '2020-05-29 14:07:41', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6976, '2020-05-29 14:11:32', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6977, '2020-05-29 14:19:53', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6978, '2020-05-29 14:20:25', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6979, '2020-05-29 14:20:39', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6980, '2020-05-29 14:26:52', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6981, '2020-05-29 14:27:41', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6982, '2020-05-29 14:33:15', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6983, '2020-05-29 14:40:33', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6984, '2020-05-29 14:50:39', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6985, '2020-05-29 14:51:30', '执行', '自动化用例', '执行自动化用例[条件判断]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6986, '2020-05-29 14:53:11', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6987, '2020-05-29 14:55:20', '执行', '自动化用例', '执行自动化用例[表达式]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6988, '2020-05-29 15:00:08', '执行', '自动化用例', '执行自动化用例[循环执行]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6989, '2020-05-29 15:01:55', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6990, '2020-05-29 15:27:07', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6991, '2020-05-29 15:31:57', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6992, '2020-05-29 15:32:40', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6993, '2020-05-29 15:33:22', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6994, '2020-05-29 15:33:35', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6995, '2020-05-29 15:40:49', '禁用', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6996, '2020-05-29 15:58:26', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (6997, '2020-05-29 17:30:41', '执行', '任务', '自动化任务样例', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (6998, '2020-05-29 17:36:37', '执行', '任务', '自动化任务样例', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (6999, '2020-05-29 17:46:38', '禁用', '任务', '自动化任务样例', 5, 43);
INSERT INTO `api_test_projectdynamic` VALUES (7000, '2020-05-31 13:41:15', '执行', '任务', '自动化任务样例', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (7001, '2020-05-31 13:56:23', '删除', '接口', '删除接口分组，列表“[\'02-商品类目-请求所有数据-生产1234\']”', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (7002, '2020-05-31 13:56:37', '执行', '接口', '执行接口[项目列表]成功', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (7003, '2020-05-31 13:56:48', '执行', '自动化用例', '执行自动化用例[测试执行接口]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (7004, '2020-05-31 13:57:00', '执行', '自动化用例', '执行自动化用例[自动化用例集]', 5, 1);
INSERT INTO `api_test_projectdynamic` VALUES (7005, '2020-05-31 13:57:19', '执行', '任务', '自动化任务样例', 5, 1);
COMMIT;

-- ----------------------------
-- Table structure for api_test_projectmember
-- ----------------------------
DROP TABLE IF EXISTS `api_test_projectmember`;
CREATE TABLE `api_test_projectmember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_projectmemb_project_id_6e07cb22_fk_api_test_` (`project_id`) USING BTREE,
  KEY `api_test_projectmember_user_id_13a8bcac_fk_auth_user_id` (`user_id`) USING BTREE,
  CONSTRAINT `api_test_projectmember_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `api_test_project` (`id`),
  CONSTRAINT `api_test_projectmember_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_projectmember
-- ----------------------------
BEGIN;
INSERT INTO `api_test_projectmember` VALUES (5, 5, 1, 1);
INSERT INTO `api_test_projectmember` VALUES (25, 5, 43, 4);
COMMIT;

-- ----------------------------
-- Table structure for api_test_publishconfig
-- ----------------------------
DROP TABLE IF EXISTS `api_test_publishconfig`;
CREATE TABLE `api_test_publishconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1024) NOT NULL,
  `automations` varchar(1024) NOT NULL,
  `env` varchar(1024) NOT NULL,
  `params` varchar(1024) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `sendEmail` int(11) DEFAULT NULL,
  `emails` varchar(1024) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `api_test_publishconfig_project_id_1e512011` (`project_id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for api_test_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `api_test_userprofile`;
CREATE TABLE `api_test_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone` varchar(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `api_test_userprofile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_test_userprofile
-- ----------------------------
BEGIN;
INSERT INTO `api_test_userprofile` VALUES (17, '11111111111', 43, 'local');
INSERT INTO `api_test_userprofile` VALUES (18, '11111111111', 1, 'local');
COMMIT;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
INSERT INTO `auth_group` VALUES (3, '测试成员');
INSERT INTO `auth_group` VALUES (2, '测试经理');
INSERT INTO `auth_group` VALUES (1, '管理员');
INSERT INTO `auth_group` VALUES (4, '项目成员');
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`) USING BTREE,
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
INSERT INTO `auth_group_permissions` VALUES (4, 1, 1);
INSERT INTO `auth_group_permissions` VALUES (5, 1, 2);
INSERT INTO `auth_group_permissions` VALUES (6, 1, 3);
INSERT INTO `auth_group_permissions` VALUES (7, 1, 4);
INSERT INTO `auth_group_permissions` VALUES (8, 1, 5);
INSERT INTO `auth_group_permissions` VALUES (9, 1, 6);
INSERT INTO `auth_group_permissions` VALUES (10, 1, 7);
INSERT INTO `auth_group_permissions` VALUES (11, 1, 8);
INSERT INTO `auth_group_permissions` VALUES (12, 1, 9);
INSERT INTO `auth_group_permissions` VALUES (13, 1, 10);
INSERT INTO `auth_group_permissions` VALUES (14, 1, 11);
INSERT INTO `auth_group_permissions` VALUES (15, 1, 12);
INSERT INTO `auth_group_permissions` VALUES (16, 1, 13);
INSERT INTO `auth_group_permissions` VALUES (17, 1, 14);
INSERT INTO `auth_group_permissions` VALUES (18, 1, 15);
INSERT INTO `auth_group_permissions` VALUES (19, 1, 16);
INSERT INTO `auth_group_permissions` VALUES (20, 1, 17);
INSERT INTO `auth_group_permissions` VALUES (21, 1, 18);
INSERT INTO `auth_group_permissions` VALUES (22, 1, 19);
INSERT INTO `auth_group_permissions` VALUES (23, 1, 20);
INSERT INTO `auth_group_permissions` VALUES (24, 1, 21);
INSERT INTO `auth_group_permissions` VALUES (25, 1, 22);
INSERT INTO `auth_group_permissions` VALUES (26, 1, 23);
INSERT INTO `auth_group_permissions` VALUES (27, 1, 24);
INSERT INTO `auth_group_permissions` VALUES (28, 1, 25);
INSERT INTO `auth_group_permissions` VALUES (29, 1, 26);
INSERT INTO `auth_group_permissions` VALUES (30, 1, 27);
INSERT INTO `auth_group_permissions` VALUES (31, 1, 28);
INSERT INTO `auth_group_permissions` VALUES (32, 1, 29);
INSERT INTO `auth_group_permissions` VALUES (33, 1, 30);
INSERT INTO `auth_group_permissions` VALUES (128, 1, 31);
INSERT INTO `auth_group_permissions` VALUES (129, 1, 32);
INSERT INTO `auth_group_permissions` VALUES (130, 1, 33);
INSERT INTO `auth_group_permissions` VALUES (138, 2, 1);
INSERT INTO `auth_group_permissions` VALUES (139, 2, 2);
INSERT INTO `auth_group_permissions` VALUES (140, 2, 3);
INSERT INTO `auth_group_permissions` VALUES (35, 2, 4);
INSERT INTO `auth_group_permissions` VALUES (36, 2, 5);
INSERT INTO `auth_group_permissions` VALUES (37, 2, 6);
INSERT INTO `auth_group_permissions` VALUES (38, 2, 7);
INSERT INTO `auth_group_permissions` VALUES (39, 2, 8);
INSERT INTO `auth_group_permissions` VALUES (40, 2, 9);
INSERT INTO `auth_group_permissions` VALUES (41, 2, 13);
INSERT INTO `auth_group_permissions` VALUES (42, 2, 14);
INSERT INTO `auth_group_permissions` VALUES (43, 2, 15);
INSERT INTO `auth_group_permissions` VALUES (44, 2, 16);
INSERT INTO `auth_group_permissions` VALUES (45, 2, 17);
INSERT INTO `auth_group_permissions` VALUES (46, 2, 18);
INSERT INTO `auth_group_permissions` VALUES (47, 2, 19);
INSERT INTO `auth_group_permissions` VALUES (48, 2, 20);
INSERT INTO `auth_group_permissions` VALUES (49, 2, 21);
INSERT INTO `auth_group_permissions` VALUES (50, 2, 22);
INSERT INTO `auth_group_permissions` VALUES (51, 2, 23);
INSERT INTO `auth_group_permissions` VALUES (52, 2, 24);
INSERT INTO `auth_group_permissions` VALUES (53, 2, 25);
INSERT INTO `auth_group_permissions` VALUES (54, 2, 26);
INSERT INTO `auth_group_permissions` VALUES (55, 2, 27);
INSERT INTO `auth_group_permissions` VALUES (56, 2, 28);
INSERT INTO `auth_group_permissions` VALUES (57, 2, 29);
INSERT INTO `auth_group_permissions` VALUES (58, 2, 30);
INSERT INTO `auth_group_permissions` VALUES (131, 2, 31);
INSERT INTO `auth_group_permissions` VALUES (132, 2, 32);
INSERT INTO `auth_group_permissions` VALUES (133, 2, 33);
INSERT INTO `auth_group_permissions` VALUES (141, 3, 1);
INSERT INTO `auth_group_permissions` VALUES (142, 3, 2);
INSERT INTO `auth_group_permissions` VALUES (143, 3, 3);
INSERT INTO `auth_group_permissions` VALUES (66, 3, 7);
INSERT INTO `auth_group_permissions` VALUES (67, 3, 8);
INSERT INTO `auth_group_permissions` VALUES (68, 3, 9);
INSERT INTO `auth_group_permissions` VALUES (69, 3, 16);
INSERT INTO `auth_group_permissions` VALUES (70, 3, 17);
INSERT INTO `auth_group_permissions` VALUES (71, 3, 18);
INSERT INTO `auth_group_permissions` VALUES (72, 3, 19);
INSERT INTO `auth_group_permissions` VALUES (73, 3, 20);
INSERT INTO `auth_group_permissions` VALUES (74, 3, 21);
INSERT INTO `auth_group_permissions` VALUES (75, 3, 22);
INSERT INTO `auth_group_permissions` VALUES (76, 3, 23);
INSERT INTO `auth_group_permissions` VALUES (77, 3, 24);
INSERT INTO `auth_group_permissions` VALUES (78, 3, 25);
INSERT INTO `auth_group_permissions` VALUES (79, 3, 26);
INSERT INTO `auth_group_permissions` VALUES (80, 3, 27);
INSERT INTO `auth_group_permissions` VALUES (81, 3, 28);
INSERT INTO `auth_group_permissions` VALUES (82, 3, 29);
INSERT INTO `auth_group_permissions` VALUES (83, 3, 30);
INSERT INTO `auth_group_permissions` VALUES (134, 3, 31);
INSERT INTO `auth_group_permissions` VALUES (135, 3, 32);
INSERT INTO `auth_group_permissions` VALUES (136, 3, 33);
INSERT INTO `auth_group_permissions` VALUES (97, 4, 16);
INSERT INTO `auth_group_permissions` VALUES (98, 4, 17);
INSERT INTO `auth_group_permissions` VALUES (99, 4, 18);
INSERT INTO `auth_group_permissions` VALUES (101, 4, 19);
INSERT INTO `auth_group_permissions` VALUES (102, 4, 20);
INSERT INTO `auth_group_permissions` VALUES (103, 4, 21);
INSERT INTO `auth_group_permissions` VALUES (104, 4, 22);
INSERT INTO `auth_group_permissions` VALUES (105, 4, 23);
INSERT INTO `auth_group_permissions` VALUES (106, 4, 24);
INSERT INTO `auth_group_permissions` VALUES (108, 4, 25);
INSERT INTO `auth_group_permissions` VALUES (109, 4, 26);
INSERT INTO `auth_group_permissions` VALUES (110, 4, 27);
INSERT INTO `auth_group_permissions` VALUES (111, 4, 28);
INSERT INTO `auth_group_permissions` VALUES (112, 4, 29);
INSERT INTO `auth_group_permissions` VALUES (113, 4, 30);
INSERT INTO `auth_group_permissions` VALUES (100, 4, 31);
INSERT INTO `auth_group_permissions` VALUES (107, 4, 32);
INSERT INTO `auth_group_permissions` VALUES (114, 4, 33);
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`) USING BTREE,
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=478 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add config', 1, 'add_config');
INSERT INTO `auth_permission` VALUES (2, 'Can change config', 1, 'change_config');
INSERT INTO `auth_permission` VALUES (3, 'Can delete config', 1, 'delete_config');
INSERT INTO `auth_permission` VALUES (4, 'Can add project', 2, 'add_project');
INSERT INTO `auth_permission` VALUES (5, 'Can change project', 2, 'change_project');
INSERT INTO `auth_permission` VALUES (6, 'Can delete project', 2, 'delete_project');
INSERT INTO `auth_permission` VALUES (7, 'Can add project config', 3, 'add_projectconfig');
INSERT INTO `auth_permission` VALUES (8, 'Can change project config', 3, 'change_projectconfig');
INSERT INTO `auth_permission` VALUES (9, 'Can delete project config', 3, 'delete_projectconfig');
INSERT INTO `auth_permission` VALUES (10, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (11, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (12, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (13, 'Can add project member', 5, 'add_projectmember');
INSERT INTO `auth_permission` VALUES (14, 'Can change project member', 5, 'change_projectmember');
INSERT INTO `auth_permission` VALUES (15, 'Can delete project member', 5, 'delete_projectmember');
INSERT INTO `auth_permission` VALUES (16, 'Can add api', 6, 'add_api');
INSERT INTO `auth_permission` VALUES (17, 'Can change api', 6, 'change_api');
INSERT INTO `auth_permission` VALUES (18, 'Can delete api', 6, 'delete_api');
INSERT INTO `auth_permission` VALUES (19, 'Can add api group', 7, 'add_apigroup');
INSERT INTO `auth_permission` VALUES (20, 'Can change api group', 7, 'change_apigroup');
INSERT INTO `auth_permission` VALUES (21, 'Can delete api group', 7, 'delete_apigroup');
INSERT INTO `auth_permission` VALUES (22, 'Can add automation', 8, 'add_automation');
INSERT INTO `auth_permission` VALUES (23, 'Can change automation', 8, 'change_automation');
INSERT INTO `auth_permission` VALUES (24, 'Can delete automation', 8, 'delete_automation');
INSERT INTO `auth_permission` VALUES (25, 'Can add automation group', 9, 'add_automationgroup');
INSERT INTO `auth_permission` VALUES (26, 'Can change automation group', 9, 'change_automationgroup');
INSERT INTO `auth_permission` VALUES (27, 'Can delete automation group', 9, 'delete_automationgroup');
INSERT INTO `auth_permission` VALUES (28, 'Can add task', 10, 'add_task');
INSERT INTO `auth_permission` VALUES (29, 'Can change task', 10, 'change_task');
INSERT INTO `auth_permission` VALUES (30, 'Can delete task', 10, 'delete_task');
INSERT INTO `auth_permission` VALUES (31, 'Can run api', 6, 'run_api');
INSERT INTO `auth_permission` VALUES (32, 'Can run automation', 8, 'run_automation');
INSERT INTO `auth_permission` VALUES (33, 'Can run task', 10, 'run_task');
INSERT INTO `auth_permission` VALUES (349, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (350, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (351, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (352, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (353, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (354, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (355, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (356, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (357, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (358, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (359, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (360, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (361, 'Can add 接口分组', 7, 'add_apigrouplevelfirst');
INSERT INTO `auth_permission` VALUES (362, 'Can change 接口分组', 7, 'change_apigrouplevelfirst');
INSERT INTO `auth_permission` VALUES (363, 'Can delete 接口分组', 7, 'delete_apigrouplevelfirst');
INSERT INTO `auth_permission` VALUES (364, 'Can add 请求头', 8, 'add_apihead');
INSERT INTO `auth_permission` VALUES (365, 'Can change 请求头', 8, 'change_apihead');
INSERT INTO `auth_permission` VALUES (366, 'Can delete 请求头', 8, 'delete_apihead');
INSERT INTO `auth_permission` VALUES (367, 'Can add 接口', 9, 'add_apiinfo');
INSERT INTO `auth_permission` VALUES (368, 'Can change 接口', 9, 'change_apiinfo');
INSERT INTO `auth_permission` VALUES (369, 'Can delete 接口', 9, 'delete_apiinfo');
INSERT INTO `auth_permission` VALUES (370, 'Can add 接口操作历史', 10, 'add_apioperationhistory');
INSERT INTO `auth_permission` VALUES (371, 'Can change 接口操作历史', 10, 'change_apioperationhistory');
INSERT INTO `auth_permission` VALUES (372, 'Can delete 接口操作历史', 10, 'delete_apioperationhistory');
INSERT INTO `auth_permission` VALUES (373, 'Can add 请求参数', 11, 'add_apiparameter');
INSERT INTO `auth_permission` VALUES (374, 'Can change 请求参数', 11, 'change_apiparameter');
INSERT INTO `auth_permission` VALUES (375, 'Can delete 请求参数', 11, 'delete_apiparameter');
INSERT INTO `auth_permission` VALUES (376, 'Can add 请求参数Raw', 12, 'add_apiparameterraw');
INSERT INTO `auth_permission` VALUES (377, 'Can change 请求参数Raw', 12, 'change_apiparameterraw');
INSERT INTO `auth_permission` VALUES (378, 'Can delete 请求参数Raw', 12, 'delete_apiparameterraw');
INSERT INTO `auth_permission` VALUES (379, 'Can add 接口请求历史', 13, 'add_apirequesthistory');
INSERT INTO `auth_permission` VALUES (380, 'Can change 接口请求历史', 13, 'change_apirequesthistory');
INSERT INTO `auth_permission` VALUES (381, 'Can delete 接口请求历史', 13, 'delete_apirequesthistory');
INSERT INTO `auth_permission` VALUES (382, 'Can add 返回参数', 14, 'add_apiresponse');
INSERT INTO `auth_permission` VALUES (383, 'Can change 返回参数', 14, 'change_apiresponse');
INSERT INTO `auth_permission` VALUES (384, 'Can delete 返回参数', 14, 'delete_apiresponse');
INSERT INTO `auth_permission` VALUES (385, 'Can add 自动化', 65, 'add_automation');
INSERT INTO `auth_permission` VALUES (386, 'Can change 自动化', 65, 'change_automation');
INSERT INTO `auth_permission` VALUES (387, 'Can delete 自动化', 65, 'delete_automation');
INSERT INTO `auth_permission` VALUES (388, 'Can add automation2 step', 68, 'add_automation2step');
INSERT INTO `auth_permission` VALUES (389, 'Can change automation2 step', 68, 'change_automation2step');
INSERT INTO `auth_permission` VALUES (390, 'Can delete automation2 step', 68, 'delete_automation2step');
INSERT INTO `auth_permission` VALUES (391, 'Can add automation list2 automation', 69, 'add_automationlist2automation');
INSERT INTO `auth_permission` VALUES (392, 'Can change automation list2 automation', 69, 'change_automationlist2automation');
INSERT INTO `auth_permission` VALUES (393, 'Can delete automation list2 automation', 69, 'delete_automationlist2automation');
INSERT INTO `auth_permission` VALUES (394, 'Can add 邮件发送配置', 21, 'add_automationreportsendconfig');
INSERT INTO `auth_permission` VALUES (395, 'Can change 邮件发送配置', 21, 'change_automationreportsendconfig');
INSERT INTO `auth_permission` VALUES (396, 'Can delete 邮件发送配置', 21, 'delete_automationreportsendconfig');
INSERT INTO `auth_permission` VALUES (397, 'Can add 自动化执行结果', 67, 'add_automationresult');
INSERT INTO `auth_permission` VALUES (398, 'Can change 自动化执行结果', 67, 'change_automationresult');
INSERT INTO `auth_permission` VALUES (399, 'Can delete 自动化执行结果', 67, 'delete_automationresult');
INSERT INTO `auth_permission` VALUES (400, 'Can add 自动化步骤', 66, 'add_automationstep');
INSERT INTO `auth_permission` VALUES (401, 'Can change 自动化步骤', 66, 'change_automationstep');
INSERT INTO `auth_permission` VALUES (402, 'Can delete 自动化步骤', 66, 'delete_automationstep');
INSERT INTO `auth_permission` VALUES (403, 'Can add 自定义方法', 27, 'add_custommethod');
INSERT INTO `auth_permission` VALUES (404, 'Can change 自定义方法', 27, 'change_custommethod');
INSERT INTO `auth_permission` VALUES (405, 'Can delete 自定义方法', 27, 'delete_custommethod');
INSERT INTO `auth_permission` VALUES (406, 'Can add 配置', 35, 'add_globalconfig');
INSERT INTO `auth_permission` VALUES (407, 'Can change 配置', 35, 'change_globalconfig');
INSERT INTO `auth_permission` VALUES (408, 'Can delete 配置', 35, 'delete_globalconfig');
INSERT INTO `auth_permission` VALUES (409, 'Can add HOST', 28, 'add_globalhost');
INSERT INTO `auth_permission` VALUES (410, 'Can change HOST', 28, 'change_globalhost');
INSERT INTO `auth_permission` VALUES (411, 'Can delete HOST', 28, 'delete_globalhost');
INSERT INTO `auth_permission` VALUES (412, 'Can add 分组', 64, 'add_group');
INSERT INTO `auth_permission` VALUES (413, 'Can change 分组', 64, 'change_group');
INSERT INTO `auth_permission` VALUES (414, 'Can delete 分组', 64, 'delete_group');
INSERT INTO `auth_permission` VALUES (415, 'Can add 项目', 29, 'add_project');
INSERT INTO `auth_permission` VALUES (416, 'Can change 项目', 29, 'change_project');
INSERT INTO `auth_permission` VALUES (417, 'Can delete 项目', 29, 'delete_project');
INSERT INTO `auth_permission` VALUES (418, 'Can add 项目动态', 30, 'add_projectdynamic');
INSERT INTO `auth_permission` VALUES (419, 'Can change 项目动态', 30, 'change_projectdynamic');
INSERT INTO `auth_permission` VALUES (420, 'Can delete 项目动态', 30, 'delete_projectdynamic');
INSERT INTO `auth_permission` VALUES (421, 'Can add 项目成员', 31, 'add_projectmember');
INSERT INTO `auth_permission` VALUES (422, 'Can change 项目成员', 31, 'change_projectmember');
INSERT INTO `auth_permission` VALUES (423, 'Can delete 项目成员', 31, 'delete_projectmember');
INSERT INTO `auth_permission` VALUES (424, 'Can add user profile', 32, 'add_userprofile');
INSERT INTO `auth_permission` VALUES (425, 'Can change user profile', 32, 'change_userprofile');
INSERT INTO `auth_permission` VALUES (426, 'Can delete user profile', 32, 'delete_userprofile');
INSERT INTO `auth_permission` VALUES (427, 'Can add 访客', 33, 'add_visitorsrecord');
INSERT INTO `auth_permission` VALUES (428, 'Can change 访客', 33, 'change_visitorsrecord');
INSERT INTO `auth_permission` VALUES (429, 'Can delete 访客', 33, 'delete_visitorsrecord');
INSERT INTO `auth_permission` VALUES (430, 'Can add 用例定时任务', 70, 'add_automationtask');
INSERT INTO `auth_permission` VALUES (431, 'Can change 用例定时任务', 70, 'change_automationtask');
INSERT INTO `auth_permission` VALUES (432, 'Can delete 用例定时任务', 70, 'delete_automationtask');
INSERT INTO `auth_permission` VALUES (433, 'Can add Token', 34, 'add_token');
INSERT INTO `auth_permission` VALUES (434, 'Can change Token', 34, 'change_token');
INSERT INTO `auth_permission` VALUES (435, 'Can delete Token', 34, 'delete_token');
INSERT INTO `auth_permission` VALUES (436, 'Can add crontab', 71, 'add_crontabschedule');
INSERT INTO `auth_permission` VALUES (437, 'Can change crontab', 71, 'change_crontabschedule');
INSERT INTO `auth_permission` VALUES (438, 'Can delete crontab', 71, 'delete_crontabschedule');
INSERT INTO `auth_permission` VALUES (439, 'Can add interval', 72, 'add_intervalschedule');
INSERT INTO `auth_permission` VALUES (440, 'Can change interval', 72, 'change_intervalschedule');
INSERT INTO `auth_permission` VALUES (441, 'Can delete interval', 72, 'delete_intervalschedule');
INSERT INTO `auth_permission` VALUES (442, 'Can add periodic task', 73, 'add_periodictask');
INSERT INTO `auth_permission` VALUES (443, 'Can change periodic task', 73, 'change_periodictask');
INSERT INTO `auth_permission` VALUES (444, 'Can delete periodic task', 73, 'delete_periodictask');
INSERT INTO `auth_permission` VALUES (445, 'Can add periodic tasks', 74, 'add_periodictasks');
INSERT INTO `auth_permission` VALUES (446, 'Can change periodic tasks', 74, 'change_periodictasks');
INSERT INTO `auth_permission` VALUES (447, 'Can delete periodic tasks', 74, 'delete_periodictasks');
INSERT INTO `auth_permission` VALUES (448, 'Can add task state', 75, 'add_taskmeta');
INSERT INTO `auth_permission` VALUES (449, 'Can change task state', 75, 'change_taskmeta');
INSERT INTO `auth_permission` VALUES (450, 'Can delete task state', 75, 'delete_taskmeta');
INSERT INTO `auth_permission` VALUES (451, 'Can add saved group result', 76, 'add_tasksetmeta');
INSERT INTO `auth_permission` VALUES (452, 'Can change saved group result', 76, 'change_tasksetmeta');
INSERT INTO `auth_permission` VALUES (453, 'Can delete saved group result', 76, 'delete_tasksetmeta');
INSERT INTO `auth_permission` VALUES (454, 'Can add task', 77, 'add_taskstate');
INSERT INTO `auth_permission` VALUES (455, 'Can change task', 77, 'change_taskstate');
INSERT INTO `auth_permission` VALUES (456, 'Can delete task', 77, 'delete_taskstate');
INSERT INTO `auth_permission` VALUES (457, 'Can add worker', 78, 'add_workerstate');
INSERT INTO `auth_permission` VALUES (458, 'Can change worker', 78, 'change_workerstate');
INSERT INTO `auth_permission` VALUES (459, 'Can delete worker', 78, 'delete_workerstate');
INSERT INTO `auth_permission` VALUES (460, 'Can add task', 78, 'add_taskstate');
INSERT INTO `auth_permission` VALUES (461, 'Can change task', 78, 'change_taskstate');
INSERT INTO `auth_permission` VALUES (462, 'Can delete task', 78, 'delete_taskstate');
INSERT INTO `auth_permission` VALUES (463, 'Can add worker', 77, 'add_workerstate');
INSERT INTO `auth_permission` VALUES (464, 'Can change worker', 77, 'change_workerstate');
INSERT INTO `auth_permission` VALUES (465, 'Can delete worker', 77, 'delete_workerstate');
INSERT INTO `auth_permission` VALUES (466, 'Can add 发布项目配置', 79, 'add_publishconfig');
INSERT INTO `auth_permission` VALUES (467, 'Can change 发布项目配置', 79, 'change_publishconfig');
INSERT INTO `auth_permission` VALUES (468, 'Can delete 发布项目配置', 79, 'delete_publishconfig');
INSERT INTO `auth_permission` VALUES (469, 'Can add 项目配置', 80, 'add_projectconfig');
INSERT INTO `auth_permission` VALUES (470, 'Can change 项目配置', 80, 'change_projectconfig');
INSERT INTO `auth_permission` VALUES (471, 'Can delete 项目配置', 80, 'delete_projectconfig');
INSERT INTO `auth_permission` VALUES (472, 'Can add 自动化执行失败详情', 81, 'add_automationresultfaildetail');
INSERT INTO `auth_permission` VALUES (473, 'Can change 自动化执行失败详情', 81, 'change_automationresultfaildetail');
INSERT INTO `auth_permission` VALUES (474, 'Can delete 自动化执行失败详情', 81, 'delete_automationresultfaildetail');
INSERT INTO `auth_permission` VALUES (475, 'Can add 接口自动化覆盖', 82, 'add_apiautomationcoverage');
INSERT INTO `auth_permission` VALUES (476, 'Can change 接口自动化覆盖', 82, 'change_apiautomationcoverage');
INSERT INTO `auth_permission` VALUES (477, 'Can delete 接口自动化覆盖', 82, 'delete_apiautomationcoverage');
COMMIT;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `username` (`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
BEGIN;
INSERT INTO `auth_user` VALUES (1, 'b1324fc2b79d4b9bd29f90b9afba8e5e', '2019-07-01 14:44:26', 1, 'admin', '测试小哥', '', 'admin@test.com', 1, 1, '2019-06-30 14:50:22');
INSERT INTO `auth_user` VALUES (43, 'e10adc3949ba59abbe56e057f20f883e', NULL, 0, 'test', '测试', '', 'test@test.com', 1, 1, '2019-11-01 04:00:27');
COMMIT;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`) USING BTREE,
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`) USING BTREE,
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for authtoken_token
-- ----------------------------
DROP TABLE IF EXISTS `authtoken_token`;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`) USING BTREE,
  UNIQUE KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `authtoken_token_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of authtoken_token
-- ----------------------------
BEGIN;
INSERT INTO `authtoken_token` VALUES ('505e7eec15c69f8eb210d3ba245888c0ff66464f', '2019-06-30 14:50:23', 1);
INSERT INTO `authtoken_token` VALUES ('a6a73b377cf5b323dcc073ad0c3527221ab4a954', '2019-11-01 04:00:27', 43);
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`) USING BTREE,
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (43, 'apitest', 'apigrouplevelfirst');
INSERT INTO `django_content_type` VALUES (45, 'apitest', 'apihead');
INSERT INTO `django_content_type` VALUES (44, 'apitest', 'apiinfo');
INSERT INTO `django_content_type` VALUES (50, 'apitest', 'apioperationhistory');
INSERT INTO `django_content_type` VALUES (46, 'apitest', 'apiparameter');
INSERT INTO `django_content_type` VALUES (47, 'apitest', 'apiparameterraw');
INSERT INTO `django_content_type` VALUES (49, 'apitest', 'apirequesthistory');
INSERT INTO `django_content_type` VALUES (48, 'apitest', 'apiresponse');
INSERT INTO `django_content_type` VALUES (53, 'apitest', 'automationcaseapi');
INSERT INTO `django_content_type` VALUES (61, 'apitest', 'automationcasetestresult');
INSERT INTO `django_content_type` VALUES (51, 'apitest', 'automationgrouplevelfirst');
INSERT INTO `django_content_type` VALUES (54, 'apitest', 'automationhead');
INSERT INTO `django_content_type` VALUES (55, 'apitest', 'automationparameter');
INSERT INTO `django_content_type` VALUES (56, 'apitest', 'automationparameterraw');
INSERT INTO `django_content_type` VALUES (62, 'apitest', 'automationreportsendconfig');
INSERT INTO `django_content_type` VALUES (57, 'apitest', 'automationresponsejson');
INSERT INTO `django_content_type` VALUES (60, 'apitest', 'automationtaskruntime');
INSERT INTO `django_content_type` VALUES (52, 'apitest', 'automationtestcase');
INSERT INTO `django_content_type` VALUES (58, 'apitest', 'automationtestresult');
INSERT INTO `django_content_type` VALUES (59, 'apitest', 'automationtesttask');
INSERT INTO `django_content_type` VALUES (42, 'apitest', 'custommethod');
INSERT INTO `django_content_type` VALUES (41, 'apitest', 'globalconfig');
INSERT INTO `django_content_type` VALUES (40, 'apitest', 'globalhost');
INSERT INTO `django_content_type` VALUES (37, 'apitest', 'project');
INSERT INTO `django_content_type` VALUES (38, 'apitest', 'projectdynamic');
INSERT INTO `django_content_type` VALUES (39, 'apitest', 'projectmember');
INSERT INTO `django_content_type` VALUES (36, 'apitest', 'userprofile');
INSERT INTO `django_content_type` VALUES (63, 'apitest', 'visitorsrecord');
INSERT INTO `django_content_type` VALUES (82, 'api_test', 'apiautomationcoverage');
INSERT INTO `django_content_type` VALUES (7, 'api_test', 'apigrouplevelfirst');
INSERT INTO `django_content_type` VALUES (8, 'api_test', 'apihead');
INSERT INTO `django_content_type` VALUES (9, 'api_test', 'apiinfo');
INSERT INTO `django_content_type` VALUES (10, 'api_test', 'apioperationhistory');
INSERT INTO `django_content_type` VALUES (11, 'api_test', 'apiparameter');
INSERT INTO `django_content_type` VALUES (12, 'api_test', 'apiparameterraw');
INSERT INTO `django_content_type` VALUES (13, 'api_test', 'apirequesthistory');
INSERT INTO `django_content_type` VALUES (14, 'api_test', 'apiresponse');
INSERT INTO `django_content_type` VALUES (65, 'api_test', 'automation');
INSERT INTO `django_content_type` VALUES (68, 'api_test', 'automation2step');
INSERT INTO `django_content_type` VALUES (15, 'api_test', 'automationcaseapi');
INSERT INTO `django_content_type` VALUES (16, 'api_test', 'automationcasetestresult');
INSERT INTO `django_content_type` VALUES (17, 'api_test', 'automationgrouplevelfirst');
INSERT INTO `django_content_type` VALUES (18, 'api_test', 'automationhead');
INSERT INTO `django_content_type` VALUES (69, 'api_test', 'automationlist2automation');
INSERT INTO `django_content_type` VALUES (19, 'api_test', 'automationparameter');
INSERT INTO `django_content_type` VALUES (20, 'api_test', 'automationparameterraw');
INSERT INTO `django_content_type` VALUES (21, 'api_test', 'automationreportsendconfig');
INSERT INTO `django_content_type` VALUES (22, 'api_test', 'automationresponsejson');
INSERT INTO `django_content_type` VALUES (67, 'api_test', 'automationresult');
INSERT INTO `django_content_type` VALUES (81, 'api_test', 'automationresultfaildetail');
INSERT INTO `django_content_type` VALUES (66, 'api_test', 'automationstep');
INSERT INTO `django_content_type` VALUES (70, 'api_test', 'automationtask');
INSERT INTO `django_content_type` VALUES (23, 'api_test', 'automationtaskruntime');
INSERT INTO `django_content_type` VALUES (24, 'api_test', 'automationtestcase');
INSERT INTO `django_content_type` VALUES (25, 'api_test', 'automationtestresult');
INSERT INTO `django_content_type` VALUES (26, 'api_test', 'automationtesttask');
INSERT INTO `django_content_type` VALUES (27, 'api_test', 'custommethod');
INSERT INTO `django_content_type` VALUES (35, 'api_test', 'globalconfig');
INSERT INTO `django_content_type` VALUES (28, 'api_test', 'globalhost');
INSERT INTO `django_content_type` VALUES (64, 'api_test', 'group');
INSERT INTO `django_content_type` VALUES (29, 'api_test', 'project');
INSERT INTO `django_content_type` VALUES (80, 'api_test', 'projectconfig');
INSERT INTO `django_content_type` VALUES (30, 'api_test', 'projectdynamic');
INSERT INTO `django_content_type` VALUES (31, 'api_test', 'projectmember');
INSERT INTO `django_content_type` VALUES (79, 'api_test', 'publishconfig');
INSERT INTO `django_content_type` VALUES (32, 'api_test', 'userprofile');
INSERT INTO `django_content_type` VALUES (33, 'api_test', 'visitorsrecord');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (34, 'authtoken', 'token');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (71, 'djcelery', 'crontabschedule');
INSERT INTO `django_content_type` VALUES (72, 'djcelery', 'intervalschedule');
INSERT INTO `django_content_type` VALUES (73, 'djcelery', 'periodictask');
INSERT INTO `django_content_type` VALUES (74, 'djcelery', 'periodictasks');
INSERT INTO `django_content_type` VALUES (75, 'djcelery', 'taskmeta');
INSERT INTO `django_content_type` VALUES (76, 'djcelery', 'tasksetmeta');
INSERT INTO `django_content_type` VALUES (78, 'djcelery', 'taskstate');
INSERT INTO `django_content_type` VALUES (77, 'djcelery', 'workerstate');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2019-06-30 14:47:09');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2019-06-30 14:47:09');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2019-06-30 14:47:09');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2019-06-30 14:47:09');
INSERT INTO `django_migrations` VALUES (5, 'api_test', '0001_initial', '2019-06-30 14:47:11');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (15, 'authtoken', '0001_initial', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (16, 'authtoken', '0002_auto_20160226_1747', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (17, 'sessions', '0001_initial', '2019-06-30 14:47:12');
INSERT INTO `django_migrations` VALUES (23, 'api_test', '0002_auto_20190722_1849', '2019-07-22 18:53:19');
INSERT INTO `django_migrations` VALUES (24, 'api_test', '0003_auto_20190723_1034', '2019-07-23 10:35:07');
INSERT INTO `django_migrations` VALUES (25, 'api_test', '0004_auto_20190724_1141', '2019-07-24 11:43:05');
INSERT INTO `django_migrations` VALUES (26, 'api_test', '0005_auto_20190724_1458', '2019-07-24 14:58:35');
INSERT INTO `django_migrations` VALUES (27, 'api_test', '0006_auto_20190731_1659', '2019-07-31 16:59:33');
INSERT INTO `django_migrations` VALUES (28, 'api_test', '0007_auto_20190731_2106', '2019-07-31 21:06:13');
INSERT INTO `django_migrations` VALUES (29, 'api_test', '0008_auto_20190801_1503', '2019-08-01 15:03:31');
INSERT INTO `django_migrations` VALUES (30, 'api_test', '0009_auto_20190820_1541', '2019-08-20 15:41:20');
INSERT INTO `django_migrations` VALUES (31, 'api_test', '0010_auto_20190820_1616', '2019-08-20 16:16:42');
INSERT INTO `django_migrations` VALUES (32, 'api_test', '0011_auto_20190822_1203', '2019-08-22 12:03:43');
INSERT INTO `django_migrations` VALUES (33, 'api_test', '0012_auto_20190822_2028', '2019-08-22 20:28:11');
INSERT INTO `django_migrations` VALUES (34, 'api_test', '0002_auto_20190826_2023', '2019-08-26 20:30:47');
INSERT INTO `django_migrations` VALUES (35, 'api_test', '0003_auto_20190827_1018', '2019-08-27 10:19:12');
INSERT INTO `django_migrations` VALUES (36, 'api_test', '0004_automationtask_status', '2019-08-27 11:38:21');
INSERT INTO `django_migrations` VALUES (37, 'api_test', '0002_auto_20190827_1139', '2019-08-27 11:52:21');
INSERT INTO `django_migrations` VALUES (38, 'api_test', '0003_automationtask', '2019-08-27 11:54:36');
INSERT INTO `django_migrations` VALUES (39, 'api_test', '0004_auto_20190827_1955', '2019-08-28 02:35:54');
INSERT INTO `django_migrations` VALUES (40, 'api_test', '0005_automationresult_project', '2019-08-29 02:21:03');
INSERT INTO `django_migrations` VALUES (41, 'api_test', '0006_auto_20190906_1040', '2019-09-06 02:41:08');
INSERT INTO `django_migrations` VALUES (42, 'admin', '0003_logentry_add_action_flag_choices', '2019-09-12 06:58:29');
INSERT INTO `django_migrations` VALUES (43, 'api_test', '0007_automationresult_api', '2019-09-12 06:58:29');
INSERT INTO `django_migrations` VALUES (44, 'api_test', '0008_auto_20190917_1737', '2019-09-17 09:38:09');
INSERT INTO `django_migrations` VALUES (45, 'djcelery', '0001_initial', '2019-09-17 12:31:24');
INSERT INTO `django_migrations` VALUES (46, 'api_test', '0009_auto_20190918_1821', '2019-09-18 10:21:43');
INSERT INTO `django_migrations` VALUES (47, 'api_test', '0011_userprofile_type', '2019-11-01 03:45:30');
INSERT INTO `django_migrations` VALUES (48, 'api_test', '0012_auto_20191101_1429', '2019-11-01 09:24:35');
INSERT INTO `django_migrations` VALUES (49, 'api_test', '0013_auto_20191101_1719', '2019-11-01 09:24:37');
INSERT INTO `django_migrations` VALUES (50, 'api_test', '0014_auto_20191101_1724', '2019-11-01 09:38:32');
INSERT INTO `django_migrations` VALUES (51, 'api_test', '0015_auto_20191101_1740', '2019-11-01 09:46:38');
INSERT INTO `django_migrations` VALUES (52, 'api_test', '0002_auto_20191210_1128', '2019-12-12 17:10:23');
INSERT INTO `django_migrations` VALUES (53, 'api_test', '0003_auto_20191210_1154', '2019-12-12 17:11:14');
INSERT INTO `django_migrations` VALUES (54, 'api_test', '0004_auto_20191211_1807', '2019-12-12 17:11:15');
INSERT INTO `django_migrations` VALUES (55, 'api_test', '0005_automationresult_user', '2019-12-18 14:16:54');
INSERT INTO `django_migrations` VALUES (56, 'api_test', '0006_publishconfig', '2019-12-20 16:11:24');
INSERT INTO `django_migrations` VALUES (57, 'api_test', '0007_auto_20191224_1120', '2019-12-24 16:15:25');
INSERT INTO `django_migrations` VALUES (58, 'api_test', '0008_auto_20191224_1614', '2019-12-24 16:15:25');
INSERT INTO `django_migrations` VALUES (59, 'api_test', '0008_auto_20191230_1826', '2019-12-30 21:28:53');
INSERT INTO `django_migrations` VALUES (60, 'api_test', '0009_merge_20191230_2127', '2019-12-30 21:28:53');
INSERT INTO `django_migrations` VALUES (61, 'api_test', '0009_auto_20200113_1621', '2020-01-14 21:40:19');
INSERT INTO `django_migrations` VALUES (62, 'api_test', '0010_merge_20200114_2138', '2020-01-14 21:40:19');
INSERT INTO `django_migrations` VALUES (63, 'api_test', '0010_apiautomationcoverage', '2020-01-16 22:29:04');
INSERT INTO `django_migrations` VALUES (64, 'api_test', '0011_apiautomationcoverage_num', '2020-01-16 22:29:04');
INSERT INTO `django_migrations` VALUES (65, 'api_test', '0012_merge_20200116_2228', '2020-01-16 22:29:04');
INSERT INTO `django_migrations` VALUES (66, 'api_test', '0013_auto_20200117_1845', '2020-01-17 18:46:33');
INSERT INTO `django_migrations` VALUES (67, 'api_test', '0014_auto_20200220_1241', '2020-02-20 12:45:03');
INSERT INTO `django_migrations` VALUES (68, 'api_test', '0015_auto_20200227_1856', '2020-02-27 18:58:01');
INSERT INTO `django_migrations` VALUES (69, 'api_test', '0016_auto_20200310_1128', '2020-03-10 11:30:14');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  KEY `django_session_expire_date_a5c62663` (`expire_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
INSERT INTO `django_session` VALUES ('kyl62ott32mda3yg8r1z6h9uzspkub54', 'MGQzZTU0NWQ3ZmFlOTc2OTUwZjc3Y2ZjODQzMDIxM2Y2Nzk4YmFjZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyZGE5NDc5YTQwMjg5NGQ2MDRiM2JiZGE1YmExZjFiYTEwMGQyYmM0In0=', '2019-07-15 14:44:26');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
