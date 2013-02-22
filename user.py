#! /usr/bin/env python
#coding=utf-8

import urllib2
import re
import hashlib

class User:
    def __init__(self):
        pass
    
    def checkUrl(self, param):
        if (re.match('^http:\/\/weibo\.com\/(\w+)$(?i)', param) or re.match('^http:\/\/weibo\.com\/u\/(\d+)$(?i)', param)):
            return True
        else:
            return False
        
    def getUrlFromUid(self, uid):
        if (str(uid).isdigit()):
            return 'http://weibo.cn/u/%d' % uid
        else:
            return None
        
    def getUrlFromParam(self, param):
        print param
        if (re.match('^http:\/\/weibo\.com\/(\w+)$(?i)', param) or re.match('^http:\/\/weibo\.com\/u\/(\d+)$(?i)', param)):
            return param.replace('weibo.com', 'weibo.cn')
        else:
            return None
        
    def getInfoFromUid(self, uid):
        url = self.getUrlFromUid(uid)
        return self.getInfoFromUrl(url)
    
    def getInfoFromParam(self, param):
        url = self.getUrlFromParam(param)
        return self.getInfoFromUrl(url)
        
    def getInfoFromUrl(self, url):
        if (not url):
            return (-1, None)
        
        html = self.getHtml(url)
        if (html.count(r'User does not exists!') > 0):
            return (0, None)
        else:
            return (self.getUid(html), self.getNick(html))
    
    # 查询url-uid对应表
    def getUidfromurl(self, db, url):
        sql = "SELECT uid FROM url2uid WHERE eu='%s'" % hashlib.md5(url).hexdigest()
        uid = db.fetchone(sql)
        if uid and int(uid) > 0:
            sql = "SELECT nick FROM users WHERE uid=%d" % uid
            nick = db.fetchone(sql)
        else:
            (uid, nick) = self.getInfoFromParam(url)
            
            # 插入url-uid对应表
            sql = "INSERT INTO url2uid (eu, url, uid) VALUES ('%s', '%s', %d)" % (hashlib.md5(url).hexdigest(), url, uid)
            db.query(sql)
        
        return (uid, nick)
    
    def getListFromUid(self, uid):
        # todo: 顺便更新nick
        url = self.getUrlFromUid(uid)
        html = self.getHtml(url)
        return self.getList(html)
    
    def getList(self, html):
        regex = r'<div\sclass=\"c\"\sid=\"M\_(.+?)\">.+?<span\sclass=\"ct\">(.+?)&nbsp;.+?<\/span><\/div><\/div><div\sclass=\"s\"><\/div>'
        return re.findall(regex, html)    
    
    def getHtml(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')]
        return opener.open(url).read()
    
    def getUid(self, html):
        regex = r'<img\ssrc=\"http:\/\/.+?\.sinaimg\.cn\/(\d+?)\/50\/.+?\"\salt=\"头像\"\sclass=\"por\"\s\/>'
        return int(re.search(regex, html).group(1))
    
    def getNick(self, html):
        regex = r'<div\sclass=\"ut\"><span\sclass=\"ctt\">(.+?)<'
        return re.search(regex, html).group(1)
