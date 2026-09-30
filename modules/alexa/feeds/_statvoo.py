#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://statvoo.com/top/ranked
__url__ = 'https://statvoo.com/dl/top-1million-sites.csv.zip'
__info__ = 'statvoo'


def fetch(outdir=None):
    return crawl(__url__, outdir=__info__ if not outdir else outdir)
