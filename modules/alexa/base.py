#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime
from conf.paths import DOWNLOAD_HOME, PRIVATE_RESOURCE_HOME
from utils.filedir import reader_g
from libs.web.downloader import download_zip


datenow = datetime.now().strftime('%Y%m%d')
MOD_DOWNLOAD_HOME = os.path.join(DOWNLOAD_HOME, 'alexa', datenow)
MOD_RESOURCE_HOME = os.path.join(PRIVATE_RESOURCE_HOME, 'alexa')
if not os.path.exists(MOD_RESOURCE_HOME):
    os.makedirs(MOD_RESOURCE_HOME)


def base_fetch(url, dirname='tmp'):
    domains = list()
    info, unzip_files = download_zip(url, outdir=os.path.join(MOD_DOWNLOAD_HOME, dirname))
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

