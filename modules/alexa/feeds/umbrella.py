#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://s3-us-west-1.amazonaws.com/umbrella-static/index.html
__url__ = 'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip'
__info__ = 'umbrella'


def fetch(outdir=None):
    return crawl(__url__, outdir=__info__ if not outdir else outdir)



