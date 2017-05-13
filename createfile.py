import json
import numpy as np
import re
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


#####################preprocessing###################
fp = open('devfile.json')
data = []
target = []

for line in fp:
    instance = json.loads(line)
    target.append(instance['lang'])
##    data.append(instance['text'])
    if 'location' in instance.keys():
        data.append(instance['text']+instance['location'])
    else:
        data.append(instance['text']+'unknown')

fp1 = open('testfile.json')

for line in fp1:
    instance = json.loads(line)
    target.append(instance['lang'])
##    data.append(instance['text'])
    if 'location' in instance.keys():
        data.append(instance['text']+instance['location'])
    else:
        data.append(instance['text']+'unknown')

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
print(target)
data = np.array(data)
fp.close()
fp1.close()
hv = HashingVectorizer(n_features=2000, token_pattern=r'\b\w+\b',ngram_range=(1,5), analyzer='char_wb')
X = hv.transform(data.ravel()).toarray()
transformer = TfidfTransformer(smooth_idf=False)
X2 = transformer.fit_transform(X).toarray()
########################classifier starts now###################
'''GaussianNB'''
clf1 = GaussianNB()
clf1.fit(X2[:8899], target[:8899])
score = clf1.score(X2[8899:], target[8899:])
print('NB score = '+str(score))

'''Decision tree'''
one_r = DecisionTreeClassifier()
one_r.fit(X2[:8899], target[:8899])
score = one_r.score(X2[8899:], target[8899:])
print('Decision tree score = '+str(score))

'''SVM'''
clf2 = svm.LinearSVC()
clf2.fit(X2[:8899], target[:8899])
score = clf2.score(X2[8899:], target[8899:])
print('SVM score = '+str(score))

