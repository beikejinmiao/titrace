#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime
from conf.paths import DOWNLOAD_HOME
from conf.config import requests_proxy
from libs.regex import find_domains
from utils.filedir import reader_g
from libs.web.downloader import download


MOD_DOWNLOAD_HOME = os.path.join(DOWNLOAD_HOME, 'ad_gfw', datetime.now().strftime('%Y%m%d'))


def crawl(urls, outdir='tmp', extfunc=find_domains, proxies=requests_proxy):
    domains = set()
    failed_urls = dict()
    outdir = os.path.join(MOD_DOWNLOAD_HOME, outdir)
    for url in urls:
        info = download(url, outdir=outdir, proxies=proxies)
        if info.filepath:
            for line in reader_g(info.filepath):
                domains |= extfunc(line)
        # 本地文件存在不一定代表下载成功,可能只下载部分
        if not info.success:
            failed_urls[url] = info.desc
    return domains, failed_urls

