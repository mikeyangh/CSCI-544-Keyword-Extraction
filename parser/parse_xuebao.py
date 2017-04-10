import argparse
import os
import os.path
from subprocess import Popen, PIPE

DATA_DIR = '../../data'

PDF_DIR = os.path.join(DATA_DIR, 'pdf')
TXT_DIR = os.path.join(DATA_DIR, 'txts')

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pdf', help='Directory of PDFs.', default=PDF_DIR)
parser.add_argument('-t', '--txt', help='Directory of TXTs.', default=TXT_DIR)
parser.add_argument('-n', '--n', help='Number of subprocess', type=int, default=4)
parser.add_argument('-l', '--limit', help='Number of files to convert', type=int, default=10)
args = parser.parse_args()


files = os.listdir(PDF_DIR)

files = list(filter(lambda name: name[-4:] == '.pdf', files))

N = len(files)

def convert(fname):
    txtname = fname[:-4] + '.txt'
    txtf = open(os.path.join(args.txt, txtname), 'w')
    p1 = Popen(['pdf2txt.py', os.path.join(args.pdf, fname)], stdout=PIPE)
    p2 = Popen(['python', 'post_processing.py'], stdin=p1.stdout, stdout=txtf)
    p1.stdout.close()
    return (p2, txtf, fname)


def process_all(nproc=1, nfiles=N):
    process_count = 0
    complete_count = 0

    running = []
    while True:
        if len(running) < nproc and process_count < nfiles:
            running.append(convert(files[process_count]))
            process_count += 1
        else:
            if len(running) == 0:
                break
            pid, code = os.waitpid(0, 0)
            new_running = []
            for p, f, name in running:
                if p.pid == pid:
                    complete_count += 1
                    print complete_count, '/', N, 'finished', name
                    f.close()
                else:
                    new_running.append((p, f, name))
            running = new_running

if args.limit == 0:
    process_all(args.n)
else:
    process_all(args.n, args.limit)
