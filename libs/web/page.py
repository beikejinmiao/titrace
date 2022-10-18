#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import traceback
import requests
from requests import HTTPError
from urllib.parse import urlparse
from http.client import responses
from bs4 import BeautifulSoup
from collections import defaultdict
from conf.config import http_headers
from libs.web.url import urlfile, normal_url, absurl
from libs.web.pywget import auto_decode
from libs.logger import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RespInfo(object):
    def __init__(self, url='', title=None, text='', status_code=-1, desc=''):
        self.url = url.strip()
        self.title = title
        self.text = text
        self.status_code = status_code
        self.desc = desc if desc else responses.get(status_code, '')

    def __str__(self):
        d = self.__dict__.copy()
        del d['text']
        return str(d)


def try_crawl(url, resp=None):
    try:
        parsed = urlparse(url)
        http_headers['Referer'] = '%s://%s/' % (parsed.scheme, parsed.netloc)
        resp = requests.get(normal_url(url), timeout=5, headers=http_headers, verify=False)
        resp.raise_for_status()
        if resp.history:
            return try_crawl(resp.url, resp=resp)
    except HTTPError:
        return RespInfo(url=url, status_code=resp.status_code, desc=resp.reason)
    except Exception as e:
        logger.error('crawl url error: %s %s' % (url, repr(e)))
        return RespInfo(url=url, status_code=-1, desc=type(e).__name__)
    #
    text = auto_decode(resp.content, default=resp.text)
    return RespInfo(url=url, text=text, status_code=resp.status_code, desc=resp.reason)


"""
提取页面标题
"""


def strip(text):
    return re.sub(r'[\r\n\t]+', '', text).strip() if text else ''


def page_info(url):
    title = ''
    resp_info = try_crawl(url)
    try:
        if resp_info.text:
            soup = BeautifulSoup(resp_info.text, "lxml")  # soup = BeautifulSoup(resp.text, "lxml")
            title_labels = soup.find_all('title')
            if title_labels:
                title = title_labels[0].text
            resp_info.title = strip(title)
    except TypeError:
        # BeautifulSoup解析图片时：  TypeError: object of type 'NoneType' has no len()
        pass
    except:
        logger.error('find title error: %s' % url)
        logger.error(traceback.format_exc())
    # title为空时,默认使用从url中提取文件名
    if not resp_info.title:
        resp_info.title = urlfile(url)
    #
    if not resp_info.desc:
        resp_info.desc = responses.get(resp_info.status_code, '')
    return resp_info


def page_title(url):
    return page_info(url).title

"""
从网页中提取所有链接和标题
https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value
https://www.w3.org/TR/REC-html40/index/attributes.html
"""

URL_LABELS = {
    # 'a': 'href',  # a标签单独处理
    'area': 'href',
    'base': 'href',
    'link': 'href',

    'script': 'src',
    'audio': 'src',
    'embed': 'src',
    'source': 'src',
    'track': 'src',

    'frame': ('src', 'longdesc'),
    'iframe': ('src', 'longdesc'),
    'img': ('src', 'longdesc', 'usemap', 'lowsrc', 'dynsrc'),
    'video': ('src', 'poster'),
    'input': ('src', 'usemap', 'formaction'),

    'q': 'cite',
    'del': 'cite',
    'ins': 'cite',
    'blockquote': 'cite',

    'form': 'action',
    'head': 'profile',
    'applet': 'codebase',
    'body': 'background',
    'button': 'formaction',
    'command': 'icon',
    'meta': 'content',
    'html': ('xmlns', 'manifest'),
    'object': ('classid', 'codebase', 'data', 'usemap'),
}


def _is_url(text):
    return True if re.match(r'[A-Za-z]+://.+', text) else False


A_HREF_REGEX = re.compile(r'<a.+href=[\'"](\w+://.+?)[\'"].*>(.+?)</a>')


def page_a_href(url, text=None, regex=False):
    if text is None:
        text = try_crawl(url).text
    if not regex:
        _urls_title = dict()  # key: url, value: title
        soup = BeautifulSoup(text, "lxml")
        for ele in soup.find_all('a'):
            if 'href' in ele.attrs and _is_url(ele.attrs['href']):
                _urls_title[ele.attrs['href']] = strip(ele.string)
    else:
        _urls_title = dict(A_HREF_REGEX.findall(text))
    #
    urls_title = dict()
    for url, title in _urls_title.items():
        urls_title[normal_url(url)] = title.strip('\r\n ') if title else ''
    return urls_title


def page_href(url, text=None):
    _urls_title = defaultdict(set)  # key: href url, value: title set
    if text is None:
        text = try_crawl(url).text
    # 获取当前链接的目录路径,用于本站内部相对路径href拼接
    parts = urlparse(url)
    site = "{0.scheme}://{0.netloc}".format(parts)
    urldir = url[:url.rfind('/') + 1] if '/' in parts.path else url
    urldir = urldir if urldir.endswith('/') else (urldir + '/')  # 和href拼接时需要有/
    # 单独处理a标签
    soup = BeautifulSoup(text, "lxml")
    links = soup.find_all('a')
    for link in links:
        # 从<a>标签中提取href
        if 'href' not in link.attrs:
            continue
        href, title = link.attrs["href"], strip(link.string)
        if href.startswith("http://") or href.startswith("https://"):
            _url = href
        elif href.startswith("#") or href.startswith('javascript:'):
            continue
        elif href.startswith("//www."):     # 先只处理www.情况
            _url = parts.scheme + href      # //www.cas.cn/../../xxgkml/zgkxyxb/xbcbw/zxjc/
        elif href.startswith("/"):
            # 绝对路径href
            _url = site + href
        else:
            # 相对路径href
            _url = urldir + href
        _urls_title[absurl(_url)].add(title)
    # 提取其他标签超链接
    for label, attr in URL_LABELS.items():
        for ele in soup.find_all(label):
            if isinstance(attr, (tuple, list)):
                for _attr_ in attr:
                    if _attr_ in ele.attrs and _is_url(ele.attrs[_attr_]):
                        _urls_title[ele.attrs[_attr_]].add(strip(ele.string))
            elif attr in ele.attrs and _is_url(ele.attrs[attr]):
                _urls_title[ele.attrs[attr]].add(strip(ele.string))
    #
    candidates = re.findall(r'url\(([A-Za-z]+://.+)\)', text)       # <div style="background: url(image.png)">
    if len(candidates) > 0:
        _urls_title[candidates[0]].add('')
    #
    urls_title = dict()
    for _url, titles in _urls_title.items():
        # 同一个url在页面内多次出现,那么拼接相应的多个标题
        urls_title[normal_url(_url)] = ' '.join(titles)
    return urls_title


if __name__ == '__main__':
    print(page_href('http://www.cas.cn/'))

