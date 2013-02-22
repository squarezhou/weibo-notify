#! /usr/bin/env python
#coding=utf-8

from pyxmpp.jid import JID
from pyxmpp.message import Message
from pyxmpp.jabber.client import JabberClient
from pyxmpp.streamtls import TLSSettings
 
class Gtalk():
    def __init__(self, sid, spwd):
        self.sid = JID(sid)
        self.spwd = spwd
        
    def send(self, rid, msg):
        self.batch_send([(rid, msg)])
        
    def batch_send(self, msgs):
        batch_send(self.sid, self.spwd, msgs)

def xmpp_do(jid,password,function,server=None,port=None):
    class Client(JabberClient):
        def __init__(self, jid, password):
            if not jid.resource:
                jid=JID(jid.node, jid.domain, "WeiboNotifyRobot")
    
            tls_settings = TLSSettings(require = True, verify_peer = False)
    
            JabberClient.__init__(self, jid, password,
                    disco_name="Weibo Notify Robot", disco_type="bot",
                    tls_settings = tls_settings, auth_methods=("sasl:PLAIN",))

        def session_started(self):
            function(self.stream)
            self.disconnect()

    c=Client(jid,password)
    c.connect()
    try:
        c.loop(1)
    except KeyboardInterrupt:
        print u"disconnecting..."
        c.disconnect()    

def batch_send(sid, spwd, msgs):
    def fun(stream):
        for (rid, body) in msgs:
            print (rid, body)
            m=Message(to_jid=JID(rid), body=body)
            stream.send(m)
            
    xmpp_do(sid, spwd, fun)