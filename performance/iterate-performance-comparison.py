import numpy as np
import pandas as pd
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        kw['log_time'].append(int((te - ts) * 1000))
        return result

    return timed


def my_compute(x):
    return x + 1


@timeit
def use_for_loop_loc(dataset, **kwargs):
    """ Use panda loc() function to retrieve and assign values"""
    dataset['b'] = np.nan
    for i in range(len(dataset)):
        dataset.loc[i, 'b'] = my_compute(dataset.loc[i, 'a'])


@timeit
def use_for_loop_at(dataset, **kwargs):
    """ Use panda at() function to retrieve and assign value"""
    dataset['b'] = np.nan
    for i in range(len(dataset)):
        dataset.at[i, 'b'] = my_compute(dataset.at[i, 'a'])


@timeit
def use_for_loop_iat(dataset, **kwargs):
    """ Use panda iat() function to retrieve and assign value"""
    dataset['b'] = np.nan
    for i in range(len(dataset)):
        dataset.iat[i, 1] = my_compute(dataset.iat[i, 0])


@timeit
def use_panda_iterrows(dataset, **kwargs):
    """ Use panda iterrows() to iterate """
    b = np.empty(len(dataset))
    for index, row in dataset.iterrows():
        b = my_compute(row['a'])
    dataset['b'] = b


@timeit
def use_column(dataset, **kwargs):
    dataset['b'] = dataset.a + 1


@timeit
def use_panda_apply(dataset, **kwargs):
    """ Use panda built-in apply function"""
    dataset['b'] = dataset.apply(my_compute)


@timeit
def use_zip(dataset, **kwargs):
    """ Use enumerate function to iterate"""
    b = np.empty(len(dataset))
    for i, (x) in enumerate(zip(dataset.a)):
        b[i] = my_compute(x[0])
    dataset['b'] = b


@timeit
def use_numpy_for_loop(dataset, **kwargs):
    """ Get column values as a numpy array compute and then assign values back to panda data frame"""
    b = np.empty(len(dataset))
    original = dataset.a
    for i in range(len(dataset)):
        b[i] = my_compute(original[i])
    dataset['b'] = b


def time_this(func, method_name, N=1000):
    """ Execute the given function 100 times and measure the execution time for each run.
        Returns a dictionary containing the statistics based on the execution times
    """
    repeats = 100
    a = np.repeat(1000, N)
    pd_dataset = pd.DataFrame({'a': a})

    timing = []
    for i in range(repeats):
        func(pd_dataset.copy(), log_time=timing)
    return {'method': method_name, 'average': np.average(timing), 'min': np.min(timing), 'max': np.max(timing)}


def measure_time(dataset_size):
    all_timing = pd.DataFrame()
    all_timing = all_timing.append([time_this(use_column, 'use_column', N=dataset_size)], )
    all_timing = all_timing.append([time_this(use_panda_apply, 'use_panda_apply', N=dataset_size)])

    all_timing = all_timing.append([time_this(use_for_loop_loc, 'use_for_loop_loc', N=dataset_size)])
    all_timing = all_timing.append([time_this(use_for_loop_at, 'use_for_loop_at', N=dataset_size)])
    all_timing = all_timing.append([time_this(use_for_loop_iat, 'use_for_loop_iat', N=dataset_size)])
    all_timing = all_timing.append([time_this(use_numpy_for_loop, 'use_numpy_for_loop', N=dataset_size)])
    all_timing = all_timing.append([time_this(use_panda_iterrows, 'use_panda_iterrows', N=dataset_size)])
    all_timing = all_timing.append([time_this(use_zip, 'use_zip', N=dataset_size)])
    print(all_timing[['method', 'average', 'min', 'max']])
    all_timing.to_csv('/tmp/performance' + str(dataset_size) + ".csv")


measure_time(1000)
measure_time(10000)
measure_time(100000)
measure_time(1000000)