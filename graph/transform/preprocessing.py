import os, sys, re

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

if len(sys.argv) < 3:
    sys.exit(1)

program, dataset_path, generated_db_path = sys.argv
files = os.listdir(dataset_path)
# files = ['1.txt','2.txt']

words = {}
# Reads file by file, then put occurrences on a hash/dict structure.
for name in files:
    if name.endswith('.txt'):
        with open(name, 'r') as f:
            for line in nonblank_lines(f):
                # word_pattern = re.compile(r'\b\w+\b')
                word_pattern = re.compile(r'(?:(?!\d)\w)+')
                for word in word_pattern.findall(line):
                    email = name.split('.')[0]
                    if word in words:
                        words[word].add(email)
                    else:
                        words[word] = {email}
        f.close()

b_indexes = []
b_relations = []
relation_index = 16
# Prepare words and its occurrences to be serialized on a list
for word, occurrences in words.items():
    s_index = '%s %d\n' % (word, relation_index)
    s_relation = '%s %s\n' % (word, ' '.join(occurrences))
    s_relation_size = len(s_relation)
    # s_relation_len_size = len(str(s_relation_size))
    relation_bytesize = s_relation_size # + s_relation_len_size
    b_relation = s_relation.encode('utf-8')
    b_index = s_index.encode('utf-8')
    b_relations.append(b_relation)
    b_indexes.append(b_index)
    relation_index += relation_bytesize

# Write the indexes and the occurrences on a binary file
with open(generated_db_path, 'wb') as db:
    db.write(b'%16d' % (relation_index + 8))
    for b_relation in b_relations:
        db.write(b_relation)
    db.write(b'-------\n')
    for b_index in b_indexes:
        db.write(b_index)
    db.close()