#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://builtwith.com/top-1m
__url__ = 'https://builtwith.com/dl/builtwith-top1m.zip'
__info__ = 'builtwith'


def fetch(outdir=None):
    # This list differs from traffic ranking in that it ranks by investment in websites.
    # For that reasons it more suites B2B use cases.
    # 不是按流量排序,且有大量疑似垃圾域名,只取前5k个
    return crawl(__url__, outdir=__info__ if not outdir else outdir, top=5000)
