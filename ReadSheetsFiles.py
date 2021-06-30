import pandas as pd

def readFileFunction(path):
    # result = None
    filepath = path.split('.')
    end=filepath[-1]
    if end == 'csv':
        return pd.read_csv(path)
    if end == 'xlsx':
        return pd.read_excel(path)
    
    



def isEmptyText(text):
    if text == None or text == "":
        return True
    return False

def checkFile(path):
    end = path.split(".")[1]
    if end == 'csv' or end =='xlsx' or end == 'xls':
        return True
    else:
        return False
        
    
