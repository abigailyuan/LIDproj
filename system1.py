import csv
from collections import defaultdict
from math import sqrt
from plotter import plot_scores

def count_trigrams(document):
    """ count_trigrams takes a string and returns a dictionary of the counts 
    of trigrams within the document. """
    count_dict = dd(float)
    i = 0
    
    for i in range(len(document[:-2])):
        trig = document[i:i+3]
        count_dict[trig] += 1.0
    
    return count_dict

def train_classifier(training_set):
    """ train_classifier takes a csv file training_set and returns a dictionary 
    containing dictionaries for each language label with the average frequency 
    of occurrence of trigrams per language. 
    """
    tset_reader = csv.reader(open(training_set, 'r'))
    
    # find the counts for each language 
    lang_dict = {}
    for row in tset_reader:
        (lang, text) = row
        if lang not in lang_dict:
            lang_dict[lang] = dd(float)
        trigram_dict = count_trigrams(text)
        for trigram in trigram_dict:
            lang_dict[lang][trigram] += trigram_dict[trigram]

    # normalise over the number of trigrams per language
    for (lang, count_dict) in lang_dict.items():
        lang_len = sqrt(sum([val**2 for val in count_dict.values()]))
        for key in count_dict.keys():
            count_dict[key] /= lang_len

    return lang_dict
default_lang_counts = train_classifier('train.csv')

def score_document(document, lang_counts=default_lang_counts):
    """ score_document takes a string document and a dictionary of language 
    counts per language stored in lang_counts. It returns a dictionary of 
    scores for the document for each language.
    """
    doc_text = open(document, 'r').read()
    doc_counts = count_trigrams(doc_text)
    languages = lang_counts.keys()
    score_dict = {}
    for lang in languages:
        
        # calculate the score for this language by performing a dot product
        score = 0.0
        for trigram in doc_counts.keys():
            score += doc_counts[trigram] * lang_counts[lang][trigram]
            
        score_dict[lang] = score
    return score_dict

# Tolerance for detecting null predictions
TOL = 1e-10

# We train the classifier here
default_lang_counts = train_classifier('train.csv')

def classify_doc(document, lang_counts=default_lang_counts):
    """ classify_document returns the language of the document according to the 
    dictionary of language counts lang_counts.
    """
    scores = score_document(document, lang_counts)
    
    vals = sorted(scores.values(), reverse=True)
    if abs(vals[1] - vals[0]) <= TOL:
        return "English"
    else:
        return max([(score, lang) for (lang, score) in scores.items()])[1]

def score_document(document, lang_counts=default_lang_counts):
    # Your code here
    pass

def select_scores(langs, document, lang_counts=default_lang_counts):
    # Your code here
    pass

# Run this to have a look at some plots
#langs = ['English', 'Indonesian', 'German', 'French','Malay']
#doc = open('Indonesian1.txt').read()
#(langs, scores) = select_scores(langs,doc)
#plot_scores(langs, scores)

# Increase the field size limit (we have big files)
csv.field_size_limit(int(1e7))

# We train the classifier here
default_lang_counts = train_classifier('small_train.csv')

def calc_precision(test_set):
    """calc_precision takes the filename of a csv file test_set and returns 
    a dictionary of the precision of the classifier per language."""
    
    # iterate through the test set, tallying the number of predictions for each 
    # language and the number of those which were correct
    t_reader = csv.reader(open(test_set, 'r'))
    pred_counts = dd(int)
    correct_counts = dd(int)
    for row in t_reader:
        (lang, doc) = row
        pred = classify_doc(doc, default_lang_counts)
        pred_counts[pred] += 1
        correct_counts[lang] += (lang == pred)
    
    # Use the tallies to find the precision for each language.
    precision_dict = dd(float)
    for (lang, pcount) in pred_counts.items():
        precision_dict[lang] = float(correct_counts[lang])/pcount
    
    return precision_dict

def calc_recall(test_set):
    """calc_recall takes the filename of a csv file test_set and returns a
    dictionary of the recall of the classifier per language."""
    
    # iterate through the test set, recording the number of documents in each 
    # language as well as the number correctly classified.
    t_reader = csv.reader(open(test_set, 'r'))
    lang_counts = dd(int)
    correct_counts = dd(int)
    for row in t_reader:
        (lang, doc) = row
        lang_counts[lang] += 1
        pred = classify_doc(doc, default_lang_counts)
        correct_counts[lang] += (pred == lang)
    # find the recall per language
    recall_dict = dd(float)
    for (lang, count) in lang_counts.items():
        recall_dict[lang] = float(correct_counts[lang])/count
    
    return recall_dict
