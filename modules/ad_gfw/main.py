#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.core import AbstractFeedsManager


class AdGfwFeedsManager(AbstractFeedsManager):
    def __init__(self, date=None):
        super().__init__('ad_gfw', date=date)
        self.failed_urls = dict()

    def runner(self):
        results = self.fetch()
        for feed, result in results.items():
            _hosts_, _failed_urls_ = result
            for host in _hosts_:
                self.add_host(host)
            self.failed_urls.update(_failed_urls_)
        #
        self.save('%s.failed_urls.%s.json' % (self.module, self.date), self.failed_urls)

    def check(self, target):
        for line, filepath in self.traverse():
            if target in line:
                print('"%s" in "%s"' % (target, filepath))


if __name__ == '__main__':
    man = AdGfwFeedsManager(date='19700101')
    man.start()

