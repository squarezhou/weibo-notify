#! /usr/bin/env python
#coding=utf-8

import sys
import logging
import re
from subscribe import Subscribe
from daemon import Daemon
import config

from pyxmpp.all import JID,Iq,Presence,Message,StreamError
from pyxmpp.jabber.client import JabberClient
from pyxmpp.interface import implements
from pyxmpp.interfaces import *
from pyxmpp.streamtls import TLSSettings

class CommandHandler(object):
    implements(IMessageHandlersProvider, IPresenceHandlersProvider)
    
    def __init__(self, client):
        """Just remember who created this."""
        self.client = client
        self.sub = Subscribe()

    
    def get_message_handlers(self):
        return [
            ("normal", self.message),
            ]
            
    def get_presence_handlers(self):
        """Return list of (presence_type, presence_handler) tuples.

        The handlers returned will be called when matching presence stanza is
        received in a client session."""
        return [
            (None, self.presence),
            ("unavailable", self.presence),
            ("subscribe", self.presence_control),
            ("subscribed", self.presence_control),
            ("unsubscribe", self.presence_control),
            ("unsubscribed", self.presence_control),
            ]
    
    def message(self,stanza):
        subject=stanza.get_subject()
        body=stanza.get_body()
        t=stanza.get_type()
        print u'Message from %s received.' % (unicode(stanza.get_from(),)),
        if subject:
            print u'Subject: "%s".' % (subject,),
        if body:
            print u'Body: "%s".' % (body,),
        if t:
            print u'Type: "%s".' % (t,)
        else:
            print u'Type: "normal".'
        if stanza.get_type()=="headline":
            # 'headline' messages should never be replied to
            return True
        if subject:
            subject=u"Re: "+subject
            
        # run command
        # todo: 只进队列让worker线程处理，不回复；因为是同步阻塞IO模型
        body = self.run(unicode(stanza.get_from(),), body)
        
        m=Message(
            to_jid=stanza.get_from(),
            from_jid=stanza.get_to(),
            stanza_type=stanza.get_type(),
            subject=subject,
            body=body)
        if body:
            p = Presence(status=body)
            return [m, p]
        return m
    
    def presence(self,stanza):
        """Handle 'available' (without 'type') and 'unavailable' <presence/>."""
        msg=u"%s has become " % (stanza.get_from())
        t=stanza.get_type()
        if t=="unavailable":
            msg+=u"unavailable"
        else:
            msg+=u"available"

        show=stanza.get_show()
        if show:
            msg+=u"(%s)" % (show,)

        status=stanza.get_status()
        if status:
            msg+=u": "+status
        print msg

    def presence_control(self,stanza):
        """Handle subscription control <presence/> stanzas -- acknowledge
        them."""
        msg=unicode(stanza.get_from())
        t=stanza.get_type()
        if t=="subscribe":
            msg+=u" has requested presence subscription."
        elif t=="subscribed":
            msg+=u" has accepted our presence subscription request."
        elif t=="unsubscribe":
            msg+=u" has canceled his subscription of our."
        elif t=="unsubscribed":
            msg+=u" has canceled our subscription of his presence."

        print msg

        return stanza.make_accept_response()
    
    def run(self, from_jid, cmd):
        gtalk = from_jid[:from_jid.find('/')]
        matches = re.match('^add\s+(.+?)$(?i)', cmd)
        if(matches):
            return self.sub.add(gtalk, matches.group(1))
        
        matches = re.match('^delete\s+(.+?)$(?i)', cmd)
        if(matches):
            return self.sub.delete(gtalk, matches.group(1))

        matches = re.match('^list$(?i)', cmd)
        if(matches):
            return self.sub.list(gtalk)
        
        return self.sub.default(gtalk)

class Client(JabberClient):
    def __init__(self, jid, password):
        if not jid.resource:
            jid=JID(jid.node, jid.domain, "WeiboNotifyRobot")

        tls_settings = TLSSettings(require = True, verify_peer = False)

        JabberClient.__init__(self, jid, password,
                disco_name="Weibo Notify Robot", disco_type="bot",
                tls_settings = tls_settings, auth_methods=("sasl:PLAIN",))

        # add the separate components
        self.interface_providers = [
            CommandHandler(self),
            ]


#logger = logging.getLogger('pyxmpp')
#logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.INFO) # change to DEBUG for higher verbosity

class RobotDaemon(Daemon):
    def run(self):
        print u"creating client..."
        
        gtalk_config = config.getConfig('gtalk')
        c=Client(JID(gtalk_config['username']), gtalk_config['password'])
        
        print u"connecting..."
        c.connect()
        
        print u"looping..."
        try:
            c.loop(1)
        except KeyboardInterrupt:
            print u"disconnecting..."
            c.disconnect()
        
        print u"exiting..."

if __name__ == "__main__":
    daemon = RobotDaemon('/tmp/robot-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        daemon.run()
        sys.exit(2)

