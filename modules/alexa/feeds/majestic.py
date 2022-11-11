#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://majestic.com/reports/majestic-million
__url__ = 'http://downloads.majestic.com/majestic_million.csv'
__info__ = 'majestic'


def fetch(outdir=None):
    # 数据样例
    # GlobalRank,TldRank,Domain,TLD,RefSubNets,RefIPs,IDN_Domain,IDN_TLD,PrevGlobalRank,PrevTldRank,PrevRefSubNets,PrevRefIPs
    # 1,1,google.com,com,491249,2418262,google.com,com,1,1,489595,2408964
    # 2,2,facebook.com,com,489261,2563757,facebook.com,com,2,2,487292,2552252
    return crawl(__url__, outdir=__info__ if not outdir else outdir, names=None, auto_unzip=False)


