import joblib
import ReadSheetsFiles as rsf
import re
import string
import pandas as pd


def load_svm_model():
    # Load SVM model
    #                    server\\src\\models\\finalized_model.sav
    model = joblib.load("arabic.sav")
    vectorizer = joblib.load("arvectorizer.sav")
    return model, vectorizer

# -----------------------------------  Preprocessing -------------------------------------


def clean(df):
    df = remove_diacritics(df)
    df = normalize_arabic(df)
    df = remove_punctuations(df)
    df = remove_repeating_char(df)
    df = remove_english_word_and_numbers(df)
    df = clean_space(df)
    return df


arabic_punctuations = '''`÷« »×؛<>٩٨'٧٦٥٤٣٢١٠_()↗*•&^%][ـ،/:"؟.,'{}⋮≈~¦+|٪!”…“–ـ/[]%=#*+\\•~@£·_{}©^®`→°€™›♥←×§″′Â█à…“★”–●â►−¢¬░¶↑±▾	═¦║―¥▓—‹─▒：⊕▼▪†■’▀¨▄♫☆é¯♦¤▲è¸Ã⋅‘∞∙）↓、│（»，♪╩╚³・╦╣╔╗▬❤ïØ¹≤‡₹´'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations

arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)


def remove_diacritics(df):
    df['Tweet'] = df['Tweet'].apply(lambda x: _remove_diacritics(x))
    return df


def _remove_diacritics(x):
    x = str(x)
    x = re.sub(arabic_diacritics, '', x)
    return x


def normalize_arabic(df):
    df['Tweet'] = df['Tweet'].apply(lambda x: _normalize_arabic(x))
    return df


def _normalize_arabic(x):
    x = str(x)
    # added space around puncts after replace
    x = re.sub("[إأآا]", "ا", x)
    x = re.sub("ى", "ي", x)
    x = re.sub("ؤ", "ء", x)
    x = re.sub("ئ", "ء", x)
    x = re.sub("ة", "ه", x)
    x = re.sub("گ", "ك", x)
    return x


def remove_punctuations(df):
    df['Tweet'] = df['Tweet'].apply(lambda x: _remove_punctuations(x))
    return df


def _remove_punctuations(x):
    x = str(x)
    # translator = str.maketrans(' ', ' ', punctuations_list)
    translator = str.maketrans(punctuations_list, ' '*len(punctuations_list))
    return x.translate(translator)


def remove_repeating_char(df):
    df['Tweet'] = df['Tweet'].apply(lambda x: _remove_repeating_char(x))
    return df


def _remove_repeating_char(x):
    x = str(x)
    return re.sub(r'(.)\1+', r'\1', x)


def remove_english_word_and_numbers(df):
    df['Tweet'] = df['Tweet'].apply(
        lambda x: _remove_english_word_and_numbers(x))
    return df


def _remove_english_word_and_numbers(x):
    x = str(x)
    return re.sub(r'[a-zA-Z0-9]+', '', x)


def clean_space(df):
    compiled_re = re.compile(r"\s+")
    df['Tweet'] = df["Tweet"].apply(lambda x: _clean_space(x, compiled_re))
    return df


def _clean_space(x, compiled_re):
    return compiled_re.sub(" ", x)

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


# -----------------------------------  End Preprocessing -------------------------------------


def predict(text):
    df = []
    df.append(text)
    df = pd.DataFrame(df, columns=['Tweet'])
    text = clean(df)
    text = remove_emoji(text['Tweet'].iloc[0])
    if len(text.split()) < 1:
        return [0] 
    vec = vectorizer.transform([text]).toarray()
    print(text)
    answer = model.predict(vec)
    # if(answer[0]==1):
    print(answer)
    return answer

def classify_DB(filepath):
    print('Loading Database')
    db = rsf.readFileFunction(filepath) # read file function - more general - it works according to the file (excel or csv)
    print('End loading')
    counter = 0 # the counter will give us the number of racist tweets
                # len(db) - count = the number of neutral tweets
    list=db.iloc[0:,0]
    db_length = len(list)
    for text in list:
        c=predict(text)
        counter += c[0]
    print('the number of offensive tweets in the Database = ',counter, '\n the number of neutral tweets in the Database = ' , db_length - counter)

    return counter, db_length - counter


# model, vectorizer = load_svm_model()