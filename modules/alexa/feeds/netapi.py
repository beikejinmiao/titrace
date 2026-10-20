#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://netapi.com/top-1-mln-websites/
__url__ = 'https://netapi.com/netapi_top1mln.csv'
__info__ = 'netapi'


def fetch(outdir=None):
    # 数据样例 (带表头, 每日更新, CC BY 4.0)
    # NetAPI_Rank,Domain
    # 1,google.com
    # 2,microsoft.com
    return crawl(__url__, outdir=__info__ if not outdir else outdir, names=None, auto_unzip=False)
