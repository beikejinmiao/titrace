#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.core import FeedsManager


class AlexaManager(FeedsManager):
    def __init__(self, date=None):
        super().__init__('alexa', date=date)
        self.top100k_sites = list()

    def run(self):
        results = self.fetch()
        for i in range(1000000):
            for feed, result in results.items():
                if i >= len(result):
                    continue
                host = result[i]
                domain = self.add_host(host)
                if i < 100000 and domain:
                    self.top100k_sites.append(domain)
        #
        self.save('%s.top100k.%s.txt' % (self.module, self.date), self.top100k_sites)

    def check(self, target):
        if isinstance(target, str):
            target = [target]
        for line_num, line, filepath in self.traverse():
            for tgt in target:
                if tgt in line:
                    print('%s : %d : %s' % (filepath, line_num, line))


if __name__ == '__main__':
    man = AlexaManager()
    man.start()

    # domains = ['jdhhbs.biz', 'ctdtgwag.biz', 'transetarary-emukebogic-underexuciless.biz',
    #            'joinhouse.party', 'iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com']
    # man.check(domains)

