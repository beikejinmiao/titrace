#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import tldextract
import concurrent.futures
from libs.construct import importc
from conf.paths import PRIVATE_RESOURCE_HOME
from utils.filedir import traverse, writer, reader
from modules.alexa.base import MOD_DOWNLOAD_HOME, MOD_RESOURCE_HOME, datenow
from libs.logger import logger


def clear():
    if os.path.exists(MOD_DOWNLOAD_HOME):
        shutil.rmtree(MOD_DOWNLOAD_HOME)
    os.makedirs(MOD_DOWNLOAD_HOME)


def async_fetch():
    # 清除旧数据
    clear()
    #
    hosts, domains = list(), list()
    _existed_hosts, _existed_domains = set(), set()
    alexa_top100k_sites = list()
    #
    threads = list()
    fetch_path = 'modules.alexa.feeds.%s.fetch'
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
    # ddns = tuple(reader(os.path.join(PRIVATE_RESOURCE_HOME, 'ddns.txt')))
    # domextract = tldextract.TLDExtract(include_psl_private_domains=True, extra_suffixes=ddns)
    domextract = tldextract.TLDExtract()

    for i in range(1000000):
        for result in results:
            if i >= len(result):
                continue
            host = result[i]
            if host in _existed_hosts:
                continue
            hosts.append(host)
            _existed_hosts.add(host)
            #
            domain = domextract(host).registered_domain
            if domain in _existed_domains:
                continue
            domains.append(domain)
            _existed_domains.add(domain)
            if i < 100000:
                alexa_top100k_sites.append(domain)

    def save(filename, dataset):
        path = os.path.join(MOD_RESOURCE_HOME, filename)
        writer(path, dataset, sort=None)
        logger.info('write to %s' % path)

    save('alexa.%s.txt' % datenow, domains)
    save('alexa.host.%s.txt' % datenow, hosts)
    save('alexa.top100k.%s.txt' % datenow, alexa_top100k_sites)


if __name__ == '__main__':
    async_fetch()
