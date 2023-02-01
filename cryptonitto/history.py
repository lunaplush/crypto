import pandas as pd
from period import Period

class History():

    def __init__(self, period:Period ):
        self.name = "History"

    def get(self):
        pass



class HistoryCryptoCurrency(History):
    def __init__(self):
        super(HistoryCryptoCurrency, self).__init__()
       # self.df = pd.DataFrame([[112, 213, 13], [71, 14, 12]], columns=["a", "b", "b"])
        self.name = "HistoryCryptoCurrency"

    def __init__(self, name):
        super(HistoryCryptoCurrency, self).__init__()
        self.name ="New Name"

    def print_info(self):
        print(self.name)
    def get(self):
        return self.df

class Ura():
    def __init__(self):
        self.name = "Ura"

if __name__ == "__main__":
    a = History()
    b = HistoryCryptoCurrency("TTT")
    print(a.get())
    print(b.get())
    b.print_info()
    c = Ura()
    History.prtin_info(c)
    print(b.riga)
