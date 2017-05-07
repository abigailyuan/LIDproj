import json
import re
import string
from collections import defaultdict as dd
from pprint import pprint


import collections

N = 4

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
        itemDict = {'lang': 'unknown', 'displayname': 'unknown', 'location': 'unknown', 'text':'unknown'}
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

##print("----------dev file--------------")
##countFile('dev.json')
##print("------------train file---------")
##countFile('train.json')
##text = getTextList('dev.json')
##for i in text:
##    print(i)
print("----------parsed data-------------")
dataList = parseText('dev.json')
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
print (dataList)
