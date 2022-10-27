#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
from collections import deque
from urllib.parse import urlparse
from libs.timer import timer
from libs.regex import is_gov_edu
from libs.web.url import urlfile, urlsite
from libs.web.page import page_href, page_title
from libs.wrapper import threaded
from modules.core import AbstractManager
from libs.logger import logger


class WebsiteManager(AbstractManager):
    def __init__(self, start_url='https://www.sc.gov.cn/', n_thread=10, max_gov_depth=2):
        super().__init__('govcn')
        #
        self._start_url = start_url
        self.n_thread = n_thread
        self.max_gov_depth = max(2, max_gov_depth)  # 控制政企网站爬取深度

        self.threads = list()
        self.urls = dict()      # key: url, value: 该url的title
        self.hosts = dict()     # key: url host, value: 该host的title(首次)
        self.domains = dict()
        self.queue = deque()
        self._wait_second = 1       # seconds

    def append(self, host, domain='', title=''):
        host = str(host).strip()
        if not host or host in self.hosts:
            return
        self.hosts[host] = title
        if not domain or domain in self.domains:
            return
        self.domains[domain] = title

    @staticmethod
    def _is_home_page(url):
        parts = urlparse(url)
        homepage1 = "{0.scheme}://{0.netloc}".format(parts)
        homepage = homepage1 + '/'
        if homepage == url or homepage1 == url:
            return True
        return False

    @threaded(daemon=True, start=False)
    def crawl(self):
        wait_time = 0
        # 持续等待1小时后,没有新URL出现,退出
        while wait_time <= 3600:
            try:
                url, depth = self.queue.popleft()       # deque线程安全
            except IndexError:  # deque is empty
                wait_time += self._wait_second
                time.sleep(self._wait_second)
                continue
            wait_time = 0   # 置零
            #
            logger.info('crawl url: %s %s' % (url, self.urls[url]))
            urls_title = page_href(url)
            for _url_, title in urls_title.items():
                if len(urlfile(_url_)) > 0 or _url_ in self.urls:
                    continue
                self.urls[_url_] = title
                is_home_page = self._is_home_page(_url_)
                #
                site = urlsite(_url_)
                host, domain = site.hostname, site.reg_domain
                if is_home_page:
                    self.append(host, domain=domain, title=title)
                if depth <= 0:
                    continue
                # 新URL(已爬取网站新页面/新网站主页/新网站其他页面)
                _depth_ = depth     # 重新赋值,避免多线程下
                if is_gov_edu(host):
                    # 政府&学校网站主页可向下爬取多层
                    if is_home_page:
                        _depth_ = self.max_gov_depth+1
                else:
                    # 普通网站只爬取1层后结束
                    _depth_ = 1
                # TODO 未限制deque大小,可能会造成OOM问题
                self.queue.append((_url_, _depth_-1))

    @timer(10, 10)
    def regular_save(self):
        # RuntimeError: dictionary changed size during iteration
        self.builtin_save(copy=True)
        self.save(os.path.join(self.download_home, '%s.url.%s.json' % (self.module, self.date)), self.urls.copy())

    def start(self):
        self._init_env()
        #
        self.urls[self._start_url] = page_title(self._start_url)
        for i in range(self.n_thread):
            self.threads.append(self.crawl())
        self.queue.append((self._start_url, self.max_gov_depth))
        for thread in self.threads:
            thread.start()
        self.regular_save()     # 定期保存
        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    man = WebsiteManager()
    man.start()
