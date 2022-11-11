#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://tranco-list.eu/
__url__ = 'https://tranco-list.s3.amazonaws.com/top-1m.csv.zip'
__info__ = 'tranco'


def fetch(outdir=None):
    # 并未过滤恶意域名,暂时取Top50w
    return crawl(__url__, outdir=__info__ if not outdir else outdir, top=500000)
