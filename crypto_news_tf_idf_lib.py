
import time
import os
import yaml
import pickle
from pathlib import Path

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




class Sentiment():
    def __init__(self):
        project_root: Path = get_project_root()
        with open(str(project_root / "config.yml")) as f:
            params = yaml.load(f, Loader=yaml.FullLoader)

        path_to_model = params["model"]["path_to_model"]

        if os.path.split(os.getcwd())[1] == "telebot":
            path_to_model = os.path.join("..", path_to_model)

        self.model_tf_idf = load_model(path_to_model)


    def do_sentiment_analysis(self, news):
        """
        Crypro-sentimental  tf-idf
        0: Negative
        1: Neutral
        2: Positive
        """


        if hasattr(self, "model_tf_idf"):

            predict = self.model_tf_idf.predict_proba([news])
            data = {}

            for i, pred in enumerate(predict.squeeze()):
                 data[i] = round(pred, 2)

        return data







if __name__ == "__main__":
    sentiment = Sentiment()
    news = "There is positive news about bitcoin"
    time_start = time.time()
    a = sentiment.do_sentiment_analysis(news)
    print(a)
    print(time.time() - time_start)
