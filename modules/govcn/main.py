#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from collections import deque
from urllib.parse import urlparse
from libs.regex import is_gov_edu
from libs.web.url import urlfile
from libs.web.page import page_href, page_title
from libs.wrapper import threaded
from libs.logger import logger


class WebsiteManager(object):
    def __init__(self, start_url='https://www.sc.gov.cn/', n_thread=10, max_gov_depth=2):
        self._start_url = start_url
        self.n_thread = n_thread
        self.max_gov_depth = max(2, max_gov_depth)  # 控制政企网站爬取深度

        self.threads = list()
        self.urls = dict()  # key: url, value: 该url的title
        self.queue = deque()
        self._wait_second = 1       # seconds

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
                if depth <= 0:
                    continue
                # 新URL(已爬取网站新页面/新网站主页/新网站其他页面)
                parts = urlparse(_url_)
                homepage1 = "{0.scheme}://{0.netloc}".format(parts)
                homepage = homepage1 + '/'
                _depth_ = depth
                if is_gov_edu(parts.netloc):
                    # 政府&学校网站主页可向下爬取多层
                    if homepage == _url_ or homepage1 == _url_:
                        _depth_ = self.max_gov_depth+1
                else:
                    # 普通网站只爬取1层后结束
                    _depth_ = 1
                # TODO 未限制deque大小,可能会造成OOM问题
                self.queue.append((_url_, _depth_-1))

    def start(self):
        self.urls[self._start_url] = page_title(self._start_url)
        for i in range(self.n_thread):
            self.threads.append(self.crawl())
        self.queue.append((self._start_url, self.max_gov_depth))
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    man = WebsiteManager()
    man.start()
