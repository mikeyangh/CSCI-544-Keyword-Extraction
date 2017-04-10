import os
import os.path
import pickle

DATA_DIR = '../../data/'

SEG_DIR = os.path.join(DATA_DIR, 'segmented')
files = os.listdir(SEG_DIR)

TMP_PATH = '/tmp/idf.pkl'

def filt(word):
    for i in range(len(word)):
        if ord(word[i]) > 0x80:
            return True
    return False

class IDF:
    def __init__(self):
        self.N = 0
        self.data = {}

    def put(self, ar):
        self.N += 1
        for word in set(ar):
            if word in self.data:
                self.data[word] += 1
            else:
                self.data[word] = 1

    def save(self):
        with open('/tmp/idf.pkl', 'wb') as f:
            pickle.dump((self.N, self.data), f)

    def load(self):
        with open('/tmp/idf.pkl', 'rb') as f:
            self.N, self.data = pickle.load(f)

idf = IDF()
if os.path.exists('/tmp/idf.pkl'):
    idf.load()
else:
    count = 0
    for fname in files:
        fpath = os.path.join(SEG_DIR, fname)
        with open(fpath) as f:
            s = f.readline()
            words=[s.strip() for s in s.split('/') if filt(s)]
            idf.put(words)
            count += 1
            print(count)
    idf.save()
