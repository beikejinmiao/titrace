#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://tranco-list.eu/
__url__ = 'https://tranco-list.s3.amazonaws.com/top-1m.csv.zip'
__info__ = 'tranco'


def fetch(outdir=None):
    return crawl(__url__, outdir=__info__ if not outdir else outdir)
