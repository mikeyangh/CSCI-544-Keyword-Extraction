# -*- coding: utf-8 -*-
import os
import os.path

import jieba as jb
import jieba.posseg as pseg
import sys

import time

blank_chars = '　'
blank_chars_replacement = ' '

SEGMENTATION_DIR = os.path.dirname(__file__)

USE_CUSTOM_DICT = True


def trim_files(raw_file_dir, dst_dir):
    if not os.path.exists(os.path.join(dst_dir, 'trimmed')):
        os.makedirs(os.path.join(dst_dir, 'trimmed'))
    for filename in os.listdir(raw_file_dir):
        if filename.endswith('.txt'):
            with open(raw_file_dir + '/' + filename, 'r') as txt_file:
                with open(dst_dir + '/trimmed/' + filename, 'w') as output_file:
                    print('Trimming file ' + filename)
                    line_list = txt_file.readlines()
                    keywords_line = None
                    for line in line_list:
                        if line.startswith(u'\u5173\u952e\u8bcd'):
                            keywords_line = line
                            break

                    line_list = [line.strip() for line in line_list if line != keywords_line]
                    whole_text = str(''.join(line_list))
                    whole_text = whole_text.translate(str.maketrans(blank_chars, blank_chars_replacement))
                    whole_text = whole_text.replace(' ', '')
                    output_file.write(whole_text + "\n")
                    if keywords_line:
                        output_file.write(keywords_line)
                    output_file.close()
                    txt_file.close()


def seg_trimmed_files(raw_file_dir, dst_dir):
    if not os.path.exists(os.path.join(dst_dir, 'segmented')):
        os.mkdir(os.path.join(dst_dir, 'segmented'))
    if not os.path.exists(os.path.join(dst_dir, 'tags')):
        os.mkdir(os.path.join(dst_dir, 'tags'))
    if USE_CUSTOM_DICT:
        jb.load_userdict(os.path.join(SEGMENTATION_DIR, 'dicts/dicts-txt/cs.txt.sorted.txt'))
        jb.load_userdict(os.path.join(SEGMENTATION_DIR, 'dicts/dicts-txt/math.txt.sorted.txt'))
    for filename in os.listdir(raw_file_dir):
        if filename.endswith('.txt'):
            with open(dst_dir + '/' + '/trimmed/' + filename, 'r') as txt_file:
                with open(dst_dir + '/segmented/' + filename, 'w') as output_file:
                    with open(dst_dir + '/tags/tag_' + filename, 'w') as tag_file:
                        print('Segmenting file ' + filename)
                        whole_text = txt_file.readline()
                        # seg_list = jb.cut(whole_text, cut_all=False)
                        pair_list = pseg.cut(whole_text)
                        word_list = []
                        tag_list = []
                        for pair in pair_list:
                            word_list.append(pair.word)
                            tag_list.append(pair.flag)
                        # word_list = [pair.word for pair in pair_list]
                        # tag_list = [pair.flag for pair in pair_list]
                        output_file.write("/ ".join(word_list) + "\n")
                        output_file.write(txt_file.readline())
                        output_file.close()
                        tag_file.write('/'.join(tag_list) + '\n')
                        tag_file.close()
                        txt_file.close()


if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) == 3:
        raw_file_dir = sys.argv[1]
        dst_dir = sys.argv[2]
        #trim_files(raw_file_dir, dst_dir)
        seg_trimmed_files(raw_file_dir, dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
    else:
        print('seg.py src dst')
    print("\nRunning time: {0}ms\n".format(int((time.time() - start_time) * 1000)))
