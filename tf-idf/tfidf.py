import argparse
import math

import idf

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()


word_score_pairs = []


with open(args.file) as f:
    tf = {}
    words=[s.strip() for s in f.readline().split('/') if idf.filt(s)]
    for word in words:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    for word in tf:
        idf_value = idf.idf.idf[word]
        word_score_pairs.append((word,tf[word] * idf_value, tf[word], idf_value))

word_score_pairs.sort(key=lambda x: x[1], reverse=True)

for word, score, tf_value, idf_value in word_score_pairs:
    print('"'+word+'"', score, tf_value, idf_value)

