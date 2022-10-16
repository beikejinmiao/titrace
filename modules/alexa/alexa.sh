#!/bin/bash
######################################################################################
#File Name      : alexa.sh
#Author         : mozi
#Mail           : beikejinmiao@gmail.com
#Created Time   : 2022-06-21 17:43:33
#Description    : http://www.queryadmin.com/1566/download-csv-top-1-million-websites-popularity/
######################################################################################

alexa_home=/root/resources/whitelist/alexa
mkdir -p ${alexa_home}
# make directory by datetime
datename=$(date +%Y%m%d)
download_dir=/tmp/whitelist/domain
work_home=${download_dir}/${datename}
mkdir -p ${work_home}; cd ${work_home}

# download latest file
## alexa
wget -c -t 5 -T 10 --no-check-certificate http://s3.amazonaws.com/alexa-static/top-1m.csv.zip
unzip top-1m.csv.zip
if [ $? == 0 ]; then
    mv top-1m.csv alexa-top-1m.csv
    cp alexa-top-1m.csv ${alexa_home}/
fi
rm -f top-1m.csv.zip

## majestic
wget -c -t 5 -T 10 --no-check-certificate http://downloads.majestic.com/majestic_million.csv
if [ $? == 0 ]; then
    mv majestic_million.csv majestic-top-1m.csv
    cp majestic-top-1m.csv ${alexa_home}/
fi

## cisco umbrella
wget -c -t 5 -T 10 --no-check-certificate http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip
unzip top-1m.csv.zip
if [ $? == 0 ]; then
    mv top-1m.csv cisco-top-1m.csv
    cp cisco-top-1m.csv ${alexa_home}/
fi
rm -f top-1m.csv.zip

## statvoo
wget -c -t 5 -T 10 --no-check-certificate https://statvoo.com/dl/top-1million-sites.csv.zip
unzip top-1million-sites.csv.zip
if [ $? == 0 ]; then
    mv top-1m.csv statvoo-top-1m.csv
    cp statvoo-top-1m.csv ${alexa_home}/
fi
rm -f top-1million-sites.csv.zip


# clean expired folder
date_dirs=(`find ${download_dir} -name "20*" -type d | sort -n`)
cur_len=${#date_dirs[@]}
if [ $cur_len -gt 7 ]; then
    del_num=`expr $cur_len - 7`
    let del_num-=1
    for i in $(seq 0 $del_num)
    do
        rm -rf ${date_dirs[$i]}
        echo "remove expired folder: '${date_dirs[$i]}'"
    done
fi

