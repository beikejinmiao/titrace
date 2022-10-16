#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from libs.regex import find_domains
from utils.filedir import reader_g
from modules.ad_gfw.base import downloads
from modules.ad_gfw.base import AD_GFW_HOME


# https://adguard.com/en/welcome.html
__url__ = [('https://filters.adtidy.org/windows/filters/%d.txt' % i) for i in range(1, 18)] + \
       [('https://filters.adtidy.org/windows/filters/%d.txt' % i) for i in range(101, 124)] + \
       [('https://filters.adtidy.org/windows/filters/%d.txt' % i) for i in range(200, 253)]
__info__ = "adguard"


def fetch():
    domains = set()
    paths = downloads(__url__, outdir=os.path.join(AD_GFW_HOME, __info__))
    for filepath in paths:
        for line in reader_g(filepath):
            if re.match(r'^\s*(@@|\|\||[a-zA-Z0-9])', line):
                domains |= find_domains(line)
    return domains
