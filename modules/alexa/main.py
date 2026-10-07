#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.core import FeedsManager


class AlexaManager(FeedsManager):
    def __init__(self, date=None):
        super().__init__('alexa', date=date)

    def run(self):
        results = self.fetch()
        for feed, result in results.items():
            for host in result:
                self.add_host(host)

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

