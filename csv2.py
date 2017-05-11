import csv
import json
import re
import string
from collections import defaultdict as dd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

corpus = []
Y = []

fp = open('trainfile.json')
for line in fp:
    instance = json.loads(line)
    corpus.append(instance['text'])
    Y.append(instance['lang'])

vectorizer = CountVectorizer(min_df=1)

X = vectorizer.fit_transform(corpus).toarray()

#transformer = TfidfTransformer(smooth_idf=False)
#X = transformer.fit_transform(counts)

#print(X)
#print(Y)

data_csv = open('train_data.csv', 'w')
writer = csv.writer(data_csv)
writer.writerows(X)
data_csv.close()

label_csv = open('label.csv', 'w')
for label in Y:
    label_csv.write(label)
label_csv.close()
