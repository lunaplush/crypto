# В библиотеке будут собраны функции NLP для определения настроения новости.
#https://github.com/crypto-sentiment/crypto_sentiment_tfidf_logreg_streamlit
import sqlite3
import time

import pandas as pd
import yaml
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer

"""
0 - Negative
1 - Neutral
2 - Positive

"""
def get_project_root() -> Path:
    return Path(__file__).parent


# loading the model into memory
def load_model(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def mod_BERT_result(b):
    b1 = {}
    for i in b[0]:
        if i["label"] == 'Neutral':
            k = 1
        if i["label"] == "Bullish":
            k = 2
        if i["label"] == "Bearish":
            k = 0
        b1[k] = i["score"]
    return b1
def model_inference(model, input_text):

    pred = model.predict_proba([input_text])

    pred_dict = {}
    for i, pred in enumerate(pred.squeeze()):
        pred_dict[i] = pred

    return pred_dict

def get_news():
    db = sqlite3.connect("db/news.sqlite")
    sqlite_select_query="SELECT * FROM 'news' WHERE language='en' LIMIT 0, 10"
    df_news = pd.read_sql(sqlite_select_query, db)
    db.close()
    return df_news

def get_sentiment(news):
    pass
    return 1


if __name__=="__main__":
    time_start = time.time()

    print("Check sentimental analyis")

    # loading config params
    project_root: Path = get_project_root()
    with open(str(project_root / "config.yml")) as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    model = load_model(params["model"]["path_to_model"])

    model_name = "ElKulako/cryptobert"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model2 = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
    pipe = TextClassificationPipeline(model=model2, tokenizer=tokenizer, max_length=64,
                                      truncation=True, padding='max_length', top_k=None)

    df = get_news()

    for i in df.iterrows():
        a = model_inference(model, i[1].title)
        b =  pipe(i[1].title)
        print(i[0], "\t",  i[1].title, "\t", a, "\t", mod_BERT_result(b))

    print(time.time()-time_start)