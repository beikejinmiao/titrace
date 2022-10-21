# maltrace
收集并维护开源黑白名单数据：域名、IP、URL等

## 域名白(灰)名单
### [ad_gfw](https://github.com/beikejinmiao/maltrace/tree/main/modules/ad_gfw/feeds)
主要收集广告拦截软件(AdGuard、Adblock)和代理软件(Crash、ShadowSocks)规则中的域名    


#### feeds列表
 - [adguard](https://adguard.com/en/welcome.html)
 - [easylist](https://easylist.to/)
 - [firebog](https://firebog.net/)
 - [fancyss](https://github.com/hq450/fancyss)      # 科学上网
 - [gfwlist](https://github.com/gfwlist/gfwlist)
 - https://www.github.com/blackmatrix7/ios_rule_script
 - https://www.github.com/LM-Firefly/Rules
 - https://www.github.com/Hackl0us/SS-Rule-Snippet
 - https://www.github.com/ACL4SSR/ACL4SSR

### [alexa](https://github.com/beikejinmiao/maltrace/tree/main/modules/alexa/feeds)
主要收集常见活跃度较高的域名，参考来源
 - http://www.queryadmin.com/1566/download-csv-top-1-million-websites-popularity/
 - https://hackertarget.com/top-million-site-list-download/

#### feeds列表
##### Alexa
下载页面：https://www.alexa.com/ [2022年5月停止服务]   
下载链接：https://s3.amazonaws.com/alexa-static/top-1m.csv.zip
##### Cisco Umbrella
下载页面: https://s3-us-west-1.amazonaws.com/umbrella-static/index.html     
下载链接：https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip
##### Majestic
下载页面：https://majestic.com/reports/majestic-million    
下载链接：https://downloads.majestic.com/majestic_million.csv
##### Statvoo
下载页面：https://statvoo.com/top/ranked    
下载链接：https://statvoo.com/dl/top-1million-sites.csv.zip
##### Tranco
下载页面：https://tranco-list.eu/    
下载链接：https://tranco-list.s3.amazonaws.com/top-1m.csv.zip


### [govcn](https://github.com/beikejinmiao/maltrace/tree/main/modules/govcn/feeds)
从可信网站([四川省政府](https://www.sc.gov.cn/))出发，递归爬取网页中的所有URL并提取域名


