import collections
import re
from flask.helpers import  send_file
import absorbProfile as absorbprofile
import os
from flask import Flask, render_template, request
import pandas as pd
import SVM_model_arabic as SVMAR
import SVM_model_hebrew as SVMHE

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def clssifydatabase(filepath):
    result = "test"
    print(filepath)
    model_name = request.form['model_name']

    if model_name == 'Hebrew':
        offensive_count, non_Offensive = SVMHE.classify_DB(filepath)

    elif model_name == 'Arabic':
        offensive_count, non_Offensive = SVMAR.classify_DB(filepath)

    neutral_percent = int(non_Offensive/(offensive_count + non_Offensive) * 100)
    result = [neutral_percent, 100 - neutral_percent]
    return render_template('classifyDB.html', result=result)
    




@app.route("/")
def index():
    # target = os.path.join(APP_ROOT, 'uploads/classified.xlsx')
    # if os.path.isfile(target):
    try:
        os.remove('uploads/classified.xlsx')
    except:
        print("There are no classified File")
    return render_template('index.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/ClassifyText', methods=['POST'])
def ClassifyText():
    model_name = request.form['model_name']
    tweet_content = request.form['tweet_content']
    
    if model_name == 'Hebrew':
        result = SVMHE.predict(tweet_content)
        result = 'Not Offensive' if (result == [0]) else 'Offensive'

    if model_name == 'Arabic':
        result = SVMAR.predict(tweet_content)
        result = 'Not Offensive' if (result == [0]) else 'Offensive'

    res = [tweet_content,result]
    return render_template('prediction.html', result=res)



@ app.route('/classifyProfile', methods=['POST'])
def classifyProfile():
    profile_name = request.form['profile_name']
    filepath = absorbprofile.get_tweets(profile_name)
    print(filepath)
    model_name = request.form['model_name']

    if model_name == 'Hebrew':
        offensive_count, non_Offensive = SVMHE.classify_DB(filepath)

    elif model_name == 'Arabic':
        offensive_count, non_Offensive = SVMAR.classify_DB(filepath)
    df = pd.read_excel('uploads/classified.xlsx')
    l = df.iloc[0:,0]
    off= df.iloc[0:,1]
    neutral_percent = int(non_Offensive/(offensive_count + non_Offensive) * 100)
    # result ='The number of neutral = '+str(neutral_percent) + '%, the number of Offensive = ' + str(100 - neutral_percent) +'%'
    result = [profile_name, neutral_percent,l,off]
    
    print('remove file - ', filepath)
    # os.remove(filepath)
    return render_template('classifyProfile.html', result=result)

    # --------------------- End Writing -----------------------------

@ app.route('/classifyDB', methods=['POST'])
def classifyDB():
    target = os.path.join(APP_ROOT, 'uploads\\')
    if not os.path.isdir(target):
        os.mkdir(target)
    destination=''
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
    print(destination)   
    return clssifydatabase(destination) # run the models on the uploaded model



@app.route('/download', methods=['GET', 'POST'])
def download():
    uploads = os.path.join(APP_ROOT, 'uploads/classified.xlsx')
    return send_file(uploads, as_attachment=True)

if __name__ == '__main__':
   app.run(debug=True)


