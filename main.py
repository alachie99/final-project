import os.path

from flask import Flask, flash, render_template, url_for, request, redirect, session
from joblib import load,dump
import pickle
import json
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import ctypes
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session


app = Flask(__name__)
app.debug = True


app.secret_key = "mysecretekey"





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')




@app.route('/check_text', methods=["POST","GET"])
def check_text():
    response = ''
    if request.method =="POST":
        user_input = request.form["text"]
        #load model
        model = pickle.load(open('model.pkl','rb'))
        vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
        # process text
        vector = vectorizer.transform([user_input])
        result = model.predict(vector)[0]
        if result == 1 :
            response ="This is offensive"
            flash("This is offensive, can not send message")
            return render_template("chat.html")

        elif result == 0:
            flash("This is hate speech, can not send message")
            response =" This is hate speech"
            return render_template("chat.html")
            
        else:
            response = "This is not offensive"
    return render_template('chat.html', response = user_input)



if __name__=="__main__":
    app.run(debug=True)

