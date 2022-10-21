#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime
from conf.paths import DOWNLOAD_HOME
from utils.filedir import reader_g
from libs.web.downloader import download_zip


MOD_DOWNLOAD_HOME = os.path.join(DOWNLOAD_HOME, 'alexa', datetime.now().strftime('%Y%m%d'))


def crawl(url, outdir='tmp'):
    domains = list()
    info, unzip_files = download_zip(url, outdir=os.path.join(MOD_DOWNLOAD_HOME, outdir))
    if not info.success:
        return domains  # empty
    # 数据样例
    # 1,google.com
    # 2,youtube.com
    # 3,microsoft.com
    for line in reader_g(unzip_files[0]):
        seq, domain = line.split(',')
        domains.append(domain)
    return domains

