
import os
import re
import pickle
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB

## ---------------------------------------- Config Section ---------------------------------------- ##

training_file = 'training.csv'
testing_file = 'testing.csv'

## -------------------------------------- End Config Section -------------------------------------- ##
def preprocess(data):
    # Remove urls
    data = re.sub(r'^https?:\/\/.*[\r\n]*', '', data, flags=re.MULTILINE)
    # Remove HTML
    noHtml = BeautifulSoup(data, "html.parser")
    noHtml =  noHtml.get_text()
    # Convert to lower case, split into individual words
    lowers = noHtml.lower()
    line = lowers.decode('ascii', 'ignore').encode('ascii')
    # cv = TfidfVectorizer()
    # docs_new = []
    # docs_new.append(line)
    # x_testcv = cv.transform(docs_new)
    # print x_testcv
    # return x_testcv
    return line
def save_classifier(classifier):
    f = open('classifier-new-1.pickle', 'wb')
    pickle.dump(classifier, f, -1)
    f.close()

def load_classifier():
    f = open('classifier-new-1.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier
def trainModel():
    df = pd.read_csv(training_file,sep = ',',names = ['CaseCreated', 'Post'],skiprows=1)
    # print len(df[df.CaseCreated == '0'])
    df_x = df['Post']
    df_y = df['CaseCreated']
    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.3)
    # print x_traincv.toarray()
    # print cv.get_feature_names()
    cv = CountVectorizer(min_df = 1, stop_words = 'english',decode_error = 'ignore')
    x_traincv = cv.fit_transform(x_train)
    # train = x_traincv.toarray()
    x_testcv = cv.transform(x_test)
    model = MultinomialNB()
    # et = ExtraTreesClassifier()
    model = model.fit(x_traincv,y_train)
    save_classifier(model)
    pickle.dump(cv, open('vectorizer.pickle', 'wb'), -1)
    predictions = model.predict(x_testcv)
    actual = np.array(y_test)
    # Calculating Accuracy
    count = 0
    for i in range(len(predictions)):
        if predictions[i] == actual[i]:
            count += 1
    # print "Count = %d" % count
    # print "Predictions = %d" % len(predictions)
    accuracy = (float(count)/float(len(predictions))) * 100
    print "Accuracy of this model is : %.2f%%" % accuracy
    return model
def main(text):
    if os.path.isfile('classifier-new-1.pickle'):
        print 'classifier file found.'
        cl = load_classifier()
    else:
        print 'classifier file not fount. Creating a new classifier file as classifier.pickle'
        cl = trainModel()

    # text = raw_input("Enter the post: ")
    line = preprocess(text)
    vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    x_testcv = vectorizer.transform([line])
    return cl.predict(x_testcv)[0]
