import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from os import path
import nltk
nltk_path = os.path.abspath(os.path.dirname(__file__))
nltk_path = nltk_path + "/nltk_dep"
nltk.data.path.append(nltk_path)
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from train_generic import stem_tokens
from train_generic import removestopwords


def tokenize(text):
    language = 'english'
    #tokens = nltk.word_tokenize(text)
    #tokens = wordpunct_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tokens = removestopwords(tokens,language)
    stemmer = PorterStemmer()
    stems = stem_tokens(tokens, stemmer)
    return stems


def train_en(trainingFile,learnt_model_file):
    path = default_storage.save('tmp/'+str(trainingFile),ContentFile(trainingFile.read()))
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    classes = ["positive", "negative"]

    # Read the data
    train_data = []
    train_labels = []
    with open(file_path, 'r') as f:
	for line in f:
            line = line.rstrip()
            contents = line.split(',')
            if not len(contents)==2:
                continue
            contents[1] = contents[1].rstrip()
            contents[0] = contents[0].rstrip()
            if contents[1] in classes:
                train_data.append(contents[0])
                train_labels.append(contents[1])

    # Create vectorizer
    vectorizer = TfidfVectorizer(tokenizer=tokenize,min_df=1,
                                 max_df = 0.95,
                                 sublinear_tf=True,
                                 use_idf=True, ngram_range=(1, 3))

   

    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    vectorizer_classifier_combo = Pipeline([('vectorizer', vectorizer), ('classifier', classifier_linear)])
    vectorizer_classifier_combo.fit(train_data, train_labels)
    directory = learnt_model_file
    if not os.path.exists(directory):
        os.makedirs(directory)
    learnt_model_file = learnt_model_file + "model_english.pkl"
    joblib.dump(vectorizer_classifier_combo, learnt_model_file)
    model = joblib.load(learnt_model_file)
    prediction = model.predict(train_data)
    print(classification_report(train_labels, prediction))
    i = 0
    for p in prediction:
        if not prediction[i] == train_labels[i]:
            print i
            print train_data[i]
        i+=1

def retrieve_file_en(trainingFile):
    path = default_storage.save('tmp/'+str(trainingFile),ContentFile(trainingFile.read()))
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    return str(file_path)

