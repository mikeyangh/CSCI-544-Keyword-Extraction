# -*- coding: utf-8 -*-
import os
import sys
import codecs
import operator
import re
reload(sys)
sys.setdefaultencoding( "utf-8" )
input_path = sys.argv[1]
idf_path = './idf.txt'

def invalid(word):
	if word.replace('.','',1).isdigit() or len(word.decode('utf-8')) < 2 or len(word.decode('utf-8')) > 5:
		return True
	if re.match(r'^Page.', word):
		return True
	return False

class KeywordExtractor(object):
	def __init__(self):
		idf_file = open(idf_path, 'r')
		self.idf = {}
		print 'init idf data'
		for index, line in enumerate(idf_file.readlines()):
			try:
				tmp_list = line.split(u' ')
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
		for word in word_count:
			count_idf = 0.
			if word.decode('utf-8') in self.idf:
				count_idf = self.idf[word.decode('utf-8')]
			word_count[word] *= count_idf
		sorted_keywords = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
		rtn = []
		for word in sorted_keywords[:topK]:
			rtn.append(word)
		return rtn

ke = KeywordExtractor()
rtn = ke.get_keywords(input_path, 50)
for word in rtn:
	print '{0} {1}'.format(word[0], word[1])

