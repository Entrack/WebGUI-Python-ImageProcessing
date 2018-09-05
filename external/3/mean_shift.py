import math
import random
from math import sqrt

import numpy as np
from PIL import Image, ImageDraw

from utils import rgb2lab, deltaE_ciede2000

# MIN_DISTANCE = 80.1
MIN_DISTANCE = 22





def weirddist(a, b):
    return deltaE_ciede2000(np.tile(a, [len(b), 1]), b)


def gaussian_kernel(a, b, bandwidth):
    dist = weirddist(a, b)
    val = (1 / (bandwidth * sqrt(2 * math.pi))) * np.exp(-0.5 * ((dist / bandwidth)) ** 2)
    return val


def shift(weirdcache, point, points):
    hash = int(point[0]) * 300 * 200 + (int(point[1]) + 100) * 300 + (int(point[2]) + 108)
    if hash not in weirdcache:
        # numerator
        kernel_bandwidth = 10
        point_weights = gaussian_kernel(point, points, kernel_bandwidth)
        tiled_weights = np.tile(point_weights, [len(point), 1])
        # denominator
        denominator = sum(point_weights)
        shifted_point = np.multiply(tiled_weights.transpose(), points).sum(axis=0) / denominator
        weirdcache[hash] = shifted_point
    # print 'Cache miss'
    return weirdcache[hash]


def mean_shift(INPUT_IMG='64.gif', OUTPUT_IMG='output.png'):
    weirdcache = {}
    # Lab points
    im = Image.open(INPUT_IMG).convert('RGB')
    img = np.array(im)

    draw = ImageDraw.Draw(im)

    points = np.array([rgb2lab(x) for x in img.reshape([-1, 3])])
    shift_points = np.copy(points)
    max_min_dist = 9000
    maxiter = 128
    iter = 0

    stopshift = np.zeros(shape=points.shape[:1], dtype='bool')
    while max_min_dist > MIN_DISTANCE:
        max_min_dist = 0
        for i in xrange(len(shift_points)):
            if stopshift[i]:
                continue
            p_new = shift_points[i]
            p_new_start = p_new
            p_new = shift(weirdcache, p_new, points)
            dist = deltaE_ciede2000(p_new_start, p_new)
            if dist < MIN_DISTANCE:
                stopshift[i] = True
            max_min_dist = max(max_min_dist, dist)
            shift_points[i] = p_new
        iter += 1
        if iter > maxiter:
            print('Out of maxiter')
            break

    clusters = np.zeros(shape=shift_points.shape[:1], dtype='int')

    clst = 1
    for i in xrange(clusters.shape[0]):
        if clusters[i] == 0:
            t = deltaE_ciede2000(shift_points[i], shift_points)
            clusters[t < MIN_DISTANCE] = clst
            clst += 1

    loaded = im.load()
    clcl = [(random.randint(0, 0x100), random.randint(0, 0x100), random.randint(0, 0x100)) for x in range(clst)]
    for y in xrange(0, img.shape[0]):
        for x in xrange(0, img.shape[1]):
            loaded[x, y] = clcl[clusters[y * img.shape[1] + x]]
    im.save(OUTPUT_IMG)
