# -*- coding:utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import scrapy
from scrapy.http import Request, FormRequest
from scrapy import log
from urllib import urlencode
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from my_bit_v1.items import MyBitV1Item
import sys
import datetime,calendar
from scrapy import optional_features
from bs4 import BeautifulSoup
optional_features.remove('boto')


insert_time = str(datetime.date.today())


forbid_url = ['thread-10442489-','thread-10480774-','thread-10287865-','thread-10534784-','thread-334630-','thread-10471436-','thread-10556444-','thread-10474940-','thread-10556345-','thread-10548923-','thread-10510780-','thread-10599468-','thread-10498674-','thread-24238-','thread-10526403-','thread-10574471-','thread-10104915-','thread-10076285-','thread-10550120-','thread-466827-','thread-10542992-','thread-10542991-','thread-361469-','thread-4373-','thread-25103-','hread-125421-','thread-125421-','thread-217728-','thread-320656-']
file_name = 'url_file'

#灌水 前程似锦 硬件与s数码 网络技术 软件使用 游戏 体坛  职场
forum_list = [('forum-14',350),('forum-83',175),('forum-80',11),('forum-10',13),('forum-21',4),('forum-22',4),('forum-115',9),('forum-124',17)]
home_url = 'http://out.bitunion.org'



url_list = []
for forum in forum_list:
	forum_id = forum[0]
	forum_length = forum[1]
	for index in range(forum_length):
		url_list.append('http://out.bitunion.org/' + forum_id + '-' + str(index+1) + '.html')
	
def get_thread_url(list_page):
	all_href = list_page.xpath('//a/@href').extract()
	ef_thread_href = []
	for href in all_href:
		flag = 0
		if('thread-' in href):
			for forbid in forbid_url:
				if forbid in href:
					flag = 1
			if flag == 0:
				ef_thread_href.append(href)
	url_dic = {}
	for href in ef_thread_href:
		fields = href.split('-')
		thread_id = home_url + '/' + fields[0] + '-' + fields[1] + '-1-1.html'
		count = int(fields[2])
		if(url_dic.has_key(thread_id)):
			if(count > url_dic[thread_id]):
				url_dic[thread_id] = count
		else:
			url_dic[thread_id] = count
	return url_dic

def get_title(raw_title):
	return raw_title.replace('<div class="t_smallfont">','').replace('<br>','').replace('</div>','')

def get_content(raw_content):
	left_index = 0
	right_index = 1
	content = ''
	for index in xrange(len(raw_content)):
		if(raw_content[index]=='>'):
			raw_content = raw_content[index+1:]

class BitSpider(CrawlSpider):
	name = 'bit-spider'
	allowed_domains = ['out.bitunion.org']
	start_urls = []

	headers = {"Accept": "*/*","Accept-Encoding": "gzip,deflate","Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh;q=0.4","Connection": "keep-alive","Content-Type":" application/x-www-form-urlencoded; charset=gb2312","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36","Referer": "http:/out.bitunion.org"}
	write_count = 0
	crawl_type = 'crawl_url'
	url_dic = {}
	def __init__(self,crawl_type='crawl_url',*args,**kwargs):
		super(BitSpider,self).__init__(*args,**kwargs)
		self.crawl_type = crawl_type
		if(self.crawl_type == 'crawl_url'):
			with open(file_name,'w') as fd:
				fd.write('url' + '\t' + 'count' + '\n')
			self.start_urls = url_list

		elif(self.crawl_type == 'crawl_thread'):
			with open(file_name,'r') as fd:
				for line in fd:
					fields = line.strip().split('\t')
					if(fields[0] == 'url' and fields[1] == 'count'):
						continue
					url = fields[0]
					#level =	int(fields[1])
					#if(level >= self.thres):
					self.start_urls.append(url)
					self.url_dic[url] = level
		else:
			raise ValueError('crawl_type:crawl_url | crawl_thread')	

	def start_requests(self):
		return [Request('http://out.bitunion.org/logging.php?action=login&referer=%2F', meta = {'cookiejar' : 1}, callback = self.post_login)]

	def post_login(self,response):
		#print '###in post###'
		verifyimgid = 'de5bf51b0c91a10a6a8f13750b41bf0a'
		verify = '12485'
		data = {'username':'spider666','password':'sd584520','verify':verify,'verifyimgid':verifyimgid}
		return [FormRequest.from_response(response,meta={'cookiejar':response.meta['cookiejar']},headers=self.headers,formdata=data,callback=self.after_login,dont_filter=True)]

	def after_login(self,response):
		#print response.body
		for url in self.start_urls:
			yield Request(url,meta={'cookiejar':response.meta['cookiejar']},callback=self.parse_page)

	def parse_page(self,response):
		#print 'in parse list page'
		page = Selector(response)
		if(self.crawl_type == 'crawl_url'):
			thread_url_dic = get_thread_url(page)
			with open(file_name,'a') as fd:
				for url in thread_url_dic:
					fd.write(url + '\t' + str(thread_url_dic[url]) + '\n')
			self.write_count += 1
		else:
			item = MyBitV1Item()
			author_list = page.xpath('//legend/font/nobr/b/text()').extract()
			item['author'] = author_list[0]
			#内容和标题在不同div下
			item['url'] = response.url
			div_list = page.xpath('//div').extract()
			raw_title = div_list[1]
			raw_content = div_list[4]
			soup_content = BeautifulSoup(raw_content)
			item['content'] = soup_content.get_text().replace("'",".")
			item['title'] = get_title(raw_title)
			item['insert_time'] = insert_time
			item['reply_number'] = self.url_dic[response.url]
			tr_list = page.xpath('//tr/td/text()').extract()
			for tr in tr_list:
				fields = tr.strip().split(' ')
				if(len(fields)==3 and (fields[-1] == 'PM' or fields[-1] == 'AM') and len(fields[0].split('-'))==3 ):
					item['post_time'] = tr
					break
			yield item
				
