#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

#
WORK_NAME = 'maltrace'
USER_HOME = os.path.expanduser('~')
MAIN_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CONF_HOME = os.path.join(MAIN_HOME, 'conf')
TOOLS_HOME = os.path.join(MAIN_HOME, 'tools')
PRIVATE_RESOURCE_HOME = os.path.join(MAIN_HOME, 'resources')
DOWNLOAD_HOME = os.path.join(MAIN_HOME, 'download')
if not os.path.exists(DOWNLOAD_HOME):
    os.makedirs(DOWNLOAD_HOME)

#
CONF_PATH = os.path.join(CONF_HOME, WORK_NAME+'.yaml')
LOG_FILEPATH = os.path.join(MAIN_HOME, "%s.log" % WORK_NAME)
ALEXA_BLOOM_FILTER_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'top-alexa-sites.blm')

