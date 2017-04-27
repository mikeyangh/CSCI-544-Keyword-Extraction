# -*- coding: utf-8 -*-
import argparse

input_file, output_file = '', 'result.txt'
K = 10

stop_dict = set()

word_list = []
word_set = set()

phrase_list = []
phrase_set = set()

word_degree_dict = {}
word_count_dict = {}

word_score_dict = {}
phrase_score_list = []


def parse_commands():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', action='store', dest='output_file', default='./result.txt', type=str,
                        help='Store output file name. Default value: result.txt')
    parser.add_argument('-k', '--keynum', action='store', dest='key_num', default=10, type=int,
                        help='Store output file name. Default value: result.txt')

    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument('-i', '--input', dest='input_file',
                                help='Store input file name', required=True)

    results = parser.parse_args()

    global input_file, output_file, K

    input_file = results.input_file
    output_file = results.output_file
    K = results.key_num


def main():

    parse_commands()
    load_stopwords()
    load_words('/Coding/544/project/txt2/segmented/3000.txt')
    generate_phrase()
    calculate_score()

    fh = open(output_file, 'w')
    num = min(K, len(phrase_score_list))
    for i in range(num):
        fh.write(phrase_score_list[i][0] + '\n')
    fh.close()


def load_stopwords():

    fh = open('../util/stop.txt', 'r')
    for line in fh:
        stop_dict.add(line.strip())
    fh.close()

    fh = open('../util/paper_stop.txt', 'r')
    for line in fh:
        stop_dict.add(line.strip())
    fh.close()


def load_words(filename):

    fh = open(filename, 'r')
    data = fh.read()
    fh.close()

    idx = 0
    reach_end = False
    while not reach_end:
        next_idx = data.find('/ ', idx)
        if next_idx < 0:
            word = data[idx:]
            reach_end = True
        else:
            word = data[idx:next_idx]

        word_set.add(word)
        word_list.append(word)
        idx = next_idx+2


def is_valid_word(word):

    if len(word) < 2:
        return False
    if is_number(word):
        return False
    if contains_alpha(word):
        return False
    if word in stop_dict:
        return False

    return True


def generate_phrase():

    words = []
    for word in word_list:
        if not is_valid_word(word):
            if len(words) > 0:
                phrase_list.append('#'.join(words))
            words = []
        else:
            words.append(word)


def calculate_score():

    for phrase in phrase_list:
        phrase_set.add(phrase)

        phrase = phrase.split('#')
        degree = len(phrase)-1
        for word in phrase:
            if word not in word_degree_dict:
                word_degree_dict[word] = 0
            if word not in word_count_dict:
                word_count_dict[word] = 0
            word_degree_dict[word] += degree
            word_count_dict[word] += 1

    for word in word_set:
        if word not in word_degree_dict:
            continue
        score = word_degree_dict[word] / float(word_count_dict[word])
        word_score_dict[word] = score

    for phrase in phrase_set:
        score = 0
        phrase_arr = phrase.split('#')
        for word in phrase_arr:
            if word not in word_score_dict:
                continue
            score += word_score_dict[word]

        phrase_concat = ''.join(phrase_arr)
        phrase_score_list.append((phrase_concat, score))

    phrase_score_list.sort(key=lambda x: -x[1])


def is_number(word):

    try:
        float(word) if '.' in word else int(word)
        return True
    except ValueError:
        return False


def contains_alpha(word):

    for letter in word:
        if letter.isalpha():
            return True
    return False


if __name__ == '__main__':
    main()
