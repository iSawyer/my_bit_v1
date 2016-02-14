import sqlite3
import threading
import multiprocessing
import os
import commands
import sys
class query_DB:

	def __init__(self):
		cmd = 'fuser ../BitUnion-DB1.db'
		rt = commands.getstatusoutput(cmd)
		if(rt[0]!=0):
			raise ValueError('fuser cmd err')
		pid_list = rt[1].strip().split(':')[1].strip().split(' ')
		for pid in pid_list:
			print pid
			if(pid == ''):
				continue
			cmd = 'kill -09 ' + pid
			rt = os.system(cmd)
		self.conn = sqlite3.connect('../BitUnion-DB1.db')
		self.cur = self.conn.cursor()
		
		
	def __del__(self):
		self.cur.close()
		self.conn.close()
		
	def get_one(self):
		query = 'select * from bitdb1'
		self.cur.execute(query)
		all_data = self.cur.fetchall()
		for data in all_data:
			yield data

	def get_max_reply(self,n=10):
		self.cur.execute('select * from bitdb1 order by reply_number desc limit 0,%d' %n)
		all_data = self.cur.fetchall()
		return all_data

	def get_top_word(self,n=200):
		pass
		#cur = self.conn.cursor()
			

	def write_textrank(self,keyword,weight):
		#conn = sqlite3.connect('../BitUnion-DB1.db')
		sql = 'create table if not exists bitdb2(keyword text PRIMARY KEY, weight float)'
		cur2 = self.conn.cursor()
		cur2.execute(sql)
		self.conn.commit()
		cur2.execute("select 1 from bitdb2 where keyword=('%s')" %keyword)
		ret = cur2.fetchone()
		if(ret):
			cur2.execute("select weight from bitdb2 where keyword=('%s')" %keyword)
			weight_old = cur2.fetchone()[0]
			weight += weight_old
			cur2.execute("update bitdb2 set weight=(%f) where keyword=('%s')" %(weight,keyword))
			self.conn.commit()
		else:
			cur2.execute("insert into bitdb2 VALUES('%s',%f)" %(keyword,weight))
			self.conn.commit()
		cur2.close()
