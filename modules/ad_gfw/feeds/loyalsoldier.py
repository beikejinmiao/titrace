#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from libs.regex import find_domains
from utils.filedir import reader_g
from modules.ad_gfw.base import downloads
from modules.ad_gfw.base import AD_GFW_HOME


__url__ = [
    'https://raw.githubusercontent.com/Loyalsoldier/cn-blocked-domain/release/domains.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/direct.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/proxy.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/reject.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/apple.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/icloud.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/google.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/gfw.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/greatfire.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/proxy.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/reject.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/apple.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/icloud.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/google.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/gfw.txt',
    'https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/greatfire.txt',
]
__name__ = "Loyalsoldier"


def fetch():
    paths = downloads(__url__, outdir=os.path.join(AD_GFW_HOME, __name__))
    domains = set()
    for filepath in paths:
        for line in reader_g(filepath):
            domains |= find_domains(line)
    return domains

