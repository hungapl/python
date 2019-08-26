from datetime import datetime


class Timer:

    def __init__(self, verbose=True):
        self.logs = list()
        self.verbose = verbose
        self.marked = None

    def start(self):
        self.marked = datetime.now()

    def reset(self):
        self.start()

    def checkpoint(self, process:str):
        duration = int((datetime.now() - self.marked).total_seconds())
        self.logs.append({'start_time': self.marked, 'duration':duration, 'process':process})

        if self.verbose:
            print(process + ' completed in ' + str(duration) + ' seconds.')
        self.marked = datetime.now()


def example():
    import time

    t = Timer()
    t.start()
    time.sleep(3)
    t.checkpoint('process1')
    time.sleep(2)
    t.checkpoint('process2')

example()


