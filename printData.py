import json
from collections import defaultdict as dd
from pprint import pprint


import collections


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
        dataDict = {'lang': null, 'displayname': null, 'location': null, 'text': null}
        





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
    print(i)
