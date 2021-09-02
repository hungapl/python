import numpy as np
import pandas as pd

from validate import DataFrameDefinitions, col_def, df_def, ValidationException
import unittest
from datetime import datetime


@DataFrameDefinitions(input_df_def=df_def(description='Person data',
                                          col_defs=[
                                              col_def(name='id', col_dtype=col_def.int, description='ID of user', nullable=False),
                                              col_def(name='score', col_dtype=col_def.float, description='Score range from 0 to 100', nullable=False),
                                              col_def(name='weight', col_dtype=col_def.float, description='Weight', unit='kilogram'),
                                              col_def(name='time', col_dtype=col_def.datetime, description='Start time', nullable=False)
                                          ]),
                      output_df_def=df_def(description='Activities of a person',
                                           col_defs=[
                                               col_def(name='activity', col_dtype=col_def.string, description='Activity - [Walking, Running, Resting]', nullable=False)
                                           ]))
def example_function(df):
    return pd.DataFrame({'activity': ['Walking']})


class TestInputOutput(unittest.TestCase):

    def test_input_output_when_df_is_correct_expect_no_exception(self):
        df_input = pd.DataFrame({'id': [1, 2], 'score': [10.0, 20.0], 'weight': [np.nan, 50.0], 'time': [datetime(2012, 9, 16, 0, 0), datetime(2012, 9, 16, 0, 0)]})
        example_function(df_input)

    def test_input_output_when_df_has_col_has_unexpected_col_type_expect_exception_thrown(self):
        # Use float numbers as ID
        df_input = pd.DataFrame({'id': [1.0, 2.0], 'score': [10.0, 20.0], 'weight': [np.nan, 50.0], 'time': [datetime(2012, 9, 16, 0, 0), datetime(2012, 9, 16, 0, 0)]})
        with self.assertRaises(ValidationException) as e:
            example_function(df_input)

    def test_input_output_when_df_has_null_for_nonnullable_cols_expect_exception_thrown(self):
        # Score column has NaN value
        df_input = pd.DataFrame({'id': [1, 2], 'score': [10.0, np.nan], 'weight': [np.nan, 50.0], 'time': [datetime(2012, 9, 16, 0, 0), datetime(2012, 9, 16, 0, 0)]})
        with self.assertRaises(ValidationException) as e:
            example_function(df_input)