#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
from libs.web.downloader import download
from modules.alexa.base import MOD_DOWNLOAD_HOME

# https://builtwith.com/top-1m
__url__ = 'https://builtwith.com/dl/builtwith-top1m.zip'
__info__ = 'builtwith'


def fetch(outdir=None):
    domains = list()
    info = download(__url__,
                    outdir=os.path.join(MOD_DOWNLOAD_HOME, __info__) if not outdir else outdir,
                    auto_unzip=True)
    if not info.success:
        return domains    # empty

    df = pd.read_csv(info.filepath[1][0], names=['Rank', 'Domain'])
    # This list differs from traffic ranking in that it ranks by investment in websites.
    # For that reasons it more suites B2B use cases.
    # 不是按流量排序,且有大量疑似垃圾域名,只取前5k个
    return df.iloc[:5000]['Domain'].values.tolist()
