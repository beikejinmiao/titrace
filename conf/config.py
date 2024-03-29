#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.pyaml import configure

http_headers = {
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

requests_proxy = None
if configure['proxy']:
    requests_proxy = configure['proxies']

requests_timeout = configure['timeout']
