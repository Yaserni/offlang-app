import pandas as pd

def predict(text,model,vectorizer):
    df = []
    df.append(text)
    df = pd.DataFrame(df, columns=['Post'])
    text = clean(df)
    text = text['Post'].iloc[0]
    if len(text.split()) < 2:
        return [0] 

    vec = vectorizer.transform([text]).toarray()
    print(vec.shape)
    answer = model.predict(vec)
    if(answer[0]==1):
        print(text)
    return answer
