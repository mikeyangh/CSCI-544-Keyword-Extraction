#coding=utf-8
import os
import sys
import codecs
import operator
import re
import math
from keywords_extent import *
reload(sys)
input_path = sys.argv[1]
origin_article_path = sys.argv[2]
idf_path = './idf.txt'

def invalid(word):
	if word.replace('.','',1).isdigit() or len(word.decode('utf-8')) < 2 or len(word.decode('utf-8')) > 5:
		return True
	if re.match(r'^Page.', word):
		return True
	return False

class KeywordExtractor(object):
	def __init__(self, idf_path):
		idf_file = open(idf_path, 'r')
		self.idf = {}
		print 'init idf data'
		for index, line in enumerate(idf_file.readlines()):
			try:
				tmp_list = line.split(' ')
				self.idf[tmp_list[0]] = float(tmp_list[1])
			except:
				continue

	def get_keywords(self, input_path, topK=20):
		fin = open(input_path).read()
		segmented = fin.split('/ ')
		word_count = {}
		for word in segmented:
			if invalid(word):
				continue
			if word not in word_count:
				word_count[word] = 0
			word_count[word] += 1
		# for word, word_num in word_count.iteritems():
		# 	word_count[word] = math.log(word_count[word])
		for word in word_count:
			count_idf = 1.
			if word in self.idf:
				count_idf = self.idf[word]
			word_count[word] *= count_idf
		sorted_keywords = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
		rtn = []
		for word in sorted_keywords[:topK]:
			rtn.append(word)
		return rtn


def generate_key(idf_path, segmented_input_path, origin_article_path, key_num = 10, extend_rate=0.5):
	ke = KeywordExtractor(idf_path)
	rtn = ke.get_keywords(segmented_input_path, key_num)
	origin_article = open(origin_article_path, 'r').read().decode('utf-8')
	result = []
	for word in rtn:
		# print '{0} {1}'.format(word[0], word[1])
		extended = key_extent(origin_article, word[0], extend_rate)
		if len(extended[0]) > 0:
			result.append(extended[0].encode('utf-8'))
		if len(extended[1]) > 0:
			result.append(extended[1].encode('utf-8'))
		else:
			result.append(word[0]) 

		extended_str = ''
		for char in extended:
			if len(char) > 0:
				extended_str += char.encode('utf-8')
				extended_str += ' '
		if len(char) > 0:	
			print '__extend: ', extended_str

	result = list(set(result))
	return result

res = generate_key(idf_path, input_path, origin_article_path, 10, .5)
for word in res:
	print word


