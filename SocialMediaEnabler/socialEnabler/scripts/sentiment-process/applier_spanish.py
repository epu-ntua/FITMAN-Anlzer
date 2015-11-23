# -*- coding: utf-8 -*-

from sklearn.externals import joblib
import nltk
import sys
from os import path
nltk.data.path.append(path.dirname( path.dirname( path.abspath(__file__) ) )+"/nltk_dep")
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

def removestopwords(tokens,language):
    unigrams = [w for w in tokens if (w not in stopwords.words(language))]
    return unigrams


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    language = 'spanish'
    stemmer = PorterStemmer()
    #tokens = nltk.word_tokenize(text)
    #tokens = wordpunct_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tokens = removestopwords(tokens,language)
    stems = stem_tokens(tokens, stemmer)
    return stems

def applier(text,file_dir):
    #file_dir = script_settings.en_model
    learnt_model_file = file_dir+'model_spanish.pkl'
    model = joblib.load(learnt_model_file)
    textA = []
    textA.append(text) 	
    prediction = model.predict(textA)
    return prediction[0]
