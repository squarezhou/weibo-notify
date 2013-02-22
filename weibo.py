#! /usr/bin/env python
#coding=utf-8

import sys
import urllib
import urllib2
import base64
import json

class Weibo:
    def __init__(self, username, password, source):
        self.auth = self.auth_encode(username, password)
        self.source = source
    
    def Timeline(self, since_id=0, count=20):
        return self.get('statuses/friends_timeline', {'since_id':since_id, 'count':count})
    
    def Follow(self, uid):
        return self.post('friendships/create', {'uid':uid})
    
    def Unfollow(self, uid):
        return self.post('friendships/destroy', {'uid':uid})
    
    def get(self, uri, params={}):
        return self.api(uri, params, 'GET')
    
    def post(self, uri, params={}):
        return self.api(uri, params, 'POST')
    
    def api(self, uri, params={}, method='GET'):
        baseurl = 'https://api.weibo.com/2/'
        url = '%s%s.json?source=%s' % (baseurl, uri, self.source)
        
        params = urllib.urlencode(params)
        
        if method == 'GET':
            url = '%s&%s' % (url, params)
            req = urllib2.Request(url)
        elif method == 'POST':
            req = urllib2.Request(url, params)
            
        req.add_header("Authorization", "Basic %s" % self.auth)
        try:
            return json.loads(urllib2.urlopen(req).read())
        except IOError, e:
            return False
    
    def auth_encode(self, username, password):
        return base64.encodestring('%s:%s' % (username, password))[:-1]
