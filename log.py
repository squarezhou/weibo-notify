#! /usr/bin/env python
#coding=utf-8

import logging
import os

def getLogger(logfile):
    logger = logging.getLogger('wnr')
    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

logfile = '%s/fetch.log' % os.getcwd()
Logger = getLogger(logfile)