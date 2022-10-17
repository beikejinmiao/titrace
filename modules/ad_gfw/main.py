#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
from conf.paths import PRIVATE_RESOURCE_HOME
from libs.construct import importc
from utils.filedir import traverse, writer, dump_json
from modules.ad_gfw.base import AD_GFW_HOME, datenow
from libs.logger import logger


def clear():
    if os.path.exists(AD_GFW_HOME):
        shutil.rmtree(AD_GFW_HOME)
    os.makedirs(AD_GFW_HOME)


def fetch2merge():
    domains = set()
    failed_urls = dict()

    def save():
        writer(os.path.join(PRIVATE_RESOURCE_HOME, 'ad_gfw.%s.txt' % datenow), domains)
        dump_json(os.path.join(PRIVATE_RESOURCE_HOME, 'ad_gfw.failed_urls.%s.json' % datenow), failed_urls)
    #
    fetch_path = 'modules.ad_gfw.feeds.%s.fetch'
    for pyfile in traverse(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feeds'),
            regex=r'^[^_].+\.py$'):
        feed = os.path.basename(pyfile)[:-3]
        logger.info('%s %s %s' % ('-'*30, feed, '-'*30))
        fetch = importc(fetch_path % feed)
        _domains_, _failed_urls_ = fetch()
        domains |= _domains_
        failed_urls.update(_failed_urls_)
        save()  # 临时保存,避免程序异常终止导致损失全部数据
    save()


if __name__ == '__main__':
    clear()
    fetch2merge()


