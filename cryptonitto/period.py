import datetime
import matplotlib.dates as mdates

class Period():
    def __init__(self, b, e):
        assert (isinstance(b, datetime.datetime))
        self.begin = b
        if e is None:
            self.end = b
        else:
            assert (isinstance(e, datetime.datetime))
            if e >= b:
                self.end = e
            else:
                self.end = b
                self.end = e


    def conv_to_data(self, data):
        """
        вспомогтаельная функция, в которой задан формат визуализации даты
        :param data:
        :return:
        """
        return data.strftime("%Y/%m/%d")

    def get_data_format_begin(self):
        return self.conv_to_data(self.begin)

    def get_data_fromat_end(self):
        return self.conv_to_data(self.end)

