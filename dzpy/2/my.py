import hashlib
import os
import sys

from sys import argv
from os import walk
from os.path import join

files = []
for directory, b, files_list in os.walk(sys.argv[1]):
    for f in files_list:
        files.append((directory, f))

used = [0 for i in range(len(files))]
answer = []
i = 0
for d1, f1 in files:
    if used[i] == 0:
        new = []
        j = 0
        for d2, f2 in files:
            if used[j] == 0:
                sha1 = hashlib.sha1()
                sha2 = hashlib.sha1()
                file1 = open(os.path.join(d1, f1))
                file2 = open(os.path.join(d2, f2))
                line1 = 'a'
                line2 = 'b'
                same = 1

                while line1 and line2:
                    line1 = file1.read(1024)
                    line2 = file2.read(1024)
                    sha1.update(line1.encode("utf-8"))
                    sha2.update(line2.encode("utf-8"))
                    if sha1.hexdigest() != sha2.hexdigest():
                        same = 0

                if (file1.read() or file2.read()):
                    same = 0

                if same:
                    new.append(os.path.join(d2, f2))
                    used[j] = 1

                file1.close()
                file2.close()
            j += 1
        answer.append(new)
    i += 1

for ans in answer:
    if len(ans) > 1:
        print(':'.join(ans))
