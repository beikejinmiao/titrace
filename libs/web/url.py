#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import tldextract
import html as htmlparser
from urllib.parse import unquote
from collections import namedtuple
from urllib.parse import urlparse
from libs.regex import html, common_dom


def normal_url(url):
    url = unquote(htmlparser.unescape(url))
    url = re.sub(r'[\r\n\t]+', '', url).strip()
    return url


UrlSiteResult = namedtuple('UrlSiteResult', ['subdomain', 'domain', 'suffix', 'reg_domain', 'hostname'])


def urlsite(url):
    url = url.lower()
    site = ''
    if re.match(r'^\w+://', url):
        site = urlparse(url).netloc
    #
    ext = tldextract.extract(url)
    if not ext.registered_domain:
        return UrlSiteResult(subdomain='', domain='', suffix='',
                             reg_domain='', hostname=site)
    return UrlSiteResult(subdomain=ext.subdomain, domain=ext.domain, suffix=ext.suffix,
                         reg_domain=ext.registered_domain, hostname=ext.fqdn)


def urlfile(url):
    if url.endswith('/'):
        return ''
    url = urlparse(url).path    # 移除URL参数
    if html.match(url) or common_dom.match(url):
        return ''
    if re.match(r'.+\.\w{2,5}$', url) and not re.match(r'.+\.[\d_]+$', url):
        return os.path.basename(url)
    return ''


def absurl(url, site=None):
    """
    获取绝对路径URL
    将相对路径URL转成绝对路径URL,避免同一URL被重复爬取
    """
    url = normal_url(url)
    if not site:
        site = urlparse(url).netloc
    if "#" in url:
        # 移除页面内部定位符井号#,其实是同一个链接
        url = url[0:url.rfind('#')]
    while '/./' in url:
        url = url.replace('/./', '/')
    ix = url.index(site) + len(site)
    host, url_path = url[:ix], url[ix:]
    # path需以斜杠/开始,要不会陷入死循环
    # https://cms.baidu.com../../images/2022-07/f9593.png
    if not url_path.startswith('/'):
        url_path = '/' + url_path
    while '/../' in url_path:
        url_path = re.sub(r'(^|/[^/]+)/\.\./', '/', url_path)
    url_path = re.sub(r'/{2,}', '/', url_path)      # ////////url/path?a=1   -->   /url/path?a=1
    return '{host}{connector}{path}'.format(host=host,
                                            connector='' if url_path.startswith('/') else '/',
                                            path=url_path)


