import os
import sys
import codecs
import math
reload(sys)
sys.setdefaultencoding( "utf-8" )
folder_path = sys.argv[1]
output_path = './idf.txt'
file_list = os.listdir(folder_path)
total_num = len(file_list)
idf = {}
for file_name in file_list:
	file_path = folder_path + '/' + file_name
	str_in = open(file_path).read()
	segmented = str_in.split('/ ')
	word_set = set()
	for word in segmented:
		word_set.add(word)
	for word in word_set:
		if word not in idf:
			idf[word] = 0
		idf[word] += 1
# print idf
fout = open(output_path, 'w')
except_count = 0
for k, v in idf.iteritems():
	try:
		if len(k) > 100:
			continue
		fout.write('{0} {1}\n'.format(k, str(math.log(1. + total_num / v))))
		# fout.write('{0} {1}\n'.format(k, v))
	except:
		except_count += 1
		continue
fout.close()
print except_count
