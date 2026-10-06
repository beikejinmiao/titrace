#!/usr/bin/env python
# -*- coding:utf-8 -*-
from multiprocessing import Process
from modules.ad_gfw.main import AdGfwManager
from modules.alexa.main import AlexaManager
from modules.icp.main import ICPManager
from modules.govcn.main import WebsiteManager


def main():
    processes = list()
    # for cls in [AdGfwManager, AlexaManager, ICPManager, WebsiteManager]:
    for cls in [AdGfwManager, AlexaManager, ICPManager]:
        man = cls()
        processes.append(Process(target=man.start))
    for pro in processes:
        pro.start()
    for pro in processes:
        pro.join()


if __name__ == '__main__':
    main()
