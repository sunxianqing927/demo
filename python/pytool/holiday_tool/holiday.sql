
-- ----------------------------
-- Table structure for holiday
-- ----------------------------
CREATE TABLE IF NOT EXISTS `holiday`  (
  `date` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `trade_flag` int(11) NOT NULL,
  `week_day` int(11) NOT NULL,
  PRIMARY KEY (`date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

