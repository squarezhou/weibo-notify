#! /usr/bin/env python
#coding=utf-8

import sys
import time
import MySQLdb
from log import Logger
from user import User
from weibo import Weibo
from mysql import Mysql
import config

reload(sys)
sys.setdefaultencoding('utf8')

class Subscribe:
    def __init__(self):
        db_config = config.getConfig('db')
        weibo_config = config.getConfig('weibo')
        app_config = config.getConfig('app')
        
        self.db = Mysql(db_config['host'], db_config['user'], db_config['passwd'], db_config['db'], db_config['charset'])
        self.user = User()
        self.wb = Weibo(weibo_config['username'], weibo_config['password'], weibo_config['appkey'])
        self.config = app_config

    def add(self, gtalk, url):
        print 'add %s %s' % (gtalk, url)
        
        if not self.user.checkUrl(url):
            return '微博URL格式错误！'
        
        if url == 'http://weibo.com/u/2268327783':
            return '您不能订阅我哦~'
        
        # 查询已订阅条数
        sql = "SELECT COUNT(uid) cnt FROM subs WHERE gtalk='%s'" % gtalk
        count = self.db.fetchone(sql)
        if count and int(count) >= int(self.config['sub_limit']):
            return '您最多只能订阅%d条哦！' % int(self.config['sub_limit'])
        
        # 查询是否已订阅
        sql = "SELECT COUNT(uid) cnt FROM subs WHERE gtalk='%s' AND url='%s'" % (gtalk, url)
        count = self.db.fetchone(sql)
        if count and int(count) > 0:
            return '您已经订阅：%s！' % url
        
        # 查询url-uid对应表
        (uid, nick) = self.user.getUidfromurl(self.db, url)
            
        if uid == -1:
            return '参数格式错误！'
        if uid == 0:
            return '账号不存在！'
        
        # 查询是否已关注
        sql = "SELECT count FROM follows WHERE uid=%d" % uid
        count = self.db.fetchone(sql)
        
        if count and int(count) > 0:
            # 关注表+1
            sql = "UPDATE follows SET count=count+1 WHERE uid=%d" % uid
        else:
            # 关注用户
            self.wb.Follow(uid)
            
            # 插入关注表
            sql = "INSERT INTO follows (uid, count) VALUES (%d, 1)" % uid
            
        self.db.query(sql)
        
        # 插入订阅表
        sql = "INSERT INTO subs (gtalk, url, uid, time) VALUES ('%s', '%s', %d, %d)" % (gtalk, url, uid, int(time.time()))
        self.db.query(sql)
        
        # 更新用户表
        sql = "REPLACE INTO users (uid, nick) VALUES (%d, '%s')" % (uid, nick)
        self.db.query(sql)
        
        return '%s 订阅成功！' % nick
    
    def delete(self, gtalk, url):
        print 'delete %s %s' % (gtalk, url)
        
        if not self.user.checkUrl(url):
            return '微博URL格式错误！'        
        
        # 查询是否已订阅
        sql = "SELECT COUNT(uid) cnt FROM subs WHERE gtalk='%s' AND url='%s'" % (gtalk, url)
        count = self.db.fetchone(sql)
        if count == None or int(count) == 0:
            return '您还未订阅：%s！' % url
        
        # 查询url-uid对应表
        (uid, nick) = self.user.getUidfromurl(self.db, url)
            
        if uid == -1:
            return '参数格式错误！'
        if uid == 0:
            return '账号不存在！'
        
        # 查询是否已关注
        sql = "SELECT count FROM follows WHERE uid=%d" % uid
        count = self.db.fetchone(sql)
        if count:
            if int(count) <= 1:
                # 删除关注表记录
                sql = "DELETE FROM follows WHERE uid=%d" % uid
                
                # 取消用户
                self.wb.Unfollow(uid)
            else:
                # 关注表-1
                sql = "UPDATE follows SET count=count-1 WHERE uid=%d" % uid
                
            self.db.query(sql)
        
        # 删除订阅表记录
        sql = "DELETE FROM subs WHERE gtalk='%s' AND url='%s'" % (gtalk, url)
        self.db.query(sql)
        
        return '删除成功！'
    
    def list(self, gtalk):
        print 'list %s' % gtalk
        
        # 查询订阅表
        sql = "SELECT subs.url, subs.uid, users.nick FROM subs, users WHERE subs.uid=users.uid AND subs.gtalk='%s' ORDER BY subs.time ASC" % gtalk
        results = self.db.fetchall(sql)
        if results:
            retstr = "您订阅的用户有：\n"

            for (idx, (url, uid, nick)) in enumerate(results):
                retstr = "%s\n%d. %s(%s)" % (retstr, (idx+1), nick, url)
                
            retstr = "%s\n\n回复'delete #对应url#'删除指定订阅" % retstr
        else:
            retstr = '您还未订阅任何用户！'
        
        return retstr
    
    def default(self, gtalk):
        return "错误命令！\n\n命令：\nlist(订阅列表)\nadd http://weibo.com/songerzhou或add http://weibo.com/u/1671527551（订阅指定微博）\ndelete http://weibo.com/songerzhou或delete http://weibo.com/u/1671527551（取消订阅指定微博）"
