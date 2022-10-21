#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.core import AbstractFeedsManager


class AlexaFeedsManager(AbstractFeedsManager):
    def __init__(self, date=None):
        super().__init__('alexa', date=date)
        self.top100k_sites = list()

    def runner(self):
        results = self.fetch()
        for i in range(1000000):
            for result in results:
                if i >= len(result):
                    continue
                host = result[i]
                domain = self.add_host(host)
                if i < 100000 and domain:
                    self.top100k_sites.append(domain)
        #
        self.save('%s.top100k.%s.txt' % (self.module, self.date), self.top100k_sites)


if __name__ == '__main__':
    man = AlexaFeedsManager(date='19700101')
    man.start()
