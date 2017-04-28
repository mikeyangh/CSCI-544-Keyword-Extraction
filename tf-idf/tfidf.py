#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import codecs
from collections import Counter
from io import open
import math
import numpy as np
import os
import sys

import idf


if __name__ == '__main__':
    utf_writer = codecs.getwriter('utf8')
    if sys.version_info.major < 3:
        sys.stdout = utf_writer(sys.stdout)

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-t', '--type')
parser.add_argument('-n', '--num', type=int, default=15)
parser.add_argument('-d', '--deduplicate', action='store_true')
args = parser.parse_args()

basename = os.path.basename(args.file)
rootdir = os.path.dirname(os.path.dirname(args.file))

trimmed_file = os.path.join(rootdir, 'trimmed', basename)

def load_stop_words(filename):
    s = set()
    with open(filename, 'rt') as f:
        for line in f:
            s.add(line.strip())
    return s

#STOP_WORDS = set(['的', '的', '了', '和', '在', '对', '提出', '中' ,
    #'是' , '与' , '并' , '基于', '为' , '上' , '将' , '等' , '其' , '下' , '不'])
STOP_WORDS = load_stop_words('../util/stop.txt')

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
    word_score_pairs.sort(key=lambda x: x[1], reverse=True)

def partial_frequency():
    word_score_pairs = []
    with open(args.file, 'rt') as f, open(trimmed_file, 'rt') as tf:
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
    word_score_pairs.sort(key=lambda x: x[1], reverse=True)
    return word_score_pairs

def deduplicate(word_list):
    word_list.sort(key=lambda x:len(''.join(x)), reverse=True)
    word_coverage_count_map = {}
    for word in word_list:
        w = ''.join(word)
        if w in word_coverage_count_map:
            continue
        count = 0
        for key, value in word_coverage_count_map.items():
            if key.find(w) == -1:
                continue
            count += 1
        word_coverage_count_map[w] = (len(word), count)
            
    trusted_word_list = []
    for key in word_coverage_count_map:
        l, count = word_coverage_count_map[key]
        if l == 2 and count >= 2:
            trusted_word_list.append(key)

    new_word_list = []
    for key in word_coverage_count_map:
        l, count = word_coverage_count_map[key]
        if count >= 1:
            continue

        collide = False
        for word in trusted_word_list:
            if key.find(word) != -1:
                collide = True
                break
        if not collide:
            new_word_list.append(key)
    #print(word_coverage_count_map)
    return trusted_word_list + new_word_list

def list_all(word_score_pairs):
    for word, score, tf_value, idf_value in word_score_pairs:
        print('"'+'_'.join(word)+'"', score, tf_value, idf_value)

def list_top(word_score_pairs):
    word_list = list(map(lambda x: x[0], word_score_pairs[:args.num]))
    if args.deduplicate:
        word_list = deduplicate(word_list)
    else:
        word_list = list(map(lambda x: ''.join(x), word_list))

    for word in word_list:
        print(word)

if __name__ == '__main__':
    word_score_pairs = partial_frequency()
    if args.type and args.type == 'all':
        list_all(word_score_pairs)
    else:
        list_top(word_score_pairs)
