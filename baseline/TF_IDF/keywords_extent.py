# -*- coding: utf-8 -*-
import sys
import codecs
LEN = 5
PROP = .5

def max_search(arr, proportion = PROP):
	rtn = ''
	for pos in range(LEN):
		char_count = {}
		most_char, most_count = None, 0
		for word in arr:
			if word is True or word is False:
				continue
			# print word
			if len(word) <= pos:
				continue
			char = word[pos]
			# print pos, char
			if char not in char_count:
				char_count[char] = 1
			else:
				char_count[char] += 1
				if char_count[char] > most_count:
					most_count = char_count[char]
					most_char = char
		# print most_char, most_count, len(arr)
		if most_count >= proportion * len(arr):
			rtn += most_char
			arr = list(filter(lambda x: len(x) > pos and x[pos] == most_char, arr))
			# print arr
		else:
			return rtn
	return rtn			

def key_extent(article, key, proportion):
	key = unicode(key, 'utf-8')
	try:
		pos = article.find(key)
	except:
		print '_____exception'
		return
	prev_chars, next_chars = [], []
	while pos != -1:
		reversed_prev = ''
		for prev_char_pos in reversed(range(max(0, pos - LEN), pos)):
			reversed_prev += article[prev_char_pos]
		prev_chars.append(reversed_prev)
		next = ''
		next_begin_pos = pos + len(key)
		for next_char_pos in range(next_begin_pos, min(len(article), next_begin_pos + LEN)):
			next += article[next_char_pos]
		next_chars.append(next)
		pos = article.find(key, pos + len(key))
	extented_prev, extented_next = '', ''
	reversed_prev = max_search(prev_chars, proportion)
	if len(reversed_prev) > 0:
		extented_prev = reversed_prev[::-1] + key
	next = max_search(next_chars, proportion)
	if len(next) > 0:
		extented_next = key + next
	return extented_prev, extented_next



