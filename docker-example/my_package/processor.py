import numpy as np
import sys


class Processor:

    # Simple process method that returns the sum of two values
    def process(self, x, y):
        return np.sum([x, y])


if __name__== "__main__":
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    p = Processor()
    print(str(x) + ' + ' + str(y) + ' = ' + str(p.process(x, y)))