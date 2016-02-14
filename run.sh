#########################################################################
# File Name: run.sh
# Author: dongsui
# mail: suidong@baidu.com
# Created Time: 日  2/ 7 00:12:17 2016
#########################################################################
#!/bin/bash
scrapy crawl bit-spider -a crawl_type=crawl_url 
scrapy crawl bit-spider -a crawl_type=crawl_thread thres=$1

