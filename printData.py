import json
import re
import string
import math
from collections import defaultdict as dd
from pprint import pprint
from sklearn.dummy import DummyClassifier


import collections
#N grams
N = 4
#K first frequent Ngrams
K = 5


def countFile(filename):
    '''count number of instances for each language in the file'''
    json_data = open(filename)
    data = json.load(json_data)
    #print(data)
    langDict = dd(int)
    for item in data:
        lang = item.get("lang")
        langDict[lang] += 1
    #print("-----------dev data-------------")
    for key in langDict.keys():
        print(key+": "+str(langDict[key]))
    json_data.close()
    return langDict

def getTextList(filename):
    json_data = open(filename)
    data = json.load(json_data)
    textList = []
    for item in data:
        text = item.get('text').split()
        textList.append(text)
    return textList

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
        
def removeSuffix(dataList):
    for instance in dataList:
        newList = []
        for word in instance['text']:
            while(len(word) > 0):
                if(word[-1] in '~`!@"#$%^&*()_+-={ }|\[]:;<>?/,."'):
                    word = word[:-1]
                else:
                    newList.append(word)
                    break
        instance['text'] = newList
    return dataList

def removePreffix(dataList):
    for instance in dataList:
        newList = []
        for word in instance['text']:
            while(len(word) > 0):
                if(word[0] in '~`!@"#$%^&*()_ +-={}|\[]:;<>?/,."'):
                    word = word[1:]
                else:
                    newList.append(word)
                    break
        instance['text'] = newList
    return dataList

def removeEmptyString(dataList):
    for instance in dataList:
        newList = []
        for word in instance['text']:
            if(len(word) > 0):
                newList.append(word)
        instance['text'] = newList
    return dataList

def removeWord(word):
    while(len(word) > 0):
        if(word[-1] in '~`!@"#$%^&*()_+-={}|\ []:;<>?/,."'):
            word = word[:-1]
        else:
            break

def count_Ngrams(document, N):
    """ count_trigrams takes a string and returns a dictionary of the counts 
    of trigrams within the document. """
    count_dict = dd(float)
    i = 0
    length = 1 - N
    Ngrams = []
    for word in document:
        if(len(word) < N):
            Ngrams.append(word)
        else:
            for i in range(0, len(word)-length):
                Ngram = word[i:i+N]
                if(Ngram not in Ngrams):
                    Ngrams.append(Ngram)
    
    return Ngrams

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
#def fullDimensionLangDict(langDict):
    

def toList(langDict, K):
    langList = []
    for key in langDict.keys():
        (k, v) = (langDict[key], key)
        langList.append((k, v))
    if(K):
        langList = sorted(langList, reverse=True)[:K]
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
    #create header
    header = []
    for ngram in Ngramset:
        header.append(ngram)
    header.append('lang')
    #train_data.append(header)
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
    #print(length)
    for i in range(len(instance)-1):
        instance[i] /= length
    print(instance)
    return instance

def normaliseAll(train_data):
    for instance in train_data:
        instance = normaliseInstance(instance)
    return train_data


print("----------read and tokenize data-------------")
dataList = parseText('dev.json')
print('             done')
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
    i['awl'] = averageWordLength(i['text'])
    i['text'] = count_Ngrams(i['text'], N)
dataList = removeEmptyString(dataList)
print('              done')
#print(dataList)
print('-------------create prototype---------------')
langDict = countLanguageNgrams(dataList)
langNgramList = createPrototype(langDict)
print(langNgramList)
print('              done')
print('-------------create a set of all Ngrams------')

#create a set of all K most frequent Ngrams in langlist
Ngramset = set()
for item in langNgramList:
    for ngram in item[:-1]:
        Ngramset.add(ngram[1])
#print(Ngramset)
print('             done')
print('----create all dimensions for all prototypes----')
#create train_data
train_data = createTrainData(Ngramset, langDict)
#print(train_data)
print('             done')
print('-------------------normalise train data-----------')
train_data = normaliseAll(train_data)
#print(train_data)
        

print('--------------summary-----------------')
print('N = '+str(N))
print('K = '+str(K))
print("num of ngrams: "+str(len(Ngramset)))
