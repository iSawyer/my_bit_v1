# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import twisted.enterprise import adbapi
from twisted.enterprise import adbapi
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import sqlite3
#import MySQLdb
#import MySQLdb.cursors
file_name = 'url_file'

class MySQLStoreBitPipeline(object):
	def __init__(self):
		self.conn = sqlite3.connect('BitUnion-DB1.db')
			
		sql = 'create table if not exists bitdb1(url char[50] PRIMARY KEY, title text, content text,author text,post_time CHAR(20),insert_time CHAR(20),reply_number INT)'
		cur = self.conn.cursor()
		cur.execute(sql)
		self.conn.commit()
		#self.conn = MySQLdb.connect(host='localhost',user='root',passwd='666666',db='BitUnionDB',port=3306)
		print '#######init database done#######'
		cur.close()

	def __del__(self):
		self.conn.close()

	def process_item(self,item,spider): 
		url = item['url'] 
		cur = self.conn.cursor()
			
			#n = cur.execute('select * from bit_db1')	
		sql = 'select 1 from bitdb1 where url=?'
		cur.execute("select 1 from bitdb1 where url=('%s')" % url)
			#self.conn.commit()
			#param = url
			#cur.execute(sql,param)
		ret = cur.fetchone()
		if(ret):
			#cur.execute("update bit_tb_1 set title = %s, content = %s, author = %s, insert_time = %s, reply_number = %s, where url=%s",(item['title'],item['content'],item['author'],item['insert_time'],item['reply_number']))
			cur.execute("update bitdb1 set title='%s',content='%s',author='%s',insert_time='%s',reply_number=%d where url='%s' " %(item['title'],item['content'],item['author'],item['insert_time'],item['reply_number'],url))
			self.conn.commit()
		else:
			cur.execute("insert into bitdb1 VALUES('%s','%s','%s','%s','%s','%s',%d)" %(item['url'],item['title'],item['content'],item['author'],item['post_time'],item['insert_time'],item['reply_number']))
			self.conn.commit()
		cur.close()
	
