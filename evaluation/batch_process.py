import argparse
import os
import os.path
from subprocess import Popen, PIPE

DATA_DIR = '../../data'

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--ref', help='Directory of reference keywords.', required=True)
parser.add_argument('-e', '--extracted', help='Directory of extracted keywords.', required=True)
parser.add_argument('-n', '--n', help='Number of subprocess', type=int, default=4)
args = parser.parse_args()


files = os.listdir(args.extracted)

def mean(array):
    return sum(array) / len(array)

precisions = []
recalls = []
f1s = []

N = len(files)

def parse_output(out):
    precision = float(out.readline().strip())
    precisions.append(precision)
    recall = float(out.readline().strip())
    recalls.append(recall)
    f1 = float(out.readline().strip())
    f1s.append(f1)

def process_one(fname):
    p2 = Popen(['python', 'evaluate.py', os.path.join(args.ref, fname), os.path.join(args.extracted, fname)], stdout=PIPE)
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
                    if code == 0:
                        parse_output(p.stdout)
                else:
                    new_running.append((p, name))
            running = new_running

process_all(args.n)

print 'precision', mean(precisions)
print 'recall', mean(recalls)
print 'f1', mean(f1s)
