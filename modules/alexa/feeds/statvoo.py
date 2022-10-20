#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.alexa.base import base_fetch

__url__ = 'https://statvoo.com/dl/top-1million-sites.csv.zip'
__info__ = 'statvoo'


def fetch():
    return base_fetch(__url__, dirname=__info__)
