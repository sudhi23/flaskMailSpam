from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
#Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
import pickle

CVNAME = "spamCv.pickle"
CLFNAME = "spamClfModel.sav"

cv = pickle.load(open(CVNAME, "rb"))
clf = pickle.load(open(CLFNAME, "rb"))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = [request.form['mail']]
        vect = cv.transform(data).toarray()
        idx = clf.predict(vect)[0]
        if(idx):
            return render_template('home.html', spam=1)
        else:
            return render_template('home.html', ham=1)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)