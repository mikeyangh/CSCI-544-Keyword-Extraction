import os
import sys
import codecs
import re
path = sys.argv[1]
print path
'''
apply rule to get rid of some words
here we get rid of words like 'Page1'
in segmented data set
'''
def not_legal(word):
	if word.startswith('Page'):
		return True
	return False

def tokenize(content):
	str_out = ''

	segmented = content.split('/ ')
	for word in segmented:
		if not_legal(word):
			continue
		str_out += word
		str_out += '/ '


fin = open(path).read().decode('utf-8')
str_out = ''

segmented = fin.split('/ ')
for word in segmented:
	if not_legal(word):
		continue
	str_out += word
	str_out += '/ '

os.remove(path)
fout = file(path,"w") 
fout.write(str_out.encode('utf-8'))
fout.close()
