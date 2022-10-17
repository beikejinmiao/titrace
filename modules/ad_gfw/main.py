#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import concurrent.futures
from conf.paths import PRIVATE_RESOURCE_HOME
from libs.construct import importc
from utils.filedir import traverse, writer, dump_json
from modules.ad_gfw.base import DOWNLOAD_HOME, AD_GFW_HOME, datenow
from libs.logger import logger


def clear():
    if os.path.exists(AD_GFW_HOME):
        shutil.rmtree(AD_GFW_HOME)
    os.makedirs(AD_GFW_HOME)


def fetch():
    # 清除旧数据
    clear()
    #
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
        func = importc(fetch_path % feed)      # 动态加载fetch方法
        _domains_, _failed_urls_ = func()
        domains |= _domains_
        failed_urls.update(_failed_urls_)
        save()  # 临时保存,避免程序异常终止导致损失全部数据
    save()


def async_fetch():
    # 清除旧数据
    clear()
    #
    domains = set()
    failed_urls = dict()

    def save():
        writer(os.path.join(PRIVATE_RESOURCE_HOME, 'ad_gfw.%s.txt' % datenow), domains)
        dump_json(os.path.join(PRIVATE_RESOURCE_HOME, 'ad_gfw.failed_urls.%s.json' % datenow), failed_urls)
    #
    threads = list()
    fetch_path = 'modules.ad_gfw.feeds.%s.fetch'
    for pyfile in traverse(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feeds'),
            regex=r'^[^_].+\.py$'):
        feed = os.path.basename(pyfile)[:-3]
        logger.info('%s %s %s' % ('-'*30, feed, '-'*30))
        func = importc(fetch_path % feed)      # 动态加载fetch方法
        threads.append(func)
    # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(method) for method in threads]
        results = [future.result() for future in futures]
    for _domains_, _failed_urls_ in results:
        domains |= _domains_
        failed_urls.update(_failed_urls_)
    save()


def check():
    from utils.filedir import reader_g
    from modules.ad_gfw.base import is_plain_file
    for filepath in traverse(os.path.join(DOWNLOAD_HOME, 'ad_gfw.'+'20221017')):
        if not is_plain_file(filepath):
            continue
        target = '0.0.0www1.sedoparking.com'
        for line in reader_g(filepath, debug=False):
            if target in line:
                logger.info('"%s" in "%s"' % (target, filepath))


if __name__ == '__main__':
    # fetch()
    async_fetch()
    # check()


