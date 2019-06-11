import pymongo
from pandas import DataFrame
from typing import Callable


class Session:
    def __init__(self, host:str, port:str, user:str, password:str,
                 database_name:str, collection_name:str, ssl=False):
        """
        Constructs a session given the database connection parameters
        :param host: Database host
        :param port: Database port
        :param user: Database user
        :param password: Database password
        :param database_name: Database name
        :param collection_name: Collection name
        :param ssl: True if SSL is required
        """
        uri = "mongodb://" + user + ":" + password + "@" + host + ":" + port
        if ssl:
            uri = uri + "?ssl=" + ssl
        self._client = pymongo.MongoClient(uri)
        self._db = self._client[database_name]
        self._collection = self._db[collection_name]

    def insert(self, data:DataFrame, to_dict_list: Callable):
        """
        Insert new documents given the data

        :param data: data to insert as a dataframe
        :param to_dict_list: function to tranform dataframe into a list of JSON
        :return: Do nothing if data is empty
        """
        if len(data) == 0:
            return
        self._collection.insert_many(to_dict_list(data))

    def find(self, db_filter:dict):
        """
        Find the documents matching the given filter
        :param db_filter: filter as a dict
        :return: a dataframe containing the matching documents
        """
        return DataFrame(list(self._collection.find(db_filter)))

    def delete(self, db_filter:dict):
        """
        Delete the documents matching the given filter

        :param db_filter: filter as a dict
        """
        self._collection.delete_many(db_filter)

    def delete_all(self):
        """
        Delete all documents from collection
        """
        self.delete({})

