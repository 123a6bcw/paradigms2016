import hashlib
import os
import sys
import collections

from sys import argv
from os import walk
from os.path import join


def gethash(path):
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        line = f.read(1024)
        while (line):
            sha1.update(line)
            line = f.read(1024)
    return sha1.hexdigest()


def find_duplicates(path):
    files = []
    for directory, b, files_list in os.walk(path):
        for f in files_list:
            files.append((directory, f))

    d = collections.defaultdict(list)
    for d1, f1 in files:
        sha1 = gethash(os.path.join(d1, f1))
        d[sha1].append(f1)

    for ans in d:
        if len(d[ans]) > 1:
            print(':'.join(d[ans]))


if __name__ == "__main__":
    find_duplicates(sys.argv[1])
