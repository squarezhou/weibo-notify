#! /usr/bin/env python
#coding=utf-8

from mysql import Mysql
import config

db_config = config.getConfig('db')
db = Mysql(db_config['host'], db_config['user'], db_config['passwd'], db_config['db'], db_config['charset'])

# 初始化数据
db.query("INSERT INTO config (var, value) VALUES ('timeline_last_id', '0')")


# 清空数据
#db.query('TRUNCATE TABLE follows')
#db.query('TRUNCATE TABLE subs')
#db.query('TRUNCATE TABLE url2uid')
#db.query('TRUNCATE TABLE users')
#db.query("UPDATE config SET value='0' WHERE var='timeline_last_id'")
