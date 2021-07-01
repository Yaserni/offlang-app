import pandas as pd
import os
from flask import Flask, render_template, request
import absorbProfile as ap  # abosrbProfile - in order to absort tweets from profile
import SVM_model_hebrew as svm_model_he
import ReadSheetsFiles as rsf
import pandas as pd

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
global arabicBert 
def clssifydatabase(filepath):
    print(filepath)
    model_name = request.form['model_name']

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
    return render_template('prediction.html', result=result)


def make_BERT_Predict(text,lang):
    print(text)
    data = pd.DataFrame(text)
    data.to_csv("text.csv")
    if lang == 'ar':
        os.system('python load_arabic_bert.py 1')
    # os.remove('text.csv')
    # os.remove('text.csv')


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
    
    if model_name == 'SVM for Hebrew':
        result = svm_model_he.predict(tweet_content)
        result = 'Not Offensive' if (result == 0) else 'Offensive'
    
   
    
    res = 'the tweet ' + str(tweet_content) + ' is ' + str(result)
    return render_template('prediction.html', result=res)

# get tweets from Profile

@ app.route('/classifyProfile', methods=['POST'])
def classifyProfile():
    profile_name = request.form['profile_name']
    filepath = ap.get_tweets(profile_name)
    print(filepath)
    model_name = request.form['model_name']

    if model_name == 'SVM for Hebrew':
        offensive_count, non_Offensive = svm_model_he.classify_DB(filepath)

    elif model_name == 'BERT for Arabic':
        os.system('python load_arabic_bert.py 2 '+ filepath)
        result_file = pd.read_csv('result.csv')
        # os.remove('result.csv')
        offensive_count, non_Offensive = result_file['res'].iloc[1], result_file['res'].iloc[0]

    result ='The number of neutral = '+str(non_Offensive) + ', the number of Offensive ' + str(offensive_count)

    # removing the file from the server
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
    
    # Rewrite the csv file 
    # df = rsf.readFileFunction(destination)

    # df.to_excel(destination.split('.')[0]+'.xlsx')   
    # print("The Rewriting process done") 
    # print(destination.split('.')[0]+'.xlsx')
    
    return clssifydatabase(destination) # run the models on the uploaded model






if __name__ == '__main__':
    app.run()
   #app.run()
