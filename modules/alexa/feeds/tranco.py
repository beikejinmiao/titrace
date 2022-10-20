#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import base_fetch

# https://tranco-list.eu/
__url__ = 'https://tranco-list.s3.amazonaws.com/top-1m.csv.zip'
__info__ = 'tranco'


def fetch():
    return base_fetch(__url__, dirname=__info__)
