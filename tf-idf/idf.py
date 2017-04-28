from __future__ import print_function
import codecs
from io import open
import math
import operator
import os
import os.path
import pickle
import sys

if __name__ == '__main__':
    utf_writer = codecs.getwriter('utf8')
    if sys.version_info.major < 3:
        sys.stdout = utf_writer(sys.stdout)

DATA_DIR = '../../data/txt3_raw_seg'

SEG_DIR = os.path.join(DATA_DIR, 'segmented')
files = os.listdir(SEG_DIR)

TMP_PATH = '/tmp/idf.txt'

def filt(word):
    #return len(word.strip()) != 0
    for i in range(len(word)):
        if ord(word[i]) > 0x80:
            return True
    return False

class IDF:
    def __init__(self):
        self.N = 0
        self.data = {}
        self.idf = {}

    def put(self, ar):
        self.N += 1
        for word in set(ar):
            if word in self.data:
                self.data[word] += 1
            else:
                self.data[word] = 1

    def run(self):
        for word in self.data:
            self.idf[word] = math.log(1.*self.N/(1+self.data[word]))


    def save(self):
        with open(TMP_PATH, 'w') as f:
            data = []
            for word in self.data:
                data.append((word, self.idf[word]))
            data.sort(key=operator.itemgetter(1))
            for word, idf, in data:
                f.write(u'{} {}\n'.format(word, idf))

    def load(self):
        with open(TMP_PATH) as f:
            for line in f:
                parts = line.strip().split(' ')
                self.idf[parts[0]] = float(parts[1])

idf = IDF()
if os.path.exists(TMP_PATH):
    idf.load()
else:
    count = 0
    for fname in files:
        fpath = os.path.join(SEG_DIR, fname)
        with open(fpath) as f:
            s = f.readline()
            words=[s.strip() for s in s.split('/') if filt(s)]
            idf.put(words)
            count += 1
            print(count)
    idf.run()
    idf.save()
