import datetime
import prophet

class ForecastModel():
    """
    Данный класс преданзначен для вычисления прогноза по готовой модели
    Возможны несколько способов загузки модели
    """
    def __init__(self, symbol, date=datetime.datetime.now()):
        self.date = date
        self.date = symbol





