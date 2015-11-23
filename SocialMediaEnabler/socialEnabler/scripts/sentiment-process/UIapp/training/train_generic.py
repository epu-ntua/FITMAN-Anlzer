import os
import nltk
nltk_path = os.path.abspath(os.path.dirname(__file__))
nltk_path = nltk_path + "/nltk_dep"
nltk.data.path.append(nltk_path)
from nltk.corpus import stopwords


def removestopwords(tokens,language):
    unigrams = [w for w in tokens if (w not in stopwords.words(language))]
    return unigrams


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


