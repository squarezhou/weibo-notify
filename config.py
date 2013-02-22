#! /usr/bin/env python
#coding=utf-8

import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config.ini")

def getConfig(section):
    config = {}
    for k in cf.options(section):
        config[k] = cf.get(section, k)
    return config