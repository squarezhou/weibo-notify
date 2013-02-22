#! /usr/bin/env python
#coding=utf-8

import config
import logging
import notify

logger = logging.getLogger('pyxmpp')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG) # change to DEBUG for higher verbosity

gtalk_config = config.getConfig('gtalk')
g = notify.Gtalk(gtalk_config['username'], gtalk_config['password'])

g.send('songerzhou@gmail.com', 'test2')