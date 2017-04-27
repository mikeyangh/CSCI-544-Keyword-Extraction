import argparse
import os
import os.path
from subprocess import Popen, PIPE

DATA_DIR = '../../data'

PDF_DIR = os.path.join(DATA_DIR, 'pdf')
TXT_DIR = os.path.join(DATA_DIR, 'txts')

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--txt', help='Directory of TXTs.', required=True)
parser.add_argument('-b', '--tag', help='Directory of Tags.', required=True)
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
    p2 = Popen(['python', 'textrank.py',
        '-a', os.path.join(args.txt, txtname),
        '-b',  os.path.join(args.tag, tagname),
        '-o',  os.path.join(args.out, outname),
        ])
    return (p2, fname)


def process_all(nproc=1, nfiles=N):
    process_count = 0
    complete_count = 0

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
            for p, name in running:
                if p.pid == pid:
                    complete_count += 1
                    print complete_count, '/', N, 'finished', name
                else:
                    new_running.append((p, name))
            running = new_running

process_all(args.n)
