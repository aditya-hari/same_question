from utils import get_result
from keras.models import load_model
from keras.models import model_from_json

import tensorflow as tf
from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, SubmitField

from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from keras.preprocessing.sequence import pad_sequences
import pickle, re

app = Flask(__name__)

class ReusableForm(Form):
    question1 = TextField("Enter first question':", validators=[
                     validators.InputRequired()])
    question2 = TextField("Enter second question':", validators=[
                     validators.InputRequired()])
    submit = SubmitField("Enter")


def load_keras_model():
    global model, stop_words, vocab
    stop_words = set(stopwords.words('english'))
    f = open('/home/aditya/Documents/Flask/Questions/vocab','rb')
    vocab = pickle.load(f)
    f.close()
    with open('/home/aditya/Documents/Flask/Questions/model.json','r') as f:
        model_json = f.read()
    model = model_from_json(model_json)
    model.load_weights('/home/aditya/Documents/Flask/Questions/model.h5')
    
@app.route("/",  methods=['GET', 'POST'])
def frontpage():
    return render_template('frontpage.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    # Create form
    form = ReusableForm(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        question1 = request.form['question1']
        question2 = request.form['question2']
        return render_template('result.html', input=get_result(model=model, question1=question1, question2=question2, stop_words=stop_words, vocab=vocab))
    # Send template information to index.html
    return render_template('index.html', form=form)

@app.route("/howitworks", methods=["GET", "POST"])
def howitworks():
    return render_template('howitworks.html')

@app.route('/abstract', methods=["GET",'POST'])
def abstract():
    return render_template('abstract.html')

@app.route('/presentation', methods=["GET",'POST'])
def presentation():
    return render_template('presentation.html')
    
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_keras_model()
    # Run app
    app.run(host="0.0.0.0", port=8000, threaded=False)