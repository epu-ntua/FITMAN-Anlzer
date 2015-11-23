import nltk
import sys
from os import path
nltk.data.path.append(path.dirname( path.dirname( path.abspath(__file__) ) )+"/nltk_dep")
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

def idlan(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    ratios = {}
    for language in {'spanish','english'}:
        stopwords_set = set(stopwords.words(language))
        words_set = set(tokens)
        common_elements = words_set.intersection(stopwords_set)
        ratios[language] = len(common_elements)
    most_rated_language = max(ratios, key=ratios.get)
    #favor spanish - TODO reconsider
    if ratios[most_rated_language] == 0:
        return 'spanish'
    if ratios['english']==ratios['spanish']:
        return 'spanish'
    if most_rated_language == 'spanish':
        return most_rated_language
    return most_rated_language

