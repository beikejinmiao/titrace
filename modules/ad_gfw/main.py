#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
from conf.paths import PRIVATE_RESOURCE_HOME
from libs.construct import importc
from utils.filedir import traverse, writer
from modules.ad_gfw.base import AD_GFW_HOME, datenow
from libs.logger import logger


def clear():
    if os.path.exists(AD_GFW_HOME):
        shutil.rmtree(AD_GFW_HOME)
    os.makedirs(AD_GFW_HOME)


def fetch2merge():
    domains = set()
    #
    fetch_path = 'modules.ad_gfw.feeds.%s.fetch'
    for pyfile in traverse(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feeds'),
            regex=r'^[^_].+\.py$'):
        feed = os.path.basename(pyfile)[:-3]
        logger.info('%s %s %s' % ('-'*30, feed, '-'*30))
        fetch = importc(fetch_path % feed)
        domains |= fetch()
    writer(os.path.join(PRIVATE_RESOURCE_HOME, 'ad_gfw.%s.txt' % datenow), domains)


if __name__ == '__main__':
    clear()
    fetch2merge()


