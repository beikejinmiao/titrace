#!/usr/bin/env python
# -*- coding:utf-8 -*-
from multiprocessing import Process
from modules.ad_gfw.main import AdGfwFeedsManager
from modules.alexa.main import AlexaFeedsManager
from modules.govcn.main import WebsiteManager


def main():
    processes = list()
    for cls in [AdGfwFeedsManager, AlexaFeedsManager, WebsiteManager]:
        man = cls()
        processes.append(Process(target=man.start))
    for pro in processes:
        pro.start()
    for pro in processes:
        pro.join()


if __name__ == '__main__':
    main()
