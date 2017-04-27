import argparse
import os


def ratio_type(x):
    x = float(x)
    if x < 0 or x > 1:
        raise argparse.ArgumentTypeError('Ratio should be within 0 and 1')
    return x


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--ratio', action='store', dest='ratio', default=0.8, type=ratio_type,
                    help='Store ratio threshold for choosing stop words. Default value: 0.8')

required_group = parser.add_argument_group('required arguments')
required_group.add_argument('-i', '--input', action='store', dest='input_dir',
                            help='Store input raw txt dir', required=True)

results = parser.parse_args()

invert_idx_dict = {}
stop_list = []

count_paper = 0

for filename in os.listdir(results.input_dir):
    if not filename.endswith('.txt'):
        continue
    try:
        fullname = os.path.join(results.input_dir, filename)
        fh = open(fullname, 'r')
        print 'Indexing ' + fullname
        data = fh.read()

        idx = 0
        reach_end = False
        while not reach_end:
            next_idx = data.find('/ ', idx)
            if next_idx < 0:
                word = data[idx:]
                reach_end = True
            else:
                word = data[idx:next_idx]

            if word not in invert_idx_dict:
                invert_idx_dict[word] = set()
            invert_idx_dict[word].add(filename)
            idx = next_idx + 2
        count_paper += 1
    except IOError:  # File not found
        print 'Failed to index ' + fullname

for word, paper_set in invert_idx_dict.items():
    if len(paper_set) > count_paper*results.ratio:
        stop_list.append(word)

with open('paper_stop.txt', 'w') as fh:
    for word in stop_list:
        fh.write(word + '\n')

