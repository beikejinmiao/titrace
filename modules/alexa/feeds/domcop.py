#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://www.domcop.com/top-10-million-domains
__url__ = 'https://www.domcop.com/files/top/top10milliondomains.csv.zip'
__info__ = 'domcop'


def fetch(outdir=None):
    # 数据样例
    # "Rank","Domain","Open Page Rank"
    # "1","facebook.com","10.00"
    # "2","fonts.googleapis.com","10.00"
    # "3","google.com","10.00"
    # "4","twitter.com","10.00"
    return crawl(__url__, outdir=__info__ if not outdir else outdir, names=None)
