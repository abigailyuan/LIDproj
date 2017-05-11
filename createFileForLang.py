import json
from collections import defaultdict as dd

def createFile(filename):
    f = open(filename)
    data_dict = dd(list)
    for line in f:
        j_content = json.loads(line)
        data_dict[j_content['lang']].append(j_content['text'])
    f.close()
    for lang in data_dict.keys():
        filename = lang+'.json'
        f = open(filename, 'a')
        for text in data_dict[lang]:
            f.write(text)
        print('finished one file')
        f.close()
    return data_dict

            
