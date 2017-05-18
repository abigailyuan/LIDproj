import json
from collections import defaultdict as dd


data = dd(int)

fp = open('devfile.json')
print('read......')
for line in fp:
    instance = json.loads(line)
    data[instance['lang']] += 1;

fp2 = open('stat.txt', 'a')
print('write.....')
for lang in data.keys():
    print(lang+' '+str(data[lang]))   
