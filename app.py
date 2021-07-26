#import os
import pickle
#import smtplib
#from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
#Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

'''
load_dotenv()

SENDER = os.getenv("SENDER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")
FROM = os.getenv("FROM")
TO = os.getenv("TO")
SUBHAM = os.getenv("SUBHAM")
SUBSPAM = os.getenv("SUBSPAM")
MAILATSPAM = FROM + "\n" + TO + "\n" + SUBSPAM + "\n" + os.getenv("SPAM")
MAILATHAM = FROM + "\n" + TO + "\n" + SUBHAM + "\n" + os.getenv("HAM")

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login(SENDER, PASSWORD)
'''

CVNAME = "spamCv.pickle"
MULTINB = "spamClfModel.sav"
LINSVC = "linearSVC.sav"

cv = pickle.load(open(CVNAME, "rb"))
clfMulNB = pickle.load(open(MULTINB, "rb"))
clfLinSVC = pickle.load(open(LINSVC, "rb"))

models = [clfMulNB, clfLinSVC]
modelNames = ['Multinomial NB', 'Linear SVC']
tas = [0.9784688995215312, 0.9814593301435407]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = [request.form['mail']]
        modelIdx = int(request.form['model'])
        vect = cv.transform(data).toarray()
        idx = models[modelIdx].predict(vect)[0]
        if(idx):
            '''
            try:
                smtpObj.sendmail(SENDER, RECEIVER, MAILATSPAM+data[0])
            except Exception as e:
                print(e)
            '''
            return render_template('home.html', spam=1, mail=data[0], ta=tas[modelIdx], modelName=modelNames[modelIdx])
        else:
            '''
            try:
                smtpObj.sendmail(SENDER, RECEIVER, MAILATHAM+data[0])
            except Exception as e:
                print(e)
            '''
            return render_template('home.html', ham=1, mail=data[0], ta=tas[modelIdx], modelName=modelNames[modelIdx])
    return render_template('home.html')

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
    #smtpObj.quit()