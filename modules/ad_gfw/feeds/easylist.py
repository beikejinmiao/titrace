#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from libs.regex import find_domains
from modules.ad_gfw.base import batch_fetch


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


def extract(text):
    if re.match(r'^\s*(~|@@|\|\||[a-zA-Z0-9])', text):
        text = re.sub(r'#.*?#.*', '', text)
        return find_domains(text)
    return set()


def fetch():
    return batch_fetch(__url__, dirname=__info__, extfunc=extract)

