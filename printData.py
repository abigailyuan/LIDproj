import json
import re
import string
import math
from collections import defaultdict as dd
from pprint import pprint
from sklearn.dummy import DummyClassifier
import numpy


import collections
#N grams
N = 4
#K first frequent Ngrams
K = 10
header = []

def parseText(filename):
    json_data = open(filename)
    data = json.load(json_data)
    dataList = []
    for item in data:
        text = item.get('text').split()
        item['text']= text
        itemDict = {'lang': 'unknown', 'displayname': 'unknown', 'location': 'unknown', 'text':'unknown', 'awl': 0}
        for key in item.keys():
            if(key != 'uid'):
                itemDict[key] = item[key]
        dataList.append(itemDict)
    return dataList

def readToList(filename):
    '''read to a list of instances while each instance is a dictionary'''
    fileList = []
    json_data = open(filename)
    data = json.load(json_data)
    for instance in data:
        dataDict = {'lang': null, 'displayname': null, 'location': null, 'text': null, 'awl': 0}
        
def removeEmptyString(dataList):
    for instance in dataList:
        newList = []
        for word in instance['text']:
            if(len(word) > 0):
                newList.append(word)
        instance['text'] = newList
    return dataList

def count_Ngrams(document, N):
    """ count_trigrams takes a string and returns a dictionary of the counts 
    of trigrams within the document. """
    return zip(*[document[i:] for i in range(N)])


def averageWordLength(data):
    length  = 0
    for i in data:
        length += len(i)
    if(len(data) != 0):
        return length / len(data)
    else:
        return 0

def countLanguageNgrams(dataList):
    langDict = {}
    for instance in dataList:
        NgramDict = {}
        if(instance['lang'] not in langDict.keys()):
            langDict[instance['lang']] = NgramDict
        for Ngram in instance['text']:
            if(Ngram not in langDict[instance['lang']].keys()):
                langDict[instance['lang']][Ngram] = 1
            else:
                langDict[instance['lang']][Ngram] += 1
    return langDict

    

def toList(langDict, K):
    langList = []
    for key in langDict.keys():
        (k, v) = (langDict[key], key)
        langList.append((k, v))
    if(K):
        ind = numpy.argpartition([freq for (freq, lang) in langList], -K)[-K:]
        langList = sorted([langList[i] for i in ind])###########
    else:
        langList = sorted(langList, reverse=True)
    return langList

    
def createPrototype(langDict):
    '''input a langDict and
        return a list of [(frequency, ngram),...,(frequency, ngram), label]'''
    langNgramList = []
    #print(langDict)
    for lang in langDict.keys():
        langList = toList(langDict[lang], K)
        langList.append(lang)
        langNgramList.append(langList)
    return langNgramList

def createTrainData(ngramset, langDict):
    train_data = []
    for ngram in Ngramset:
        header.append(ngram)
    header.append('lang')
    for lang in langDict.keys():
        instance = []
        for ngram in header[:-1]:
            if ngram in langDict[lang].keys():
                instance.append(langDict[lang][ngram])
            else:
                instance.append(0)
        instance.append(lang)
        train_data.append(instance)
    return train_data

def getInstanceLength(instance):
    length = 0.0
    for i in instance[:-1]:
        length += (i*i)
    return math.sqrt(length)

def normaliseInstance(instance):
    length = getInstanceLength(instance)
    for i in range(len(instance)-1):
        instance[i] /= length
    return instance

def normaliseAll(train_data):
    for instance in train_data:
        instance = normaliseInstance(instance)
    return train_data

def createVector(Ngrams):
    Ngramcount = {}
    notInSet = {}
    for i in header[:-1]:
        if i not in Ngramcount.keys():
            Ngramcount[i] = 0
    for i in Ngrams:
        if i in Ngramcount.keys():
            Ngramcount[i] += 1
        else:
            if i in notInSet.keys():
                notInSet[i] += 1
            else:
                notInSet[i] = 1
    vector = []
    for i in header[:-1]:
        frequency = Ngramcount[i]
        vector.append(frequency)
        
    return vector

def computerScores(train_data, vector):
    scores = []
    for lang in train_data:
        score = 0
        for i in range(len(lang[:-1])):
            score += lang[i] * vector[i]
        scores.append((score, lang[-1]))
    return sorted(scores, reverse=True)


    
def processTest(test):
    #tokenize test data
    test = test.split()

    #clearify test data
    buffer = []
    for i in test:
        if ('@' not in i) and ('#' not in i) and ('http' not in i):
            i = re.sub('[%s]' % re.escape(string.punctuation),'',i)
            i = re.sub('\d','',i)
            if i != '':
                buffer.append(i)
    test = buffer

    #create Ngrams
    Ngrams = count_Ngrams(test, N)

    #create vector for test
    vector = createVector(Ngrams)

    #compute scores for each language
    scores = computerScores(train_data, vector)

    return scores

def doTest(filename):
    json_data = open(filename)
    data = json.load(json_data)
    numOfTest = 0
    numOfCorrect = 0
    for item in data:
        numOfTest += 1
        prediction = processTest(item['text'])[0][1]
        if(prediction == item['lang']):
           numOfCorrect += 1
    accuracy = float(numOfTest) / numOfTest
    print('numOfTest = '+str(numOfTest))
    print('numOfCorrect = '+str(numOfCorrect))
    print('accuracy = '+str(accuracy))

print("----------read and tokenize data-------------")
dataList = parseText('train.json')
print('-----------count Ngrams----------------------')
for i in dataList:
    buffer = []
    for j in i['text']:
        if ('@' not in j) and ('#' not in j) and ('http' not in j):
            j = re.sub('[%s]' % re.escape(string.punctuation),'',j)
            j = re.sub('\d','',j)
            if j != '':
                buffer.append(j)
    i['text'] = buffer
    #i['awl'] = averageWordLength(i['text'])
    i['text'] = count_Ngrams(i['text'], N)
    print('counted '+i['lang'])
dataList = removeEmptyString(dataList)

print('-------------create prototype---------------')
langDict = countLanguageNgrams(dataList)
langNgramList = createPrototype(langDict)

print('-------------create a set of all Ngrams------')

#create a set of all K most frequent Ngrams in langlist
Ngramset = set()
for item in langNgramList:
    for ngram in item[:-1]:
        Ngramset.add(ngram[1])

print('----create all dimensions for all prototypes----')
#create train_data
train_data = createTrainData(Ngramset, langDict)

print('-------------------normalise train data-----------')
train_data = normaliseAll(train_data)

        
##
##print('--------------summary-----------------')
##print('N = '+str(N))
##print('K = '+str(K))
##print("num of ngrams: "+str(len(Ngramset)))
print('----------------test----------------')
##flag = True
##while(flag):
##    test = input('enter the text for testing:\n')
##    if(test == 'quit'):
##        flag = False
##        break
##    scores = processTest(test)
##    print('prediction: '+scores[0][1])
##    print('---------------------------------------')
doTest('testLabel.json')
