#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from libs.regex import find_domains
from utils.filedir import reader_g
from modules.ad_gfw.base import downloads
from modules.ad_gfw.base import AD_GFW_HOME


# https://easylist.to/
__url__ = [
    'https://easylist-downloads.adblockplus.org/Liste_AR.txt',
    'https://easylist-downloads.adblockplus.org/easylistitaly.txt',
    'https://easylist-downloads.adblockplus.org/easylistdutch.txt',
    'https://easylist-downloads.adblockplus.org/liste_fr.txt',
    'https://easylist-downloads.adblockplus.org/easylistchina.txt',
    'https://easylist-downloads.adblockplus.org/antiadblockfilters.txt',

    'https://easylist.to/easylistgermany/easylistgermany.txt',
    'https://raw.githubusercontent.com/easylist/EasyListHebrew/master/EasyListHebrew.txt',
    'https://raw.githubusercontent.com/tomasko126/easylistczechandslovak/master/filters.txt',
    'https://stanev.org/abp/adblock_bg.txt',
    'https://raw.githubusercontent.com/heradhis/indonesianadblockrules/master/subscriptions/abpindo.txt',
    'https://notabug.org/latvian-list/adblock-latvian/raw/master/lists/latvian-list.txt',
]
__info__ = "easylist"


def fetch():
    domains = set()
    paths = downloads(__url__, outdir=os.path.join(AD_GFW_HOME, __info__))
    for filepath in paths:
        for line in reader_g(filepath):
            if re.match(r'^\s*(@@|\|\||[a-zA-Z0-9])', line):
                domains |= find_domains(line)
    return domains

