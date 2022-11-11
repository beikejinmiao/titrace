#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
from datetime import datetime
import tldextract
import concurrent.futures
from libs.construct import importc
from libs.web.downloader import is_data_file
from conf.paths import DOWNLOAD_HOME, PRIVATE_RESOURCE_HOME
from utils.filedir import traverse, writer, reader_g
from libs.logger import logger


class AbstractManager(object):
    def __init__(self, module, date=None):
        self.module = module
        self.date = datetime.now().strftime('%Y%m%d') if not date else date
        self.download_home = os.path.join(DOWNLOAD_HOME, self.module, self.date)
        self.resource_home = os.path.join(PRIVATE_RESOURCE_HOME, self.module)
        self.hosts = None
        self.domains = None
        # ddns = tuple(reader(os.path.join(PRIVATE_RESOURCE_HOME, 'ddns.txt')))
        # self.domextract = tldextract.TLDExtract(include_psl_private_domains=True, extra_suffixes=ddns)
        self.domextract = tldextract.TLDExtract()

    def _init_env(self):
        if os.path.exists(self.download_home):
            shutil.rmtree(self.download_home)
            logger.warning('clear: %s' % self.download_home)
        os.makedirs(self.download_home)
        logger.info('mkdir: %s' % self.download_home)
        if not os.path.exists(self.resource_home):
            os.makedirs(self.resource_home)
            logger.info('mkdir: %s' % self.resource_home)

    def crawl(self):
        pass

    def append(self, host):
        pass

    def save(self, filename, dataset):
        path = os.path.join(self.resource_home, filename)
        writer(path, dataset, sort=None)
        logger.info('save to %s' % path)

    def builtin_save(self, copy=False):
        """
        copy设置为True时，避免多线程异步保存触发异常RuntimeError: dictionary changed size during iteration
        """
        if self.domains is not None:
            if isinstance(self.domains, dict):
                suffix = 'json'
            else:
                suffix = 'txt'
            self.save('%s.%s.%s' % (self.module, self.date, suffix), self.domains if not copy else self.domains.copy())
        if self.hosts is not None:
            if isinstance(self.hosts, dict):
                suffix = 'json'
            else:
                suffix = 'txt'
            self.save('%s.host.%s.%s' % (self.module, self.date, suffix), self.hosts if not copy else self.hosts.copy())

    def start(self):
        pass


class AbstractFeedsManager(AbstractManager):
    def __init__(self, module, date=None):
        super().__init__(module, date=date)
        #
        self.hosts, self.domains = list(), list()       # 使用list保存添加顺序
        self._existed_hosts, self._existed_domains = set(), set()

    @property
    def _feed_fetch_funcs(self):
        functions = dict()
        fetch_path = 'modules.{module}.feeds.%s.fetch'.format(module=self.module)
        for pyfile in traverse(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), self.module, 'feeds'),
                regex=r'^[^_].+\.py$'):
            feed = os.path.basename(pyfile)[:-3]
            func = importc(fetch_path % feed)  # 动态加载fetch方法
            functions[feed] = func
        return functions

    def crawl(self):
        """
        并发下载feed
        :return:
        """
        # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = list()
            feeds = list(self._feed_fetch_funcs.keys())
            for feed in feeds:
                logger.info('%s %s %s' % ('-' * 30, feed, '-' * 30))
                futures.append(executor.submit(self._feed_fetch_funcs[feed], os.path.join(self.download_home, feed)))
            results = dict(zip(feeds, [future.result() for future in futures]))
        return results

    def runner(self):
        pass
        # 自定义处理爬取结果

    def append(self, host):
        """
        :param host:
        :return: 若发现新域名,则返回域名内容
        """
        host = str(host).strip()
        if not host or host in self._existed_hosts:
            return
        self.hosts.append(host)
        self._existed_hosts.add(host)
        domain = self.domextract(host).registered_domain
        if not domain or domain in self._existed_domains:
            return
        self.domains.append(domain)
        self._existed_domains.add(domain)
        return domain

    def traverse(self):
        """
        遍历本地文件,返回host和所在路径
        :return:
        """
        for filepath in traverse(self.download_home):
            if not is_data_file(filepath):
                continue
            for i, line in enumerate(reader_g(filepath, debug=False)):
                yield i+1, line, filepath

    def start(self, refresh=True):
        if refresh:
            self._init_env()
            self.runner()
            self.builtin_save()
        else:
            for info in self.traverse():
                self.append(info[1])

