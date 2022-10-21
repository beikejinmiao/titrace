#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from libs.regex import find_domains
from modules.ad_gfw.base import crawl


# https://adguard.com/en/welcome.html
__url__ = [('https://filters.adtidy.org/windows/filters/%d.txt' % i) for i in range(1, 18)] + \
       [('https://filters.adtidy.org/windows/filters/%d.txt' % i) for i in range(101, 124)] + \
       [('https://filters.adtidy.org/windows/filters/%d.txt' % i) for i in range(200, 253)]
__info__ = "adguard"


def extract(text):
    if re.match(r'^\s*(~|@@|\|\||[a-zA-Z0-9])', text):
        text = re.sub(r'#.*?#.*', '', text)
        return find_domains(text)
    return set()


def fetch(outdir=None):
    return crawl(__url__, outdir=__info__ if not outdir else outdir, extfunc=extract, proxies=None)

