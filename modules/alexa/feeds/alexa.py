#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import base_fetch

__url__ = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
__info__ = 'alexa'


def fetch():
    return base_fetch(__url__, dirname=__info__)


if __name__ == '__main__':
    print(fetch()[:10])
