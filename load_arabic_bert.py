from simpletransformers.classification import ClassificationModel
import pandas as pd
import sys

import ReadSheetsFiles as rsf

x = {"reprocess_input_data": True,
     "fp16": False,
     "num_train_epochs": 4,
     "use_cuda": False}

model = ClassificationModel(
    "bert", "outputsArabic/",
    num_labels=2,
    args=x,
    use_cuda=False
)


def predictSingleTweet(text=None):
    if text == None:
        text = rsf.readFileFunction("text.csv").drop(axis=0, columns="Unnamed: 0")
        text = text.iloc[0, 0]
    l = []
    l.append(text)
    result = model.predict(l)
    res = pd.DataFrame(result, columns=['val'])
    res.to_csv("result.csv")
    return res

    # ------------------------------------------------


def classify_DB(filepath):
    print("in the classify DB ---------\n" + sys.argv[2] + "\n-----------------")
    print('Loading Database')
    db = rsf.readFileFunction(filepath)
    # db = pd.read_excel(filepath)
    print('before loading the pandas list')
    print('End loading')
    counter = 0  # the counter will give us the number of racist tweets

    # len(db) - count = the number of neutral tweets
    db_length = len(db)
    # l = []
    # print('after loading the pandas list')

    # for i in range(0, db_length):
    #     l.append(db['info'].iloc[i])
    list1=db.iloc[0:,0].tolist()
    # List1=[]
    # for i in l:
    #     List1.append(i)
    # print(List1)
    print(list1)
    c = model.predict(list1)
    print('after predict BERT')
    counter = sum(c[0])


    print('the number of neutral tweets in the Database = ', counter,
          '\n the number of racist tweets in the Database = ', db_length - counter)
    l = [counter, db_length - counter]
    p = pd.DataFrame(l, columns=['res'])
    p.to_csv("result.csv")
    return l

# ----------------- ----------------- -----------------

def printClear():
    for i in range(7):
        print('***\n')


# if __name__ == "__main__":
#     if sys.argv[1] == '1':
#         predictSingleTweet()
#         # print(predictSingleTweet())
    
#     if sys.argv[1] == '2':
#         print("in the if ---------\n" + sys.argv[2] + "\n-----------------")
#         print(classify_DB(sys.argv[2]))
    
#     if sys.argv[1] == '3':
#         printClear()
#         print("In the main ____ arg[1] = 3 ")
#         l=classify_DB(sys.argv[2])
#         printClear()
#         print(l)

