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
        if i["label"] == "Bullish": #Positive
            k = 2
        if i["label"] == "Bearish": #Negative
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
    sqlite_select_query = "SELECT * FROM 'news' WHERE language='en' LIMIT 0, 10"
    df_news = pd.read_sql(sqlite_select_query, db)
    db.close()
    return df_news

class Sentiment():
    def __init__(self, tf_idf=True, bert=True ):
        if tf_idf:
            # loading config params
            project_root: Path = get_project_root()
            with open(str(project_root / "config.yml")) as f:
                params = yaml.load(f, Loader=yaml.FullLoader)
            self.model_tf_idf = load_model(params["model"]["path_to_model"])
        if bert:
            model_name = "ElKulako/cryptobert"
            tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
            self.model_bert = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
            self.pipe_bert = TextClassificationPipeline(model=self.model_bert, tokenizer=tokenizer, max_length=64,
                                              truncation=True, padding='max_length', top_k=None)

    def do_sentiment_analysis(self, news):
        """
        Crypro-sentimental  tf-idf
        0: Negative
        1: Neutral
        2: Positive
        """
        if hasattr(self, "model_tf_idf"):
            self.sentiment_tf_idf = model_inference(self.model_tf_idf, news)
            for k in self.sentiment_tf_idf:
                self.sentiment_tf_idf[k] = round(self.sentiment_tf_idf[k], 2)

        if hasattr(self, "model_bert"):
            self.sentiment_bert =mod_BERT_result(self.pipe_bert(news))
            for k in self.sentiment_bert:
                self.sentiment_bert[k] = round(self.sentiment_bert[k], 2)
        if hasattr(self, "sentiment_bert") and hasattr(self, "sentiment_tf_idf"):
            result = list(zip(["Negative:", "Neutral:", "Positive"],
                              [self.sentiment_tf_idf[0], self.sentiment_tf_idf[1], self.sentiment_tf_idf[2]],
                              [self.sentiment_bert[0], self.sentiment_bert[1], self.sentiment_bert[2]]))
            return result
        if hasattr(self, "sentiment_bert"):


            return self.sentiment_bert
        if hasattr(self, "sentiment_tf_idf"):
            return self.sentiment_tf_idf
        else:
            return {0: 0, 1: 0, 2: 1}






def get_sentiment(news):

    sentiment = Sentiment(tf_idf=True, bert=True)
    answer = sentiment.do_sentiment_analysis(news)

    return answer


if __name__=="__main__":
    # time_start = time.time()
    #
    # print("Check sentimental analyis")
    #
    # # loading config params
    # project_root: Path = get_project_root()
    # with open(str(project_root / "config.yml")) as f:
    #     params = yaml.load(f, Loader=yaml.FullLoader)
    # model = load_model(params["model"]["path_to_model"])
    #
    # model_name = "ElKulako/cryptobert"
    # tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    # model2 = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
    # pipe = TextClassificationPipeline(model=model2, tokenizer=tokenizer, max_length=64,
    #                                   truncation=True, padding='max_length', top_k=None)
    #
    # df = get_news()
    #
    # for i in df.iterrows():
    #     a = model_inference(model, i[1].title)
    #     b =  pipe(i[1].title)
    #     print(i[0], "\t",  i[1].title, "\t", a, "\t", mod_BERT_result(b))
    #
    # print(time.time()-time_start)
    df = get_news()
    for i in df.iterrows():
        print(i[1].title, get_sentiment(i[1].title))
        #print(get_sentiment(i[1].title))