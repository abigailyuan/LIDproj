from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict as dd
import json

def createCorpus(filename):
    f = open(filename)
    data_dict = dd(list)
    for line in f:
        j_content = json.loads(line)
        data_dict[j_content['lang']].append(j_content['text'])
    f.close()
    return data_dict

def vectorize(data_dict):
    vectorDict = {}
    corpus = []
    for lang in data_dict.keys():
        string = ''
        for text in data_dict[lang]:
            string += text
        corpus.append(string)
    vectorizer = CountVectorizer(min_df=1, ngram_range=(2,6), token_pattern=r'\b\w+\b')
    X = vectorizer.fit_transform(corpus).toarray() #X is the classifier metrix
    print(X)

data_dict = createCorpus('trainfile.json')
vectorize(data_dict)
