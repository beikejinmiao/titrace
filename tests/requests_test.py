#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from libs.pyaml import configure


proxies = configure['proxies']
print(proxies)

with requests.get('https://codeload.github.com/blackmatrix7/ios_rule_script/zip/refs/heads/master',
                  proxies=proxies) as resp:
    with open('test.zip', 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

