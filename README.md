# titrace
收集并维护开源黑白名单数据：域名、IP、URL等

## 域名白(灰)名单
### [ad_gfw](https://github.com/beikejinmiao/titrace/tree/main/modules/ad_gfw/feeds)
主要收集广告拦截软件(AdGuard、Adblock)和代理软件(Crash、ShadowSocks)规则中的域名    


#### feeds列表
 - [adguard](https://adguard.com/en/welcome.html)
 - [easylist](https://easylist.to/)
 - [firebog](https://firebog.net/)
 - [fancyss](https://github.com/hq450/fancyss)      　# 科学上网
 - [gfwlist](https://github.com/gfwlist/gfwlist)
 - https://www.github.com/blackmatrix7/ios_rule_script
 - https://www.github.com/LM-Firefly/Rules
 - https://www.github.com/Hackl0us/SS-Rule-Snippet
 - https://www.github.com/ACL4SSR/ACL4SSR

### [alexa](https://github.com/beikejinmiao/titrace/tree/main/modules/alexa/feeds)
主要收集常见活跃度较高的域名，参考来源
 - http://www.queryadmin.com/1566/download-csv-top-1-million-websites-popularity/
 - https://hackertarget.com/top-million-site-list-download/

#### feeds列表
 - [Alexa](https://www.alexa.com/)   
    https://s3.amazonaws.com/alexa-static/top-1m.csv.zip　　[2022年5月停止服务]
 - [Cisco Umbrella](https://s3-us-west-1.amazonaws.com/umbrella-static/index.html)      
    https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip
 - [Majestic](https://majestic.com/reports/majestic-million)    
    https://downloads.majestic.com/majestic_million.csv
 -  [Statvoo](https://statvoo.com/top/ranked)      
    https://statvoo.com/dl/top-1million-sites.csv.zip
 - [Tranco](https://tranco-list.eu/)     
    https://tranco-list.s3.amazonaws.com/top-1m.csv.zip


### [govcn](https://github.com/beikejinmiao/titrace/tree/main/modules/govcn)
以可信网站([四川省政府](https://www.sc.gov.cn/))为起始页
 - 递归爬取网页中的所有URL和对应的title　 　# 限制深度，过滤常见大站域名
 - 提取域名和常见拼音简写 


