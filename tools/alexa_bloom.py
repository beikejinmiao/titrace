#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import glob
import tldextract
from pybloom_live import BloomFilter
from conf.paths import PRIVATE_RESOURCE_HOME
from utils.filedir import reader_g
from libs.logger import logger


ALEXA_BLOOM_FILTER_1M_PATH = os.path.join(PRIVATE_RESOURCE_HOME, 'top-1m-sites.blm')


def _create(src_file: str | list, blm_file, capacity=1000000):
    bloom = BloomFilter(capacity, 0.001)
    src_files = src_file if isinstance(src_file, list) else [src_file]
    for file in src_files:
        for line in reader_g(file):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            bloom.add(line.lower())
    with open(blm_file, 'wb') as fopen:
        bloom.tofile(fopen)
    logger.info('Total domain count of \'%s\': %d' % (blm_file, len(bloom)))


def create_1m():
    capacity = 3000000
    filepaths = [
        glob.glob(os.path.join(PRIVATE_RESOURCE_HOME, 'ad_gfw', 'ad_gfw.2*'))[-1],
        glob.glob(os.path.join(PRIVATE_RESOURCE_HOME, 'alexa', 'alexa.2*'))[-1],
        glob.glob(os.path.join(PRIVATE_RESOURCE_HOME, 'icp', 'icp.2*'))[-1],
        os.path.join(PRIVATE_RESOURCE_HOME, 'whitelist.txt')
    ]
    _create(filepaths, ALEXA_BLOOM_FILTER_1M_PATH, capacity=capacity)


def check(hosts):
    blooms = {
        'alexa_1m': {
            'blm_file': ALEXA_BLOOM_FILTER_1M_PATH,
            'bloom': None,
        }
    }
    for name in blooms:
        with open(blooms[name]['blm_file'], 'rb') as fopen:
            bloom = BloomFilter.fromfile(fopen)
        blooms[name]['bloom'] = bloom

    for host in hosts:
        host = host.lower()
        reg_domain = tldextract.extract(host).top_domain_under_public_suffix
        if not reg_domain:
            reg_domain = host
        results = dict()
        for name in blooms:
            results[name] = reg_domain in blooms[name]['bloom']
        print(reg_domain.ljust(30) +
              ', \t'.join(['%s: %s' % (name, result) for name, result in results.items()]))


if __name__ == '__main__':
    # create_100k()
    create_1m()

    domains = ['wifi.vivo.com.cn', 'vc-gp-n-105-242-216-26.umts.vodacom.co.za', 'info.lenovo.com.cn',
               'news.sina.com.cn', 'webapi.weather.com.cn', 'www.google.co.jp', 'www.google.com.hk',
               '71.am', 'connectivity.samsung.com.cn', '32.43.204.121.board.fz.fj.dynamic.163data.com.cn',

               'weibo.66.dnssina.com', 'mb.hd.sohu.com.cn', 'maps.google.co.jp', '1234567.com.cn', 'krypt.com',
               'alios.cn', 'www.fliggy.com', 'www.dingtalk.com', 'www.alibabagroup.com', 'www.alimama.com', 'www.xinmin.cn',
               'alitianji.com', 'alitelecom.com', 'baiduyundns.com', 'baidubos.com', 'samsungacr.com',
               'sogoubaidusm.cn', 'tencentbs.cn', 'huaweikyy.site', 'vivokyy.site',
               'rei9jc56oyqux0rcpcquqmm7jc5freirpsquqkope3n3axrjacg8ipolxvbm.codes']
    check(domains)
