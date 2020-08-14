# Simple file for testing regular expressions patterns.

import re

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

words = {}
with open('1.txt', 'r') as f:
    for line in nonblank_lines(f):
        word_pattern = re.compile(r'(?:(?!\d)\w)+')
        for word in word_pattern.findall(line):
            email = '1'
            if word in words:
                words[word].add(email)
            else:
                words[word] = {email}

print(words)