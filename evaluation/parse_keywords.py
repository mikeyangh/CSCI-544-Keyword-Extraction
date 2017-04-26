# -*- coding: utf-8 -*-：
import sys
import os
import os.path

KEYWORD_DIR = os.getcwd() + '/' + 'keywords'
input_dir = ''


def main():

    parse()


def parse():

    if not os.path.isdir(input_dir):
        raise Exception('Direcotry ' + input_dir + 'does not exist.')
    if not os.path.exists(KEYWORD_DIR):
        os.mkdir(KEYWORD_DIR)
    for input_file in os.listdir(input_dir):
        if not input_file.endswith('.txt'):
            continue
        output_file = KEYWORD_DIR + '/' + input_file
        input_file = input_dir + '/' + input_file
        print 'Extracting keywords from ' + input_file
        with open(input_file, 'r') as input_fh:
            with open(output_file, 'w') as output_fh:
                for line in input_fh:
                    if line.startswith('关键词'):
                        try:
                            # cut off '关键词' and space
                            field = line[10:]
                            words = field.split(';')
                            for word in words:
                                word = word.strip()
                                output_fh.write(word + '\n')
                        except IndexError:
                            print 'Failed to extract from ' + input_file
                            os.remove(output_file)
                        break
            output_fh.close()
        input_fh.close()


if __name__ == '__main__':

    assert len(sys.argv) == 2
    input_dir = sys.argv[1]
    main()