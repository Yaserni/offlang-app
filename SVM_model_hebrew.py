import os
import ReadSheetsFiles as rsf
import re
import pandas as pd
import joblib




# -----------------------------------  Preprocessing -------------------------------------


def clean(df):
    # remove 
    df["Post"]=df["Post"].apply(lambda x :re.sub(r'[^א-ת]+',' ',x))
    df = delete_Stop_Words(df)
    df = remove_repeating_char(df)
    df = remove_spaces(df)
    return df


stop_word=['אני', 'את', 'אתה', 'אנחנו', 'אתן', 'אתם', 'הם', 'הן', 'היא', 'הוא', 'שלי', 'שלו', 'שלך', 'שלה', 'שלנו', 'שלכם', 'שלכן', 'שלהם', 'שלהן', 'לי', 'לו', 'לה', 'לנו', 'לכם', 'לכן', 'להם', 'להן', 'אותה', 'אותו', 'זה', 'זאת', 'אלה', 'אלו', 'תחת', 'מתחת', 'מעל', 'בין', 'עם', 'עד', 'נגר', 'על', 'אל', 'מול', 'של', 'אצל', 'כמו', 'אחר', 'אותו', 'בלי', 'לפני', 'אחרי', 'מאחורי', 'עלי', 'עליו', 'עליה', 'עליך', 'עלינו', 'עליכם', 'לעיכן', 'עליהם', 'עליהן', 'כל', 'כולם', 'כולן', 'כך', 'ככה', 'כזה', 'זה', 'זות', 'אותי', 'אותה', 'אותם', 'אותך', 'אותו', 'אותן', 'אותנו', 'ואת', 'את', 'אתכם', 'אתכן', 'איתי', 'איתו', 'איתך', 'איתה', 'איתם', 'איתן', 'איתנו', 'איתכם', 'איתכן', 'יהיה', 'תהיה', 'היתי', 'היתה', 'היה', 'להיות', 'עצמי', 'עצמו', 'עצמה', 'עצמם', 'עצמן', 'עצמנו', 'עצמהם', 'עצמהן', 'מי', 'מה', 'איפה', 'היכן', 'במקום שבו', 'אם', 'לאן', 'למקום שבו', 'מקום בו', 'איזה', 'מהיכן', 'איך', 'כיצד', 'באיזו מידה', 'מתי', 'בשעה ש', 'כאשר', 'כש', 'למרות', 'לפני', 'אחרי', 'מאיזו סיבה', 'הסיבה שבגללה', 'למה', 'מדוע', 'לאיזו תכלית', 'כי', 'יש', 'אין', 'אך', 'מנין', 'מאין', 'מאיפה', 'יכל', 'יכלה', 'יכלו', 'יכול', 'יכולה', 'יכולים', 'יכולות', 'יוכלו', 'יוכל', 'מסוגל', 'לא', 'רק', 'אולי', 'אין', 'לאו', 'אי', 'כלל', 'נגד', 'אם', 'עם', 'אל', 'אלה', 'אלו', 'אף', 'על', 'מעל', 'מתחת', 'מצד', 'בשביל', 'לבין', 'באמצע', 'בתוך', 'דרך', 'מבעד', 'באמצעות', 'למעלה', 'למטה', 'מחוץ', 'מן', 'לעבר', 'מכאן', 'כאן', 'הנה', 'הרי', 'פה', 'שם', 'אך', 'ברם', 'שוב', 'אבל', 'מבלי', 'בלי', 'מלבד', 'רק', 'בגלל', 'מכיוון', 'עד', 'אשר', 'ואילו', 'למרות', 'אס', 'כמו', 'כפי', 'אז', 'אחרי', 'כן', 'לכן', 'לפיכך', 'מאד', 'עז', 'מעט', 'מעטים', 'במידה', 'שוב', 'יותר', 'מדי', 'גם', 'כן', 'נו', 'אחר', 'אחרת', 'אחרים', 'אחרות', 'אשר', 'או']

def delete_Stop_Words(data):
    data['Post'] = data['Post'].apply(lambda x: ' '.join([t for t in x.split() if t not in stop_word]))
    return data

def remove_repeating_char(data):
    data['Post'] = data['Post'].apply(lambda x: _remove_repeating_char(x))
    return data
    
def _remove_repeating_char(x):
    x = str(x)
    return re.sub(r'(.)\1+', r'\1', x)

def remove_spaces(data):
    data["Post"]=data["Post"].apply(lambda x:' '.join(x.split()))
    return data


# -----------------------------------  End Preprocessing -------------------------------------

def predict(text):
    df = []
    df.append(text)
    df = pd.DataFrame(df, columns=['Post'])
    text = clean(df)
    text = text['Post'].iloc[0]
    if len(text.split()) < 1:
        return [0] 

    vec = vectorizer.transform([text]).toarray()
    answer = model.predict(vec)
    return answer

def classify_DB(filepath):
    db = rsf.readFileFunction(filepath) # read file function - more general - it works according to the file (excel or csv)
    counter = 0 # the counter will give us the number of racist tweets
                # len(db) - count = the number of neutral tweets
    list=db.iloc[0:,0] # all sentences 
    db_length = len(list)
    classifiedList = []
    for text in list:
        c=predict(text)
        counter += c[0]
        classifiedList.append(c[0])
    df = pd.DataFrame(data=[])
    df['sentence']=list
    df['offensive']=classifiedList
    df.to_excel(F'uploads/class.xlsx',index=False)
    os.remove(filepath)
    return counter, db_length - counter

def load_svm_model():
    # Load SVM model
    model = joblib.load("finalized_model_he.sav")
    vectorizer = joblib.load("vectorizer_he.sav")
    return model, vectorizer

model, vectorizer = load_svm_model()