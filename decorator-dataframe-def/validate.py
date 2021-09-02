import pandas as pd


def default_enable():
    return True


class ValidationException(Exception):

    def __init__(self, message):
        super(ValidationException, self).__init__(message)


class df_def:

    def __init__(self, description, col_defs, all_col_defined=True):
        self.description = description
        self.col_defs = col_defs
        self.all_col_defined = all_col_defined

    def get_columns(self):
        return [c.name for c in self.col_defs]


class col_def:

    class col_dtype:

        def __init__(self, name, is_dtype):
            self.name = name
            self.is_dtype = is_dtype

    from pandas.api.types import is_float_dtype, is_string_dtype, is_integer_dtype, is_datetime64_dtype, is_bool_dtype

    int = col_dtype('int', is_integer_dtype)
    float = col_dtype('float', is_float_dtype)
    string = col_dtype('string', is_string_dtype)
    datetime = col_dtype('datetime', is_datetime64_dtype)
    bool = col_dtype('bool', is_bool_dtype)

    def __init__(self, name, col_dtype, description='', unit='', nullable=True, example=''):
        self.name = name
        self.col_dtype = col_dtype
        self.description = description
        self.unit = unit
        self.nullable = nullable
        self.example = example

        if (col_dtype == int) & nullable:
            raise Exception('Integer column cannot store NaN values')


class InputOutputValidator:
    def _is_empty(self, df):
        if df is None:
            return True
        return df.empty

    def _validate_df(self, df, name, df_def):
        if self._is_empty(df) or df_def is None:
            return
        expectecd_cols = df_def.get_columns()
        missing = [c for c in expectecd_cols if c not in df.columns]
        if len(missing) > 0:
            raise ValidationException(
                'Required column(s) missing from {} dataframe: {}'.format(name, missing))

        if df_def.all_col_defined:
            col_not_defined = [c for c in df.columns if c not in expectecd_cols]
            if len(col_not_defined) > 0:
                raise ValidationException(
                    'The following column(s) are not defined for {} dataframe : {}'.format(name, col_not_defined))

        for c in df_def.col_defs:
            col_name = c.name
            expected_dtype = c.col_dtype
            actual_dtype = df[col_name].dtype
            if not expected_dtype.is_dtype(actual_dtype):
                raise ValidationException('Column {} is type {} but expected to be of type {}'.format(col_name, actual_dtype, expected_dtype.name))
            if c.nullable is not None and not c.nullable:
                if df[col_name].isnull().any():
                    raise ValidationException('Column {} cannot have null values'.format(col_name))

    def _validate_input(self, *args):
        raise Exception('Not Implemented')

    def __call__(self, func):
        def validate(*args, **kwargs):
            if self._enable():
                args_df = list()
                for a in args:
                    if isinstance(a, pd.DataFrame):
                        args_df.append(a)
                self._validate_input(args_df)

            result = func(*args, **kwargs)

            if self._enable():
                self._validate_df(df=result, name='output', df_def=self._output_df_def)
            return result

        return validate


class DataFrameDefinitions(InputOutputValidator):

    def __init__(self, input_df_def=None, output_df_def=None, df_input_index=0, enable=default_enable):
        self._input_df_def = input_df_def
        self._output_df_def = output_df_def
        self._df_input_index = df_input_index
        self._enable = enable

    def _validate_input(self, args):
        input_df = args[self._df_input_index]
        self._validate_df(df=input_df, name='input', df_def=self._input_df_def)


class DataFrameDefinitionsMultipleInputs(DataFrameDefinitions):
    def __init__(self, input_df_def=None, output_df_def=None, enable=default_enable):
        self._input_df_def = input_df_def
        self._output_df_def = output_df_def
        self._enable = enable

    def _validate_input(self, args):
        if self._input_df_def is not None:
            for i in range(len(self._input_df_def)):
                input_df = args[i]
                self._validate_df(df=input_df, name='Input {}'.format(i), df_def=self._input_df_def[i])