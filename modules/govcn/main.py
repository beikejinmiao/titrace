#!/usr/bin/env python
# -*- coding:utf-8 -*-
from queue import Queue
from urllib.parse import urlparse
from libs.regex import is_gov_edu
from libs.web.url import urlfile
from libs.web.page import page_href, page_title
from libs.wrapper import threaded
from libs.logger import logger


class CrawlManager(object):
    def __init__(self, start_url, n_thread=10, max_gov_depth=2):
        self._start_url = start_url
        self.n_thread = n_thread
        self.max_gov_depth = max(2, max_gov_depth)  # 控制政企网站爬取深度

        self.threads = list()
        self.urls = dict()  # key: url, value: 该url的title
        self.queue = Queue(500000)

    @threaded(daemon=True, start=False)
    def crawl(self):
        while True:
            url, depth = self.queue.get(block=True)
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
                self.queue.put((_url_, _depth_-1))

    def start(self):
        self.urls[self._start_url] = page_title(self._start_url)
        for i in range(self.n_thread):
            self.threads.append(self.crawl())
        self.queue.put((self._start_url, self.max_gov_depth))
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    man = CrawlManager('https://www.sc.gov.cn/')
    man.start()
