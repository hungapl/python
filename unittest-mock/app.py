import pandas as pd


class MyException(Exception):
    def msg(self):
        return 'an exception occurred'


class Dao:

    def __init__(self, csv_file:str):
        self.csv_file = csv_file

    def load_data(self, limit=10):
        return pd.read_csv(self.csv_file)[:limit]


class Processor:
    def __init__(self, dao:Dao):
        self.dao = dao

    def process(self):
        """
            Provide a sum of the score columns of the data frame loaded using the given dao
        :return: sum of scores
        """
        df = self.dao.load_data(5)
        return df.score.sum()
