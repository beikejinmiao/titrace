#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
from datetime import datetime
from conf.paths import DOWNLOAD_HOME
from libs.web.downloader import download


MOD_DOWNLOAD_HOME = os.path.join(DOWNLOAD_HOME, 'alexa', datetime.now().strftime('%Y%m%d'))


def crawl(url, outdir='tmp', auto_unzip=True, top=None, names=('Rank', 'Domain'), dom_field='Domain'):
    info = download(url, outdir=os.path.join(MOD_DOWNLOAD_HOME, outdir), auto_unzip=auto_unzip)
    if not info.success:
        return list()  # empty
    #
    if auto_unzip is True:
        csv_path = info.filepath[1][0]
    else:
        csv_path = info.filepath
    df = load(csv_path, top=top, names=names)
    return df[dom_field].values.tolist()


def load(path, top=None, names=('Rank', 'Domain')):
    # 默认数据样例
    # 1,google.com
    # 2,youtube.com
    # 3,microsoft.com
    df = pd.read_csv(path, names=names)
    if top and isinstance(top, int) and top > 0:
        df = df.loc[:min(df.shape[0], top)]
    return df

