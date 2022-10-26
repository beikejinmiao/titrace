#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.regex import find_domains
from utils.filedir import reader_g
from libs.web.downloader import download


__url__ = [
    'https://codeload.github.com/blackmatrix7/ios_rule_script/zip/refs/heads/master',
    'https://codeload.github.com/LM-Firefly/Rules/zip/refs/heads/master',
    'https://codeload.github.com/Hackl0us/SS-Rule-Snippet/zip/refs/heads/main',
    'https://codeload.github.com/ACL4SSR/ACL4SSR/zip/refs/heads/master',
]
__info__ = 'githubzip'


def fetch(outdir=None):
    domains = set()
    failed_urls = dict()
    for url in __url__:
        info = download(url, outdir=__info__ if not outdir else outdir, auto_unzip=True)
        if not info.success:
            failed_urls[url] = info.desc
        for filepath in info.filepath[1]:
            for line in reader_g(filepath):
                domains |= find_domains(line)
    return domains, failed_urls
