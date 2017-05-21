import json
import csv
import numpy as np
import re
import string
from collections import defaultdict as dd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
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
timeout = 20000
current_num = 0
for line in fp:
    current_num+=1
    
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
    if current_num == timeout:
        break

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
categories_reverse = {'1': 'ar',
                      '2': 'bg',
                      '3': 'de',
                      '4': 'en',
                      '5': 'es',
                      '6': 'fa',
                      '7': 'fr',
                      '8': 'he',
                      '9': 'hi',
                      '10': 'it',
                      '11': 'ja',
                      '12': 'ko',
                      '13': 'mr',
                      '14': 'ne',
                      '15': 'nl',
                      '16': 'ru',
                      '17': 'th',
                      '18': 'uk',
                      '19': 'ur',
                      '20': 'zh',
                      '21': 'unk'}
target = np.array(target)
for i in range(len(target)):
    target[i] = categories[target[i]]

data = np.array(data)
fp.close()
fp1.close()
hv = HashingVectorizer(n_features=40000, token_pattern=r'\b\w+\b',ngram_range=(1,6), analyzer='char_wb')
X = hv.transform(data).toarray()
transformer = TfidfTransformer(smooth_idf=True)
X2 = transformer.fit_transform(X).toarray()
######################classifier starts now###################
##'''GaussianNB'''
##clf1 = GaussianNB()
##clf1.fit(X2[:train_length], target[:train_length])
##score = clf1.score(X2[train_length:], target[train_length:])
##print('NB score = '+str(score))
##
##'''Decision tree'''
##one_r = DecisionTreeClassifier()
##one_r.fit(X2[:train_length], target[:train_length])
##score = one_r.score(X2[train_length:], target[train_length:])
##print('Decision tree score = '+str(score))
##
##'''SVM'''
##clf2 = svm.LinearSVC()
##clf2.fit(X2[:train_length], target[:train_length])
##score = clf2.score(X2[train_length:], target[train_length:])

'''Bagging'''
bagging = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)
bagging.fit(X2[:train_length], target[:train_length])
score = bagging.score(X2[train_length:], target[train_length:])
print('bagging score = '+str(score))
##print('start to predict.....')
##y = bagging.predict(X2[train_length:])
##print('start to write file.....')
####print('SVM score = '+str(score))
##id = 0
##data_2d = []
##data_2d.append(['docid','lang'])
##fp3 = open('submit.csv', 'w')
##for i in y:
##    print('a')
##    idstr = ''
##    if id / 10 < 1:
##        idstr = '000'+ str(id)
##    elif id / 10 <10:
##        idstr = '00' + str(id)
##    elif id / 10 <100:
##        idstr = '0' + str(id)
##    elif id / 10 < 1000:
##        idstr = str(id)
##    instance = ['test'+idstr, categories_reverse[i]]
##    data_2d.append(instance)
##    id += 1
##writer = csv.writer(fp3)
##print('start to write rows.....')
##writer.writerows(data_2d)
##fp3.close()
##i=2
##while(i<30):
##    hv = HashingVectorizer(n_features=1500, token_pattern=r'\b\w+\b',ngram_range=(2,i), analyzer='char_wb')
##    X = hv.transform(data).toarray()
##    transformer = TfidfTransformer(smooth_idf=False)
##    X2 = transformer.fit_transform(X).toarray()
##    clf1 = GaussianNB()
##    clf1.fit(X2[:train_length], target[:train_length])
##    score = clf1.score(X2[train_length:], target[train_length:])
##    print('range = '+str(i)+'NB score = '+str(score))
##    i+=1











