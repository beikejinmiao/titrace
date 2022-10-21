#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.regex import find_domains
from modules.ad_gfw.base import crawl


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
__info__ = "loyalsoldier"


def fetch(outdir=None):
    return crawl(__url__, outdir=__info__ if not outdir else outdir)



