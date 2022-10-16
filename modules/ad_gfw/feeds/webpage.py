#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.regex import find_domains
from libs.web import pywget


__url__ = [
    'https://ppfocus.com/0/te8f690d9.html',
]
__info__ = "webpage"


def fetch():
    domains = set()
    for url in __url__:
        text = pywget.retrieve(url).text
        for host in find_domains(text):
            domains.add(host.lower())
        return domains

