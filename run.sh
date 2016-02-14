#!/bin/bash
scrapy crawl bit-spider -a crawl_type=crawl_url 
scrapy crawl bit-spider -a crawl_type=crawl_thread

