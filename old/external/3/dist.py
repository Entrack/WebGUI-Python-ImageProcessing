from math import pow, exp

import numpy as np

from utils import CIEDERGB


def dist(a, b):
    avgc1 = np.average(a.reshape([-1, 3]), axis=0)
    avgc2 = np.average(b.reshape([-1, 3]), axis=0)
    return CIEDERGB(avgc1, avgc2)


def norm_similarity(a, b):
    return max(0, exp(-pow(CIEDERGB(a, b) / 8., 2)))
