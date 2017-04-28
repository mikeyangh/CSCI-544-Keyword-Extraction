from __future__ import print_function
import argparse
from io import open
import os
import os.path
from subprocess import Popen, PIPE

DATA_DIR = '../../data'

PDF_DIR = os.path.join(DATA_DIR, 'pdf')
TXT_DIR = os.path.join(DATA_DIR, 'txts')

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--txt', help='Directory of TXTs.', required=True)
parser.add_argument('-n', '--n', help='Number of subprocess', type=int, default=4)
parser.add_argument('-o', '--out', help='Directory of outputs', required=True)
args = parser.parse_args()


files = os.listdir(args.txt)

files = list(filter(lambda name: name.endswith('.txt'), files))

N = len(files)

def process_one(fname):
    txtname = fname[:-4] + '.txt'
    tagname = 'tag_' + fname[:-4] + '.txt'
    outname = fname[:-4] + '.txt'
    output_file = open(os.path.join(args.out, outname), 'wt')
    p2 = Popen(['python', 'tfidf.py', '-n', '10', '--vanilla',
        os.path.join(args.txt, txtname)], stdout=output_file)
    return (p2, fname, output_file)


def process_all(nproc=1, nfiles=N):
    process_count = 0
    complete_count = 0

    if not os.path.exists(args.out):
        os.makedirs(args.out)
    running = []
    while True:
        if len(running) < nproc and process_count < nfiles:
            running.append(process_one(files[process_count]))
            process_count += 1
        else:
            if len(running) == 0:
                break
            pid, code = os.waitpid(0, 0)
            new_running = []
            for p, name, output_file in running:
                if p.pid == pid:
                    output_file.close()
                    complete_count += 1
                    print(complete_count, '/', N, 'finished', name)
                else:
                    new_running.append((p, name, output_file))
            running = new_running

process_all(args.n)
