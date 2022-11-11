#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

# https://s3-us-west-1.amazonaws.com/umbrella-static/index.html
__url__ = 'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip'
__info__ = 'umbrella'


def fetch(outdir=None):
    # 并未过滤恶意域名,暂时取Top50w
    # umbrella与netlab dga域名碰撞概率比其他源要大得多
    return crawl(__url__, outdir=__info__ if not outdir else outdir, top=500000)



