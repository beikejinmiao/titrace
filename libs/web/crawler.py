#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests
import copy
import traceback
from urllib.parse import urlparse
from collections import deque
from collections.abc import Iterable
from bs4 import BeautifulSoup
from conf.config import http_headers
from libs.regex import img, video, executable
from libs.web.url import urlsite, normal_url
from libs.web.url import urlfile, absurl
from libs.web.page import RespInfo
from libs.web.pywget import auto_decode
from libs.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# http://www.bjamu.cn/mailto:hr@hofu.co
MAIL_URL_REGEX = re.compile(r'/mailto:.+?@\w+\.\w+', re.I)


def strip(text):
    return re.sub(r'[\r\n\t]+', '', text).strip() if text else ''


class UrlFileInfo(RespInfo):
    def __init__(self, url='', url_from='', title=None,
                 filename=None, text='', status_code=-1, desc=''):
        super().__init__(url=url, title=title if title else filename,
                         text=text, status_code=status_code, desc=desc)
        self.url_from = url_from    # url来源网页
        self.filename = filename    # 远程文件名


class Spider(object):
    def __init__(self, start_url, limited_sites=None, headers=None, timeout=10, hsts=False):
        self._start_url = normal_url(start_url)
        self.site = urlsite(self._start_url).reg_domain
        # 是否限制只爬取同站网页
        if limited_sites is False:
            self.limited_sites = None           # 不做任何限制
        else:
            self.limited_sites = set()
            self.limited_sites.add(self.site)   # 默认包含本站
            if isinstance(limited_sites, Iterable):
                for site in limited_sites:
                    self.limited_sites.add(urlsite(site).reg_domain)    # 限定范围
        self._same_site = True if self.limited_sites is not None and len(self.limited_sites) == 1 else False
        #
        self.urls = dict()          # key: url, value: 该url的信息
        self.urls[self._start_url] = UrlFileInfo(url=self._start_url, filename=urlfile(self._start_url))
        self._broken_urls = dict()
        self._file_urls = dict()
        self.__urlpath_limit = dict()       # 限制某个URL路径下的最大数量(某些查询页面参数组合范围极大)
        self.__parsed_urls = set()
        #
        self.session = requests.session()
        self.session.headers = headers if isinstance(headers, dict) and len(headers) > 0 else http_headers
        self.timeout = timeout
        #
        self.hsts = hsts                    # 是否只访问HTTPS网站链接

    def scrape(self, path_limit=None):
        """
        执行爬取&提取页面url操作
        """
        new_urls = deque([self.urls[self._start_url]])
        while len(new_urls):
            url_info = new_urls.popleft()
            url = url_info.url
            if url_info.filename:
                # 过滤部分文件链接
                if not self.filter(url_info.filename):
                    self._file_urls[url] = url_info
                    yield url_info
                continue
            # 提取url site和url路径
            """
            urlparse('https://xsc.baidu.cn/node/docs/49716.htm')
            >> ParseResult(scheme='https', netloc='xsc.baidu.cn', path='/node/docs/49716.htm', params='', query='', fragment='')
            urlparse('https://xsc.baidu.cn/?q=node/49716.htm')
            >> ParseResult(scheme='https', netloc='xsc.baidu.cn', path='/', params='', query='q=node/49716.htm', fragment='')
            urlparse('https://xsc.baidu.cn')    # 注意
            >> ParseResult(scheme='https', netloc='xsc.baidu.cn', path='', params='', query='', fragment='')
            """
            parts = urlparse(url)
            site = "{0.scheme}://{0.netloc}".format(parts)
            # 针对某些查询页面,参数组合范围极大,需要限制该路径下的URL数量,避免任务无法结束
            urlpath = site + parts.path
            if urlpath not in self.__urlpath_limit:
                self.__urlpath_limit[urlpath] = 1
            else:
                _path_cnt_ = self.__urlpath_limit[urlpath]
                if _path_cnt_ > 5000:
                    continue
                self.__urlpath_limit[urlpath] = _path_cnt_ + 1
            # 爬取正常网页
            try:
                resp = self.session.get(url, timeout=self.timeout, verify=False)
                logger.info('GET %s %s' % (url, resp.status_code))
                # https://stackoverflow.com/questions/20475552/python-requests-library-redirect-new-url
                # 如果发生重定向,更新URL,避免提取页面href后拼接错误新URL(大量404)
                if resp.history:
                    logger.info('!RedirectTo: %s' % resp.url)
                    new_url = absurl(resp.url, site=self.site if self._same_site else None)  # 更新重定向后的URL
                    new_url_info = copy.copy(url_info)
                    new_url_info.url = new_url
                    self.urls[new_url] = new_url_info
                    new_urls.append(new_url_info)
                    continue
            except Exception as e:
                logger.error('GET %s %s' % (url, e))
                self._broken_urls[url] = self.urls.get(url)
                url_info.status_code = -1
                url_info.desc = type(e).__name__
                yield url_info
                continue
            # 针对已解析过的URL页面,忽略 -- 某些重定向页面(404/403等被重定向至固定页面)会反复出现
            if url in self.__parsed_urls:
                continue
            self.__parsed_urls.add(url)
            try:
                # 获取当前链接的目录路径,用于本站内部相对路径href拼接
                urldir = url[:url.rfind('/') + 1] if '/' in parts.path else url
                urldir = urldir if urldir.endswith('/') else (urldir + '/')  # 和href拼接时需要有/
                # 解析HTML页面
                text = auto_decode(resp.content, default=resp.text)
                soup = BeautifulSoup(text, "lxml")  # soup = BeautifulSoup(text, "html.parser")
                url_info.status_code, url_info.desc,  url_info.text = resp.status_code, resp.reason, text
                if url_info.title is None or \
                        len(url_info.title) <= 2 or len(url_info.title) >= 48 or \
                        len(re.findall('[\u4e00-\u9fa5]', url_info.title)) <= 2:
                    # 来源网页的a标签中提取的描述：过短或过长或中文数量小于2，爬取后提取title标签内容
                    title_labels = soup.find_all('title')
                    if title_labels:
                        url_info.title = strip(title_labels[0].string)
                yield url_info
                # 提取页面内容里的URL
                links = soup.find_all('a')
                for link in links:
                    # 从<a>标签中提取href
                    if 'href' not in link.attrs:
                        continue
                    href, title = link.attrs["href"], strip(link.string)
                    if href.startswith("#") or href.startswith('javascript:'):
                        continue
                    if href.startswith("http://") or href.startswith("https://"):
                        new_url = href
                    elif href.startswith("/"):
                        # 绝对路径href
                        new_url = site + href
                    else:
                        # 相对路径href
                        new_url = urldir + href
                    if self.limited_sites is not None and urlsite(new_url).reg_domain not in self.limited_sites:
                        continue
                    new_url = absurl(new_url, site=self.site if self._same_site else None)
                    # 限制URL
                    if path_limit and path_limit not in new_url:
                        continue
                    # 忽略邮件URL链接： http://www.bjamu.cn/mailto:bjjpjc@163.com
                    if MAIL_URL_REGEX.search(new_url):
                        continue
                    if self.hsts and new_url.startswith('http://'):
                        new_url = 'https://' + new_url[7:]
                    new_url = normal_url(new_url)
                    if new_url and new_url not in self.urls:
                        # 保存该new_url信息
                        new_url_info = UrlFileInfo(url=new_url, url_from=url, title=title, filename=urlfile(new_url))
                        self.urls[new_url] = new_url_info
                        new_urls.append(new_url_info)
            except:
                logger.error('网页内容解析异常: %s' % url)
                logger.error(traceback.format_exc())

    def filter(self, path):
        # 默认忽略图片、音频、视频、可执行文件
        if img.match(path) or video.match(path) or executable.match(path):
            return True
        return False


if __name__ == '__main__':
    spider = Spider('https://rtx.bcsa.edu.cn/lixiao.html')
    from libs.regex import find_urls
    for resp in spider.scrape():
        if resp.text:
            print(find_urls(resp.text))

