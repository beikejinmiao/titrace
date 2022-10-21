#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import crawl

__url__ = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
__info__ = 'alexa'


def fetch(outdir=None):
    return crawl(__url__, outdir=__info__ if not outdir else outdir)


if __name__ == '__main__':
    print(fetch()[:10])
