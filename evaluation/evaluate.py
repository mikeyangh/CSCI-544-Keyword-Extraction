# -*- coding: utf-8 -*-
import re
import sys

ref_keywords_dict = {}
extracted_keywords_dict = {}


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


def load_keywords(fileneame, keywords_dict):
    fh = open(fileneame, 'r')
    for line in fh:
        words = group_words(line.strip().decode('utf-8'))
        for word in words:
            if word not in keywords_dict:
                keywords_dict[word] = 1
            else:
                keywords_dict[word] += 1
    fh.close()


def calculate_score():
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

    precision = match_num/float(extracted_word_num)
    recall = match_num/float(ref_word_num)

    return 2 * precision * recall / (precision + recall)


def main():
    ref_keywords_file = sys.argv[1]
    extracted_keywords_file = sys.argv[2]
    load_keywords(ref_keywords_file, ref_keywords_dict)
    load_keywords(extracted_keywords_file, extracted_keywords_dict)
    print calculate_score()

if __name__ == '__main__':
    assert len(sys.argv) == 3
    main()
