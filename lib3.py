# В библиотеке будут собраны функции NLP для определения настроения новости.
import sqlite3
import pandas as pd
import yaml
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

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

if __name__=="__main__":
    print("Check sentimental analyis")

    # loading config params
    project_root: Path = get_project_root()
    with open(str(project_root / "config.yml")) as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    model = load_model(params["model"]["path_to_model"])
    df = get_news()

    for i in df.iterrows():
        a = model_inference(model, i[1].title)
        print(i[0],"\t",  i[1].title, "\t", a)