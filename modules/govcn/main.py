#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os
import time
import traceback
from collections import deque, defaultdict
from urllib.parse import urlparse
from libs.timer import timer
from libs.regex import is_gov_edu
from libs.web.url import urlfile, urlsite
from libs.web.page import page_href, page_title
from libs.wrapper import threaded
from modules.core import AbstractManager
from libs.logger import logger


class WebsiteManager(AbstractManager):
    """
    政企网站每个站点(主站和子站)最多爬取N个网页,其他网站只爬取站点(主站和子站)主页
    """
    def __init__(self, start_url='https://www.sc.gov.cn/', n_thread=10, max_gov_link=10):
        super().__init__('govcn')
        #
        self._start_url = start_url
        self.n_thread = n_thread
        self.max_gov_link = max(1, max_gov_link)  # 控制政企网站爬取深度
        self._host_url_limit = defaultdict(lambda: 0)
        #
        self.threads = list()
        self.urls = dict()      # key: url, value: 该url的title
        self.hosts = dict()     # key: url host, value: 该host的title(首次)
        self.domains = dict()
        self.queue = deque()
        self._wait_second = 1       # seconds

    def append(self, host, domain=None, title='', update=False):
        host = str(host).strip().lower()
        if not host:
            return
        if host not in self.hosts:
            self.hosts[host] = title
        else:
            old_title = self.hosts[host]
            if title and (old_title or update is True):
                self.hosts[host] = title
        #
        if domain is None:
            domain = self.domextract(host).registered_domain
        if not domain:
            return
        if domain not in self.domains:
            self.domains[domain] = title
        else:
            old_title = self.domains[domain]
            if title and (old_title or update is True):
                self.domains[domain] = title

    @staticmethod
    def _home_page(url):
        site = urlsite(url)
        parts = urlparse(url)
        _homepage = '{scheme}://{host}'.format(scheme=parts.scheme, host=site.hostname)
        homepage = _homepage + '/'
        #
        is_home_page = False
        if _homepage == url or homepage == url:
            is_home_page = True

        return is_home_page, site.hostname, site.reg_domain, homepage

    @threaded(daemon=True, start=False)
    def crawl(self):
        wait_time = 0
        # 持续等待1小时后,没有新URL出现,退出
        while wait_time <= 3600:
            try:
                url, title = self.queue.popleft()       # deque线程安全
            except IndexError:  # deque is empty
                wait_time += self._wait_second
                time.sleep(self._wait_second)
                continue
            wait_time = 0   # 置零
            #
            try:
                is_home_page, host, domain, homepage = self._home_page(url)
                if is_gov_edu(host):
                    # 政府&学校网站主页可爬取非主页链接
                    if self._host_url_limit[homepage] >= self.max_gov_link:
                        continue
                    self._host_url_limit[homepage] += 1
                else:
                    if not is_home_page:
                        continue
                #
                urls_title = page_href(url)
                if is_home_page:
                    # 从页面中的<title>标签获取标题并强制更新
                    home_title = urls_title[url]
                    if not title or len(re.findall('[\u4e00-\u9fa5]', home_title)) >= 2:     # 针对外网网站名,保留中文描述
                        title = home_title
                    self.append(host, domain=domain, title=title, update=True)
                logger.info('crawled url: %s %s' % (url, title))
                #
                for _url_, _title_ in urls_title.items():
                    if len(urlfile(_url_)) > 0 or _url_ in self.urls:
                        continue
                    # 新URL(已爬取网站新页面/新网站主页/新网站其他页面)
                    self.urls[_url_] = _title_
                    _is_home_page_, _host_, _domain_, _homepage_ = self._home_page(_url_)
                    # 使用页面中的超链接描述当做标题
                    if _is_home_page_:
                        self.append(_host_, domain=_domain_, title=_title_)
                    # TODO 未限制deque大小,可能会造成OOM问题
                    self.queue.append((_url_, _title_))
            except:
                logger.error(traceback.format_exc())

    @timer(10, 10)
    def regular_save(self):
        # RuntimeError: dictionary changed size during iteration
        self.builtin_save(copy=True)
        self.save(os.path.join(self.download_home, '%s.url.%s.json' % (self.module, self.date)), self.urls.copy())
        logger.info('queue size: %s' % len(self.queue))

    def start(self):
        self._init_env()
        #
        _start_url_title = page_title(self._start_url)
        self.urls[self._start_url] = _start_url_title
        for i in range(self.n_thread):
            self.threads.append(self.crawl())
        self.queue.append((self._start_url, _start_url_title))
        for thread in self.threads:
            thread.start()
        self.regular_save()     # 定期保存
        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    man = WebsiteManager(n_thread=10, max_gov_link=10)
    man.start()
