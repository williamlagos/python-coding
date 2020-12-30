import sys

if len(sys.argv) < 3:
    sys.exit(1)

program, database, query_word = sys.argv

with open('database.bin', 'rb') as db:
    # Seek for the first sector with the index pointing to the positions on binary file
    index_sector = int(db.read(16).decode('utf-8'))
    db.seek(index_sector)
    indexes_list = db.read().decode('utf-8').split('\n')

    # Remove any invalid tuples to form a valid dictionary / hashmap on python, just with the indexes.
    indexes_tuples = [ tuple(x.split(' ')) for x in indexes_list[:-1] ]
    indexes_tuples_without_spaces = [ x for x in indexes_tuples if len(x) >= 2 ]
    # indexes_tuples_with_spaces = [x for x in indexes_tuples if len(x) < 2]
    # print(indexes_tuples_with_spaces)
    indexes_dict = { k:int(v) for (k,v) in indexes_tuples_without_spaces }

    # With the dict in hands, search for the word and its index, on an O(1) time complexity
    db.seek(indexes_dict[query_word])
    result_list = db.readline().decode('utf-8')[:-1].split(' ')[1:]
    # Print the results found in that line, then close the file
    for result in result_list:
        print(result)
    db.close()