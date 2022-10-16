#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import tldextract


ipv4 = re.compile(r"^((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)(\.((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)){3}$")
# http://stackoverflow.com/questions/9238640/how-long-can-a-tld-possibly-be
domain = re.compile(r"^([\w\-]{1,128}\.){1,255}[a-zA-Z]{2,16}$")
url = re.compile(r"^(http[s]?://.*)|(([\w\-]+\.){1,10}[a-zA-Z]{2,16}(?::\d+)?[/?].*)$")

# find regex
domain_find_regex = re.compile(r"(?:\w[\w-]*\.)+[0-9a-zA-Z]+")
url_find_regex = re.compile(r'(?:tcp|http[s]?|[t]?ftp|ssh|git|jdbc|telnet)://'
                            r'[\w\-.]+\w+(?::\d+)?'
                            r'(?:/|\?)[\w./?;&=+#%@$-]*')

plain_text = re.compile(r".*\.(txt|json|md|log|xml|yml|yaml|conf|ini)$", re.I)
doc = re.compile(r".*\.("
                 r"doc|docx|docm|dot|dotx|dotm|rtf|"
                 r"csv|xls|xlsx|xlsm|xlt|xltx|xltm|"
                 r"ppt|pptx|pptm|pot|potx|potm|pps|ppsx|ppsm|"
                 r"wps|wpt|et|ett|dps|dpt|vsd|vsdx|pdf|odt|chm"
                 r")$", re.I)
html = re.compile(r".*\.(html|htm|html5|shtml|shtm|xhtml|mht|mhtml|phtml|asp|aspx|jsp|jspx|php|do)$", re.I)
js_css = re.compile(r".*\.(js|ts|tsx|css)$", re.I)
img = re.compile(r".*\.(jpg|jpeg|jpgv|gif|png|pngc|ico|bmp|svg|pic|tif|tiff|psd|swf)$", re.I)
video = re.compile(r".*\.(mp4|mp3|avi|mkv|flv|3gp|ts|m3u8|wav|mov|wmv|wmx|webm)$", re.I)
executable = re.compile(r".*\.(dll|exe|msi|apk|iso|bin|jar|class|pyc|rpm|deb|whl|dbf)$", re.I)
archive = re.compile(r".*\.(zip|tar|7z|gz|tgz|xz|txz|bz|tbz|bz2|tbz2|rar)$", re.I)

file = re.compile(r".*\.("
                  r"jpg|jpeg|gif|png|ico|bmp|svg|pic|tif|tiff|psd|xcf|cdr|eps|indd|"
                  r"txt|csv|pdf|doc|docx|xls|xlsx|xltx|ppt|pptx|vsd|vsdx|chm|odt|swf|xml|"
                  r"zip|tar|7z|rar|gz|tgz|xz|bz|bz2|exe|apk|msi|iso|bin|"
                  r"mp4|mp3|avi|mkv|flv|3gp|ts|m3u8|wav|mov|wmv|wmx|"
                  r"jar|class|rpm|deb|whl|dbf"
                  r")$", re.I)
gov_edu = re.compile(r"^([0-9a-zA-Z][0-9a-zA-Z\-]{0,62}\.){1,255}(gov|edu)(\.[a-zA-Z]{2})?")
common_dom = re.compile(r".*\.(com|cn|net|org|info|edu|gov|mil|top|biz|int|name|tw|(gov|edu)\.[a-zA-Z]{2})$", re.I)


def is_valid_ip(text):
    if ipv4.match(text):
        return True
    return False


def is_valid_domain(text):
    if domain.match(text) and "." in text[-7:] and tldextract.extract(text).suffix != "":
        return True
    return False


def maybe_url(text):
    if url.match(text) and tldextract.extract(text).suffix != "":
        return True
    return False


def is_gov_edu(text):
    if gov_edu.match(text):
        return True
    return False


def find_domains(text):
    domains = set()
    for item in domain_find_regex.findall(text):
        if tldextract.extract(item).suffix != "":
            domains.add(item)
    return domains


def find_urls(text):
    return list(set(url_find_regex.findall(text)))


ioc_find_regex = re.compile(r'('
                            r'http[s]?://[\w\-.:]+\w+[\w./?&=+#%-]+|'
                            r'(?:[\w\-]+\.){1,16}\w+(?::\d+)?[/?][\w./?&=+#%-]+'
                            r')')


def is_valid_ioc(text):
    return is_valid_ip(text) or is_valid_domain(text) or maybe_url(text)


def find_ioc(text):
    return [ioc for ioc in ioc_find_regex.findall(text) if is_valid_ioc(ioc)]

