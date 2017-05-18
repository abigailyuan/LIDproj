import json
import numpy as np
import re
import string
from collections import defaultdict as dd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn import svm




######################preprocessing####################

fp = open('devfile.json')
data = []
target = []

'''
clean text by removing punctuatuations and numbers, removing instance
whose text is too short, and convert all texts to lowercase
'''
for line in fp:
    filtered_text = []
    instance = json.loads(line)
    word_list = instance['text'].split()
    for word in word_list:
        if ('@' not in word) and ('#' not in word) and ('http' not in word):
            word = re.sub('[%s]' % re.escape(string.punctuation),'',word)
            word = re.sub('\d','',word)
            if word != '':
                filtered_text.append(word.lower())
    instance['text'] = ' '.join(filtered_text)
    if len(instance['text']) > 10:
        if 'location' in instance.keys():
            data.append(instance['text']+instance['location'])
        else:
            data.append(instance['text']+'unknown')
        target.append(instance['lang'])
  

train_length = len(data)

fp1 = open('testfile.json')
for line in fp1:
    filtered_text = []
    instance = json.loads(line)
    word_list = instance['text'].split()
    for word in word_list:
        if ('@' not in word) and ('#' not in word) and ('http' not in word):
            word = re.sub('[%s]' % re.escape(string.punctuation),'',word)
            word = re.sub('\d','',word)
            if word != '':
                filtered_text.append(word.lower())
    instance['text'] = ' '.join(filtered_text)
    if 'location' in instance.keys():
        data.append(instance['text']+instance['location'])
    else:
        data.append(instance['text']+'unknown')
    target.append(instance['lang'])



categories = {'ar': 1,
              'bg': 2,
              'de': 3,
              'en': 4,
              'es': 5,
              'fa': 6,
              'fr': 7,
              'he': 8,
              'hi': 9,
              'it': 10,
              'ja': 11,
              'ko': 12,
              'mr': 13,
              'ne': 14,
              'nl': 15,
              'ru': 16,
              'th': 17,
              'uk': 18,
              'ur': 19,
              'zh': 20,
              'unk': 21}
target = np.array(target)
for i in range(len(target)):
    target[i] = categories[target[i]]

data = np.array(data)
fp.close()
fp1.close()
hv = HashingVectorizer(n_features=1500, token_pattern=r'\b\w+\b',ngram_range=(2,2), analyzer='char_wb')
X = hv.transform(data).toarray()
transformer = TfidfTransformer(smooth_idf=False)
X2 = transformer.fit_transform(X).toarray()
########################classifier starts now###################
'''GaussianNB'''
clf1 = GaussianNB()
clf1.fit(X2[:train_length], target[:train_length])
score = clf1.score(X2[train_length:], target[train_length:])
print('NB score = '+str(score))

'''Decision tree'''
one_r = DecisionTreeClassifier()
one_r.fit(X2[:train_length], target[:train_length])
score = one_r.score(X2[train_length:], target[train_length:])
print('Decision tree score = '+str(score))

'''SVM'''
clf2 = svm.LinearSVC()
clf2.fit(X2[:train_length], target[:train_length])
score = clf2.score(X2[train_length:], target[train_length:])
print('SVM score = '+str(score))















