#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.core import AbstractFeedsManager


class AlexaFeedsManager(AbstractFeedsManager):
    def __init__(self, date=None):
        super().__init__('alexa', date=date)
        self.top100k_sites = list()

    def runner(self):
        results = self.crawl()
        for i in range(1000000):
            for feed, result in results.items():
                if i >= len(result):
                    continue
                host = result[i]
                domain = self.append(host)
                if i < 100000 and domain:
                    self.top100k_sites.append(domain)
        #
        self.save('%s.top100k.%s.txt' % (self.module, self.date), self.top100k_sites)

    def check(self, target):
        for line, filepath in self.traverse():
            if target in line:
                print('"%s" in "%s"' % (target, filepath))


if __name__ == '__main__':
    man = AlexaFeedsManager(date='19700101')
    man.start()
    # man.check('crowleychryslerjeepdodge.com')

