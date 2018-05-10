
# A very simple Flask Hello World app for you to get started with...
import numpy as np
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import sklearn
print(sklearn.__version__)
from sklearn.externals import joblib # <---- import pickle library

clf = joblib.load('ico_predictor.pkl')

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    if request.method == 'GET':
        return render_template('home.html')
    return redirect(url_for('home.html'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    return redirect(url_for('contact.html'))



@app.route('/model')
def model():
    return app.send_static_file('model.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    platform = str(request.form['input_platform'])
    if platform == 'ETH':
        ETH = 1
        NEO = 0
        OTHER = 0
        OWN = 0
        WAVES = 0
    elif platform == 'NEO':
        ETH = 0
        NEO = 1
        OTHER = 0
        OWN = 0
        WAVES = 0
    elif platform == 'OTHER':
        ETH = 0
        NEO = 0
        OTHER = 1
        OWN = 0
        WAVES = 0
    elif platform == 'OWN':
        ETH = 0
        NEO = 0
        OTHER = 0
        OWN = 1
        WAVES = 0
    elif platform == 'WAVES':
        ETH = 0
        NEO = 0
        OTHER = 0
        OWN = 0
        WAVES = 1

    raised = int(request.form['input_total_raised'])
    whitelist = int(request.form['input_whitelist'])
    alexa = int(request.form['input_alexa'])
    twitter = int(request.form['input_twitter'])
    telegram = int(request.form['input_telegram'])
    rating = float(request.form['input_rating'])
    origin = str(request.form['input_origin'])
    if origin == 'Africa':
        Africa = 1
        Americas = 0
        Asia = 0
        Europe = 0
    elif origin == 'Americas':
        Africa = 0
        Americas = 1
        Asia = 0
        Europe = 0
    elif origin == 'Asia':
        Africa = 0
        Americas = 0
        Asia = 1
        Europe = 0
    elif origin == 'Europe':
        Africa = 0
        Americas = 0
        Asia = 0
        Europe = 1

    prediction = clf.predict([[raised, alexa, twitter, whitelist, telegram, rating, ETH, NEO, OTHER, OWN, WAVES, Africa, Americas, Asia, Europe]])

    if prediction[0] == 1:
        return 'ROI Higher than 50% is expected.'
    else:
        return 'ROI Less than 50% is expected. May want to look into different investments.'
