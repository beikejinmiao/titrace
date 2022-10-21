#!/usr/bin/env python
# -*- coding:utf-8 -*-
from modules.ad_gfw.main import AdGfwFeedsManager
from modules.alexa.main import AlexaFeedsManager
from modules.govcn.main import WebsiteManager


def main():
    for cls in [AdGfwFeedsManager, AlexaFeedsManager, WebsiteManager]:
        man = cls()
        man.start()


if __name__ == '__main__':
    main()
