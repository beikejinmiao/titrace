#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
from datetime import datetime
from conf.paths import DOWNLOAD_HOME
from libs.web.downloader import download


MOD_DOWNLOAD_HOME = os.path.join(DOWNLOAD_HOME, 'alexa', datetime.now().strftime('%Y%m%d'))


def crawl(url, outdir='tmp'):
    info = download(url, outdir=os.path.join(MOD_DOWNLOAD_HOME, outdir), auto_unzip=True)
    if not info.success:
        return list()  # empty
    # 数据样例
    # 1,google.com
    # 2,youtube.com
    # 3,microsoft.com
    df = pd.read_csv(info.filepath[1][0], names=['Rank', 'Domain'])
    return df['Domain'].values.tolist()

