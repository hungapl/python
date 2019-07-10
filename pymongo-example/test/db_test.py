import unittest
import pandas as pd
import pprint
from datetime import datetime
from db import Session

host = 'localhost'
port = "27017"
user = 'test'
password = 'test'
database_name = 'testdb'
collection_name = 'col1'

FIELD_ENTITY_ID = 'entityId'
FIELD_TIME_OCCURRED = 'timeOccurred'
FIELD_DATA = 'data'

test_data = pd.DataFrame({
    FIELD_ENTITY_ID: ["Brisbane", "Melbourne"],
    FIELD_TIME_OCCURRED: [datetime(2020, 6, 1), datetime(2020, 6, 1)],
    FIELD_DATA: [13, 7]})


def to_dict_list(df):
    return [{FIELD_ENTITY_ID: entityId,
         FIELD_TIME_OCCURRED: timeOccurred,
         FIELD_DATA: data} for entityId, timeOccurred, data in zip(df.entityId, df.timeOccurred, df.data)]


def db_filter(entity_id: str, time_occurred_start: datetime, time_occurred_end: datetime):
    return {FIELD_ENTITY_ID: {"$eq": entity_id}, FIELD_TIME_OCCURRED: {'$gte': time_occurred_start,
                                                                       '$lte': time_occurred_end}}


def pp(comment, results):
    print()
    print(comment + ':')
    for item in results:
        pprint.pprint(item)
    print()
    print()


class DbTestCase(unittest.TestCase):
    def setUp(self):
        self._session = Session(host=host, port=port, user=user, password=password,
                    database_name=database_name, collection_name=collection_name)
        self._session.delete_all()  # reset database
        assert len(self._session.find({})) == 0

    def _insert_test_data(self):
        self._session.insert(test_data, to_dict_list=to_dict_list)

    def test_session_insert_empty_list(self):
        self._session.insert([], to_dict_list=to_dict_list)
        self.assertEqual(len(self._session.find({})), 0)

    def test_session_insert_and_find(self):
        self._session.insert(test_data, to_dict_list=to_dict_list)
        results_df = self._session.find({})
        self.assertEqual(2, len(results_df))
        self.assertTrue(test_data[['entityId', 'timeOccurred', 'data']]
                        .equals(results_df[['entityId', 'timeOccurred', 'data']]))

        results_df = self._session.find({FIELD_ENTITY_ID: 'Brisbane'})
        self.assertEqual(1, len(results_df))
        self.assertTrue(test_data.head(1)[['entityId', 'timeOccurred', 'data']]
                        .equals(results_df[['entityId', 'timeOccurred', 'data']]))


if __name__ == '__main__':
    unittest.main()