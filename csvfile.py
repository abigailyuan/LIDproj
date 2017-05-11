import csv
import json
import re
import string
from collections import defaultdict as dd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#read data to a dict
trainfile = open('trainfile.json')
train_data = dd(list)
for line in trainfile:
    instance = json.loads(line)
    train_data[instance['lang']].append(instance['text'])
trainfile.close()

#get tokenized text for each text
vectorDict = dd(list)
vectorizer = CountVectorizer(ngram_range=(2,4),token_pattern=r'\b\w+\b',min_df=1)
analyze = vectorizer.build_analyzer()
for lang in train_data.keys():
    for instance in train_data[lang]:
        buffer = []
        for j in analyze(instance):
            if ('@' not in j) and ('#' not in j) and ('http' not in j):
                j = re.sub('[%s]' % re.escape(string.punctuation),'',j) # remove punctuation
                j = re.sub('\d','',j)    # remove numbers
            if (j != '')and(j != ' ')and(j != '  ')and (len(j) > 1):
                buffer.append(j)
        vectorDict[lang].append(buffer)
        break
    break
    print('appended '+lang)
    
#get ngrams for each instance


#get label list for all instance in label[]

