import os

import jieba as jb
import sys

import time

blank_chars = '　'
blank_chars_replacement = ' '


def trim_files(raw_file_dir):
    for filename in os.listdir(raw_file_dir):
        if filename.endswith('.txt'):
            with open(raw_file_dir + '/' + filename, 'r') as txt_file:
                with open(raw_file_dir + '/trimmed/' + filename, 'w+') as output_file:
                    print('Trimming file ' + filename)
                    line_list = txt_file.readlines()
                    line_list = [line.strip() for line in line_list]
                    whole_text = str(''.join(line_list))
                    whole_text = whole_text.translate(str.maketrans(blank_chars, blank_chars_replacement))
                    whole_text = whole_text.replace(' ', '')
                    output_file.write(whole_text + "\n")
                    output_file.close()
                    txt_file.close()


def seg_trimmed_files(raw_file_dir):
    jb.load_userdict('/Users/dengyuchi/Development/CSCI-544-Keyword-Extraction/segmentation/dicts/dicts-txt/cs.txt.sorted.txt')
    jb.load_userdict('/Users/dengyuchi/Development/CSCI-544-Keyword-Extraction/segmentation/dicts/dicts-txt/math.txt.sorted.txt')
    for filename in os.listdir(raw_file_dir):
        if filename.endswith('.txt'):
            with open(raw_file_dir + '/' + '/trimmed/' + filename, 'r') as txt_file:
                with open(raw_file_dir + '/segmented/' + filename, 'w+') as output_file:
                    print('Segmenting file ' + filename)
                    whole_text = txt_file.readline()
                    seg_list = jb.cut(whole_text, cut_all=False)
                    output_file.write("/ ".join(seg_list) + "\n")
                    output_file.close()
                    txt_file.close()


if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) == 2:
        raw_file_dir = sys.argv[1]
        trim_files(raw_file_dir)
        seg_trimmed_files(raw_file_dir)
    print("\nRunning time: {0}ms\n".format(int((time.time() - start_time) * 1000)))
