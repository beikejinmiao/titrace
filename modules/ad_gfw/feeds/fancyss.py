#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.regex import find_domains
from modules.ad_gfw.base import crawl


__url__ = [
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/WhiteList_new.txt',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/adblock.conf',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/apple_china.txt',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/cdn.txt',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/gfwlist.conf',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/google_china.txt',
]
__info__ = "fancyss"


def fetch(outdir=None):
    return crawl(__url__, outdir=__info__ if not outdir else outdir)



