import argparse
from collections import Counter
import math
import numpy as np
import sys
import os

import idf

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-t', '--type')
parser.add_argument('-n', '--num', default=10)
args = parser.parse_args()

basename = os.path.basename(args.file)
rootdir = os.path.dirname(os.path.dirname(args.file))

trimmed_file = os.path.join(rootdir, 'trimmed', basename)

STOP_WORDS = set(['的', '的', '了', '和', '在', '对', '提出', '中' ,
    '是' , '与' , '并' , '基于', '为' , '上' , '将' , '等' , '其' , '下' , '不'])

word_score_pairs = []

def cap(x, v):
    if x > v:
        return v
    return x

def tf_smooth(x):
    if x > 60:
        return 60 - 60**3 / 8000
    return x - x**3 / 8000

def absolute_frequency():
    with open(args.file) as f, open(trimmed_file) as tf:
        whole_text = tf.readline()
        tf = Counter()
        words=[s.strip() for s in f.readline().split('/') if idf.filt(s)]
        n = len(words)
        for word in words:
            tf[(word,)] = whole_text.count(word)
        for phrase in zip(words[0:(n-2)], words[1:]):
            tf[phrase] = whole_text.count(''.join(phrase))
    
        for phrase in tf:
            idf_value = sum([idf.idf.idf[word] for word in phrase])
            prod = np.product([idf.idf.idf[word] for word in phrase])
            
            if len(phrase) > 1:
                idf_value += prod
            word_score_pairs.append((phrase,tf_smooth(tf[phrase]) * cap(idf_value, 20), tf[phrase], idf_value))

def partial_frequency():
    with open(args.file) as f, open(trimmed_file) as tf:
        whole_text = tf.readline()
        tf = Counter()
        words=[s.strip() for s in f.readline().split('/')]
        n = len(words)
        for word in words:
            if idf.filt(word):
                tf[(word,)] += 1
        for phrase in zip(words[0:(n-2)], words[1:]):
            w1, w2 = phrase
            if idf.filt(w1) and idf.filt(w2) and w1 not in STOP_WORDS and w2 not in STOP_WORDS:
                tf[phrase] += 1
        for phrase in zip(words[0:(n-3)], words[1:(n-2)], words[2:]):
            w1, w2, w3 = phrase
            if idf.filt(w1) and idf.filt(w2) and idf.filt(w3) and w1 not in STOP_WORDS and w3 not in STOP_WORDS:
                tf[phrase] += 1
    
        for phrase in tf:
            idf_value = sum([idf.idf.idf[word] for word in phrase])
            words = list(phrase)
            for i in range(len(phrase)-1):
                idf_value += idf.idf.idf[words[i]] * idf.idf.idf[words[i+1]]

            word_score_pairs.append((phrase,tf_smooth(tf[phrase]) * cap(idf_value, 20), tf[phrase], idf_value))

partial_frequency()

word_score_pairs.sort(key=lambda x: x[1], reverse=True)

def list_all(word_score_pairs):
    for word, score, tf_value, idf_value in word_score_pairs:
        print('"'+'_'.join(word)+'"', score, tf_value, idf_value)

def list_top(word_score_pairs):
    for word, _, _, _ in word_score_pairs[:args.num]:
        print(''.join(word))

if args.type and args.type == 'all':
    list_all(word_score_pairs)
else:
    list_top(word_score_pairs)
