#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.regex import find_domains
from utils.filedir import reader_g
from modules.ad_gfw.base import download_gitzip
from modules.ad_gfw.base import AD_GFW_HOME


__url__ = [
    'https://codeload.github.com/blackmatrix7/ios_rule_script/zip/refs/heads/master',
    'https://codeload.github.com/LM-Firefly/Rules/zip/refs/heads/master',
    'https://codeload.github.com/Hackl0us/SS-Rule-Snippet/zip/refs/heads/main',
    'https://codeload.github.com/ACL4SSR/ACL4SSR/zip/refs/heads/master',
]


def fetch():
    domains = set()
    paths = download_gitzip(__url__, outdir=AD_GFW_HOME)
    for filepath in paths:
        for line in reader_g(filepath):
            domains |= find_domains(line)
    return domains
