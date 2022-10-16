#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from libs.regex import find_domains
from utils.filedir import reader_g
from modules.ad_gfw.base import downloads
from modules.ad_gfw.base import AD_GFW_HOME


__url__ = [
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/WhiteList_new.txt',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/adblock.conf',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/apple_china.txt',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/cdn.txt',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/gfwlist.conf',
    'https://raw.githubusercontent.com/hq450/fancyss/master/rules/google_china.txt',
]
__name__ = "fancyss"


def fetch():
    paths = downloads(__url__, outdir=os.path.join(AD_GFW_HOME, __name__))
    domains = set()
    for filepath in paths:
        for line in reader_g(filepath):
            domains |= find_domains(line)
    return domains

