#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.regex import find_domains
from modules.ad_gfw.base import batch_fetch


# https://firebog.net/
__url__ = [
    'https://v.firebog.net/hosts/AdguardDNS.txt',
    'https://v.firebog.net/hosts/Admiral.txt',
    'https://v.firebog.net/hosts/Easyprivacy.txt',
    'https://v.firebog.net/hosts/Prigent-Ads.txt',
    'https://v.firebog.net/hosts/Easylist.txt',

    'https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt',
    'https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt',

    'https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts',
    'https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts',
    'https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/android-tracking.txt',
    'https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt',
    'https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/AmazonFireTV.txt',

    'https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt',
    'https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts',
    'https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts',
    'https://adaway.org/hosts.txt',
    'https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt',
    'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
    'https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt',
    # 'https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-blocklist.txt',
]
__info__ = "firebog"


def extract(text):
    return find_domains(text)


def fetch():
    return batch_fetch(__url__, dirname=__info__, extfunc=extract)

