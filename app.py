import pandas as pd
import os
from flask import Flask, render_template, request
import pandas as pd
import SVM_model_arabic as SVMAR
import SVM_model_hebrew as SVMHE
import joblib

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
def clssifydatabase(filepath):
    result="test"
    print(filepath)
    model_name = request.form['model_name']
    '''
    if model_name == 'SVM for Hebrew':
        offensive_count, non_Offensive = svm_model_he.classify_DB(filepath)

    elif model_name == 'BERT for Arabic':
        print('in the BERT BERT for Arabic')
        os.system('python load_arabic_bert.py 2 '+filepath)
        print('Before reading the result file \n\n\n\n\n')
        result_file = pd.read_csv('result.csv')
        offensive_count, non_Offensive = result_file['res'].iloc[1], result_file['res'].iloc[0]
    result = "The number of neutral = " + str(non_Offensive) + ", the number of Offensive " + str(offensive_count) 
    # removing the file from the server
    print('remove file - ', filepath)
    os.remove(filepath)
    '''
    return render_template('prediction.html', result=result)





@app.route("/")
def index():
    return render_template('index.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/ClassifyText', methods=['POST'])
def ClassifyText():
    model_name = request.form['model_name']
    tweet_content = request.form['tweet_content']
    
    if model_name == 'Hebrew':
        svm_model_he = joblib.load("finalized_model_he.sav")
        vectorizer_he = joblib.load("vectorizer_he.sav")
        #print(tweet_content)
        result = SVMHE.predict(tweet_content,svm_model_he,vectorizer_he)
        result = 'Not Offensive' if (result == [0]) else 'Offensive'

    if model_name == 'Arabic':
        #print(tweet_content)
        svm_model_ar = joblib.load("arabic.sav")
        vectorizer_ar = joblib.load("arvectorizer.sav")
        result = SVMAR.predict(tweet_content,svm_model_ar,vectorizer_ar)
        result = 'Not Offensive' if (result == [0]) else 'Offensive'

    res = 'The tweet ' + str(tweet_content) + ' is ' + str(result)
    return render_template('prediction.html', result=res)



@ app.route('/classifyProfile', methods=['POST'])
def classifyProfile():
    profile_name = request.form['profile_name']
    filepath = ap.get_tweets(profile_name)
    print(filepath)
    model_name = request.form['model_name']

    if model_name == 'Hebrew':
        offensive_count, non_Offensive = svm_model_he.classify_DB(filepath)

    elif model_name == 'Arabic':
        os.system('python load_arabic_bert.py 2 '+ filepath)
        result_file = pd.read_csv('result.csv')
        offensive_count, non_Offensive = result_file['res'].iloc[1], result_file['res'].iloc[0]

    result ='The number of neutral = '+str(non_Offensive) + ', the number of Offensive ' + str(offensive_count)

    print('remove file - ', filepath)
    os.remove(filepath)
    return render_template('prediction.html', result=result)

    # --------------------- End Writing -----------------------------


@ app.route('/classifyDB', methods=['POST'])
def classifyDB():
    target = os.path.join(APP_ROOT, 'uploads\\')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print('*************** After if ***************')
    destination=''
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        
        print('******************************')
        print(destination)
        print(filename)
        print('******************************')

        file.save(destination)
    print(destination)   
    return clssifydatabase(destination) # run the models on the uploaded model

svm_model_he=None
vectorizer_he=None
svm_model_ar=None
vectorizer_ar=None

def load_he_svm_model():
    # Load Hebrew - SVM model
    svm_model_he = joblib.load("finalized_model_he.sav")
    vectorizer_he = joblib.load("vectorizer_he.sav")
    # Load Arabic - SVM model
    svm_model_ar = joblib.load("arabic.sav")
    vectorizer_ar = joblib.load("arvectorizer.sav")
    return svm_model_he,vectorizer_he,svm_model_ar,vectorizer_ar

if __name__ == '__main__':
    svm_model_he,vectorizer_he,svm_model_ar,vectorizer_ar = load_he_svm_model()
    app.run(debug=True)
