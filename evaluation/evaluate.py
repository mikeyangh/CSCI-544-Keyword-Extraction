# -*- coding: utf-8 -*-
import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('ref', help='Reference keywords')
parser.add_argument('extracted', help='Extracted keywords')
parser.add_argument('-n', '--num', help='Upper limit of n-gram', type=int, default=1)
args = parser.parse_args()

ref_keywords_dict = {}
extracted_keywords_dict = {}

class Averager:
    def __init__(self):
        self.data = []

    def add(self, v):
        if v is not None:
            self.data.append(v)

    def mean(self):
        if len(self.data) == 0:
            return 0
        return float(sum(self.data)) / len(self.data)


def group_words(s):
    regex = []

    # Match a whole word:
    regex += [ur'\w+']

    # Match a single CJK character:
    regex += [ur'[\u4e00-\ufaff]']

    # Match one of anything else, except for spaces:
    regex += [ur'[^\s]']

    regex = "|".join(regex)
    r = re.compile(regex)

    return r.findall(s)

def load_keywords(fileneame, keywords_dict, ngram):
    fh = open(fileneame, 'r')
    for line in fh:
        words = group_words(line.strip().decode('utf-8'))
        for i in range(0, len(words) + 1 - ngram):
            word = tuple(words[i:(i+ngram)])
            if word not in keywords_dict:
                keywords_dict[word] = 1
            else:
                keywords_dict[word] += 1
    fh.close()


def calculate_score(ref_keywords_dict, extracted_keywords_dict):
    ref_word_num = 0
    extracted_word_num = 0
    for _, count in ref_keywords_dict.items():
        ref_word_num += count
    for _, count in extracted_keywords_dict.items():
        extracted_word_num += count

    match_num = 0
    for word, count in extracted_keywords_dict.items():
        if word not in ref_keywords_dict:
            continue
        match_num += min(count, ref_keywords_dict[word])

    if extracted_word_num == 0 or ref_word_num == 0:
        return None, None, None
    precision = match_num/float(extracted_word_num)
    recall = match_num/float(ref_word_num)
    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1


def main():
    ref_keywords_file = args.ref
    extracted_keywords_file = args.extracted
    precisions = Averager()
    recalls = Averager()
    f1s = Averager()
    for ngram in range(1, args.num + 1):
        load_keywords(ref_keywords_file, ref_keywords_dict, ngram)
        load_keywords(extracted_keywords_file, extracted_keywords_dict, ngram)
        precision, recall, f1 = \
                calculate_score(ref_keywords_dict, extracted_keywords_dict)
        precisions.add(precision)
        recalls.add(recall)
        f1s.add(f1)
    print precisions.mean()
    print recalls.mean()
    print f1s.mean()

if __name__ == '__main__':
    main()
