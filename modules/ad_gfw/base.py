#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime
from conf.paths import DOWNLOAD_HOME, PRIVATE_RESOURCE_HOME
from conf.config import requests_proxy
from libs.regex import find_domains
from utils.filedir import reader_g
from libs.web.downloader import download


datenow = datetime.now().strftime('%Y%m%d')
MOD_DOWNLOAD_HOME = os.path.join(DOWNLOAD_HOME, 'ad_gfw', datenow)
MOD_RESOURCE_HOME = os.path.join(PRIVATE_RESOURCE_HOME, 'ad_gfw')
if not os.path.exists(MOD_RESOURCE_HOME):
    os.makedirs(MOD_RESOURCE_HOME)


def batch_fetch(urls, dirname='tmp', extfunc=find_domains, proxies=requests_proxy):
    domains = set()
    failed_urls = dict()
    outdir = os.path.join(MOD_DOWNLOAD_HOME, dirname)
    for url in urls:
        info = download(url, outdir=outdir, proxies=proxies)
        if info.filepath:
            for line in reader_g(info.filepath):
                domains |= extfunc(line)
        # 本地文件存在不一定代表下载成功,可能只下载部分
        if not info.success:
            failed_urls[url] = info.desc
    return domains, failed_urls

