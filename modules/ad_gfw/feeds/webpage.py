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
    failed_urls = dict()
    for url in __url__:
        try:
            info = pywget.retrieve(url)
            if not info.success:
                failed_urls[url] = info.desc
        except Exception as e:
            failed_urls[url] = repr(e)
            continue
        for host in find_domains(info.text):
            domains.add(host.lower())
    return domains, failed_urls

