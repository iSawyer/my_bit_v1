#-*- coding:UTF-8 -*-
from query_DB import *
import jieba
import jieba.analyse
import sys

stop_words = []
max_reply = 46



def load_stopwords():
	with open('stopwords.txt','rb') as fd:
		for line in fd:
			words = line.strip()
			stop_words.append(words)
	return stop_words


# url title content author post_time insert_time reply_number
def text_rank():
	db = query_DB()
	stop_words = load_stopwords()
	for sample in db.get_one():
		author = sample[3]
		title = sample[1]
		content = sample[2]
		reply_number = sample[-1]
		if(author == 'mikki' or author == u'图说'):
			continue
		if(reply_number >=3):
			title_seg = jieba.analyse.textrank(title,topK=5,withWeight=True,allowPOS=('ns','n','vn','v'))
			for word,weight in title_seg:
				weight *= 0.7 * (float(reply_number) / max_reply)
				db.write_textrank(word,weight)
				
		#content_seg = jieba.analyse.textrank(content,topK=8,withWeight=True,allowPOS=('ns','n','vn','v'))
		#for word,weight in content_seg:
			#weight *= 0.3 * (float(reply_number) / max_reply)
			#db.write_textrank(word,weight)

def top_reply(n=20):
	db = query_DB()
	data_all = db.get_max_reply(n)
	i = 1
	for data in data_all:
		print str(i)+'.'+'\t' +'url:'+ data[0]+'\t'+'title:'+data[1]+'\t'+'author:'+data[3]
		i += 1

def top_author(n=20):
	db = query_DB()
	author_dic = {}
	for sample in db.get_one():
		author = sample[3]
		if(author == 'mikki' or author == u'图说'):
			continue
		if(author_dic.has_key(author)):
			author_dic[author] +=  sample[-1]
		else:
			author_dic[author] = sample[-1]
	author_list = sorted(author_dic.iteritems(),key = lambda asd:asd[1],reverse=True)
	author_list = author_list[0:n]
	i = 1
	for author in author_list:
		print str(i) + '.' + author[0] + ':' + str(author[1])
		i+=1	

if __name__ == '__main__':
	#text_rank()
	#top_reply()
	#top_author(30)
