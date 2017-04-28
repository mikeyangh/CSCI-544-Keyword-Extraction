import argparse

ITERATION_TIME = 200
WINDOW_SIZE = 2
KEY_PHRASE_NUM = 10
FILTER = 0.33
d = 0.85


words_file = '/Coding/544/project/txt2/segmented/3000.txt'
tags_file = '/Coding/544/project/txt2/segmented/tag_3000.txt'
output_file = 'result.txt'

words = []
tags = []

stop_set = set()
filter_set = set()
valid_tag_set = {'n', 'v', 'a', 'eng', 'x'}

text_graph_dict = {}
score_dict = {}

keyword_list = []
keyword_set = set()

keyphrase_list = []


def parse_commands():

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--d', action='store', dest='d', default=0.85, type=float,
                        help='Store value d for textrank. Default value: 0.85')
    parser.add_argument('-t', '--time', action='store', dest='iterate_time', default=200, type=int,
                        help='Store iteration time for textrank. Default value: 200')
    parser.add_argument('-w', '--window', action='store', dest='window', default=2, type=int,
                        help='Store cooccurrence window size for textrank. Default value: 2')
    parser.add_argument('-f', '--filter', action='store', dest='filter', default=0.33, type=float,
                        help='Store the ratio of unfiltered single key word. Default value: 0.33')
    parser.add_argument('-k', '--keynum', action='store', dest='key_num', default=10, type=int,
                        help='Store the number of generated keywords. Default value: 10')
    parser.add_argument('-o', '--output', action='store', dest='output_file', default='./result.txt', type=str,
                        help='Store output file name. Default value: result.txt')

    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument('-a', '--words', dest='words_file',
                                help='Input words file name', required=True)
    required_group.add_argument('-b', '--tags', dest='tags_file',
                                help='Input tags file name', required=True)

    results = parser.parse_args()

    global ITERATION_TIME, WINDOW_SIZE, KEY_PHRASE_NUM, d, words_file, tags_file, output_file
    d = results.d
    ITERATION_TIME = results.iterate_time
    WINDOW_SIZE = results.window
    words_file = results.words_file
    tags_file = results.tags_file
    FILTER = results.filter
    KEY_PHRASE_NUM = results.key_num
    output_file = results.output_file


def load_words(filename):

    fh = open(filename, 'r')
    data = fh.read()
    fh.close()

    idx = 0
    while True:
        next_idx = data.find('/ ', idx)
        if next_idx < 0:
            words.append(data[idx:])
            break
        words.append(data[idx:next_idx])
        idx = next_idx+2


def load_tags(filename):

    fh = open(filename, 'r')
    data = fh.read().split('/')
    for tag in data:
        tags.append(tag)
    fh.close()


def load_stopwords():

    fh = open('../util/stop.txt', 'r')
    for line in fh:
        stop_set.add(line.strip())
    fh.close()

    fh = open('../util/paper_stop.txt', 'r')
    for line in fh:
        stop_set.add(line.strip())
    fh.close()


def load_filter():
    fh = open('../util/filter.txt', 'r')
    for line in fh:
        filter_set.add(line.strip())
    fh.close()


def generate_graph():

    for i in range(len(words)):
        word = words[i]
        # print word + ': ' + tags[i]

        if not is_valid_candidate(word, tags[i]):
            continue

        if word not in text_graph_dict:
            text_graph_dict[word] = {}

        score_dict[word] = 1.0

        end_idx = min(i+WINDOW_SIZE-1, len(words)-1)
        for j in range(i+1, end_idx+1):
            neighbor = words[j]
            if not is_valid_candidate(word=neighbor, tag=tags[j]):
                continue
            if neighbor not in text_graph_dict:
                text_graph_dict[neighbor] = {}

            if neighbor not in text_graph_dict[word]:
                text_graph_dict[word][neighbor] = 1
            else:
                text_graph_dict[word][neighbor] += 1

            if word not in text_graph_dict[neighbor]:
                text_graph_dict[neighbor][word] = 1
            else:
                text_graph_dict[neighbor][word] += 1


def iterate_update():

    for i in range(ITERATION_TIME):
        for word in score_dict:
            update_score(word)


def get_topk_word(k):

    word_list = []
    for word, score in score_dict.items():
        word_list.append((word, score))

    word_list.sort(key=lambda x: -x[1])
    num = min(len(word_list), k)
    for i in range(num):
        keyword_list.append(word_list[i])
        keyword_set.add(word_list[i][0])


def update_score(word):

    tmp_dict = text_graph_dict[word]
    neighbors_val = 0

    for neighbor, weight in tmp_dict.items():
        neighbors_val += score_dict[neighbor]*weight/weight_sum(neighbor)

    score_dict[word] = (1-d)+d*neighbors_val


def weight_sum(word):

    res = 0
    tmp_dict = text_graph_dict[word]
    for neighbor, weight in tmp_dict.items():
        res += weight
    return res


def is_valid_candidate(word, tag='n'):

    if len(word) < 2:
        return False
    if is_number(word):
        return False
    # if contains_alpha(word):
    #     return False
    if word in stop_set:
        return False
    if tag not in valid_tag_set:
        return False
    return True


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


def combine_keyword():

    phrase_count_dict = {}
    keyphrase_score_dict = {}
    idx = 0
    phrase = ''
    score = 0
    count = 0
    while idx < len(words):
        if words[idx] in keyword_set:
            phrase += words[idx]
            score += score_dict[words[idx]]
            count += 1
        else:
            if phrase not in phrase_count_dict:
                phrase_count_dict[phrase] = 1
            else:
                phrase_count_dict[phrase] += 1

            if len(phrase) > 0 and phrase not in keyphrase_score_dict:
                keyphrase_score_dict[phrase] = score/float(count)
                # keyphrase_score_dict[phrase] = score

            phrase = ''
            score = 0
            count = 0
        idx += 1

    for keyphrase in keyphrase_score_dict:
        keyphrase_score_dict[keyphrase] *= phrase_count_dict[keyphrase]

    tmp_list = [(phrase, _score) for phrase, _score in keyphrase_score_dict.items() if phrase not in filter_set]
    tmp_list.sort(key=lambda x: -x[1])
    tmp_list = deduplicate(tmp_list)
    global keyphrase_list
    keyphrase_list = tmp_list[:min(len(tmp_list), KEY_PHRASE_NUM)]


def deduplicate(tmp_list):
    res_list = []
    for i in range(len(tmp_list)):
        if i == 0:
            res_list.append(tmp_list[0])
            continue
        covered = False
        for j in range(i):
            if tmp_list[i][0].find(tmp_list[j][0]) >= 0 or tmp_list[j][0].find(tmp_list[i][0]) >= 0:
                covered = True
                break
        if not covered:
            res_list.append(tmp_list[i])

    return res_list


def main():

    parse_commands()
    load_words(filename=words_file)
    load_tags(filename=tags_file)
    assert len(words) == len(tags)
    load_stopwords()
    load_filter()

    generate_graph()

    iterate_update()
    remain_num = int(round(len(score_dict)*FILTER))
    get_topk_word(remain_num)
    combine_keyword()

    # for (word, score) in keyword_list:
    #     print word + ' ' + str(score)

    fh = open(output_file, 'w')
    for (word, score) in keyphrase_list:
        # fh.write(word + ' ' + str(score) + '\n')
        fh.write(word + '\n')
    fh.close()


if __name__ == '__main__':

    main()
