#! /usr/bin/env python
#coding=utf-8

import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

class Mysql:
    def __init__(self, host='localhost', user='test',passwd='', db='test', charset='utf8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.connect()
        
    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.user,passwd=self.passwd, db=self.db, charset=self.charset)
        self.cursor = self.conn.cursor()
        self.cursor.execute('set wait_timeout=3600')
        self.cursor.execute('set names %s' % self.charset)
    
    # 取第一行第一列
    def fetchone(self, sql):
        result = self.fetchrow(sql)
        if result:
            return result[0]
        else:
            return None
        
    # 取第一行
    def fetchrow(self, sql):
        count = self.query(sql)
        if count > 0:
            return self.cursor.fetchone()
        else:
            return None
    
    # 取所有行
    def fetchall(self, sql):
        count = self.query(sql)
        if count > 0:
            return self.cursor.fetchall()
        else:
            return None
        
    # 执行sql
    def query(self, sql):
        try:
            self.conn.ping()
        except Exception, e:
            self.conn.close()
            self.connect()
        
        result = self.cursor.execute(sql)
        self.conn.commit()
        return result