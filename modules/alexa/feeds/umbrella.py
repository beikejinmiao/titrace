#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import base_fetch

__url__ = 'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip'
__info__ = 'umbrella'


def fetch():
    return base_fetch(__url__, dirname=__info__)



