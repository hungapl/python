import unittest
from unittest.mock import patch, Mock

import pandas as pd

import app

test_data = pd.DataFrame({'name': ['Bob', 'Amy'], 'score':[10, 20]})


class AppTest(unittest.TestCase):

    @patch('app.Dao')
    def test_run(self, dao:app.Dao):
        """
            Test processor is summing the score column when process is called
        """
        dao.load_data.return_value = test_data
        p = app.Processor(dao)
        results = p.process()

        dao.load_data.assert_called_with(5)
        self.assertEqual(sum(test_data.score), results)

    @patch('app.Dao')
    def test_dao_throws_exception_expect_process_propagate_exception(self, dao:app.Dao):
        """
            Test process method returns -1 upon exception
        """
        dao.load_data = Mock(side_effect=Exception('some exception'))
        p = app.Processor(dao)

        with self.assertRaises(Exception):
            self.assertEqual(-1, p.process())
