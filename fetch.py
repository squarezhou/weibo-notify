#! /usr/bin/env python
#coding=utf-8

import sys
import time
import notify
from log import Logger
from user import User
from daemon import Daemon
from weibo import Weibo
from mysql import Mysql
import config

db_config = config.getConfig('db')
db = Mysql(db_config['host'], db_config['user'], db_config['passwd'], db_config['db'], db_config['charset'])

user = User()

weibo_config = config.getConfig('weibo')
wb = Weibo(weibo_config['username'], weibo_config['password'], weibo_config['appkey'])

gtalk_config = config.getConfig('gtalk')
g = notify.Gtalk(gtalk_config['username'], gtalk_config['password'])

def fetch():
    # 取friends timeline
    sql = "SELECT value FROM config WHERE var='timeline_last_id'"
    timeline_last_id = int(db.fetchone(sql))
    
    timeline = wb.Timeline(timeline_last_id, 10)
    
    if len(timeline['statuses']) > 0:
        msgs = []
        for tl in timeline['statuses']:
            (id, text, uid, nick) = (tl['id'], tl['text'], int(tl['user']['id']), tl['user']['screen_name'])
            print (id, text, uid, nick)
            
            # 更新users表
            sql = "UPDATE users SET nick='%s' WHERE uid=%d" % (nick, int(uid))
            db.query(sql)
            
            msg = "您订阅的账号 %s 发布了一条新的微博：\n%s" % (nick, text)
            
            # 取订阅uid的GTalk
            sql = "SELECT gtalk FROM subs WHERE uid=%d" % uid
            results = db.fetchall(sql)
            
            if results:
                for (gtalk,) in results:
                    # 添加GTalk通知到列表
                    msgs.append((gtalk, msg))
        
        # 发送GTalk通知
        g.batch_send(msgs)
        
        # 更新last_id
        sql = "UPDATE config SET value='%s' WHERE var='timeline_last_id'" % str(timeline['statuses'][0]['id'])
        db.query(sql)

class FetchDaemon(Daemon):
    def run(self):
        while True:
            fetch()
            print '---'
            #Logger.info('-----------------------------------')
            time.sleep(60)

if __name__ == "__main__":
    fetch()
#    daemon = FetchDaemon('/tmp/fetch-daemon.pid')
#    if len(sys.argv) == 2:
#        if 'start' == sys.argv[1]:
#            daemon.start()
#        elif 'stop' == sys.argv[1]:
#            daemon.stop()
#        elif 'restart' == sys.argv[1]:
#            daemon.restart()
#        else:
#            print "Unknown command"
#            sys.exit(2)
#        sys.exit(0)
#    else:
#        daemon.run()
#        sys.exit(2)
