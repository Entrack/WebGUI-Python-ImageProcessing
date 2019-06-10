import random
from math import sqrt

import numpy as np
import numpy.random
import scipy
import scipy.linalg
import scipy.optimize
import scipy.sparse.linalg
from PIL import Image, ImageDraw

NORMLIMIT = 1E-2
FORCESPLITSIZE = 8

from dist import norm_similarity




# TOSTOP = 32 * 32
TOSTOP = 1024
MAXDEPTH = 100








def normcut_flatcoord(shape, x, y):
    return shape[1] * y + x


cache = {}


class EnoughException(Exception):
    pass



def ncutval(cut, SPLITPOINT, ddata, A, d):
    X = ((cut > SPLITPOINT).astype('float') - 1 / 2.) * 2
    ddiag = np.array(ddata)
    K = sum(ddiag[X > 0]) / sum(ddiag)
    # print K
    B = K / (1 - K)
    Y = (1 + X) - B * (1 - X)
    YY = scipy.sparse.csc_matrix((list(Y), ([0] * len(Y), range(len(Y))))).transpose()
    rx = (YY.transpose().dot(A).dot(YY) / (YY.transpose().dot(d).dot(YY)))[0, 0]
    return rx

NANOHACK = 1E-128

def normcut(area, mask):
    pts = area.shape[0] * area.shape[1]
    wdata = []
    wids = []

    for y in xrange(area.shape[0]):
        for x in xrange(area.shape[1]):
            me = area[y, x]
            meid = normcut_flatcoord(area.shape, x, y)
            if not mask[y, x]:
                continue
            # We are... pretty much connected to ourselves
            wdata += [1]
            wids += [(meid, meid)]

            # [y-1,x], [y,x-1]
            # Moving only forward, avoiding repeats
            for z in [[y + 1, x], [y, x + 1]]:
                # z[0]>=0 and z[1]>=0
                if z[0] < area.shape[0] and z[1] < area.shape[1]:
                    t = area[z[0], z[1]]
                    tid = normcut_flatcoord(area.shape, z[1], z[0])
                    if mask[z[0], z[1]]:
                        tx = norm_similarity(me, t)
                    else:
                        tx = numpy.random.rand() * NANOHACK
                    wdata += [tx] + [tx]
                    wids += [(meid, tid)] + [(tid, meid)]

    # print 'Built wdata'
    w = scipy.sparse.coo_matrix((wdata, ([w[0] for w in wids], [w[1] for w in wids])), shape=[pts, pts], dtype='float')
    # This NANOHACK lets me to not bother about truncating matrices more precisely
    ddata = (w.sum(axis=0) + numpy.random.rand(pts) * NANOHACK).tolist()[0]
    dids_simple = [x for x in xrange(0, pts)]
    # print 'Built ddata'
    d = scipy.sparse.coo_matrix((ddata, (dids_simple, dids_simple)), shape=[pts, pts], dtype='float')
    w = w.tocsc()
    d = d.tocsc()
    A = d - w
    B = d
    # print 'Go eigenvalues'
    ret = scipy.sparse.linalg.eigsh(A=A, M=B, k=2, sigma=0, which='LM')
    # print 'Finished'
    valz = ret[0]
    vecz = ret[1]
    cut = vecz[:, np.argmax(valz)]
    ret = np.empty(area.shape[:2])

    optme = lambda x: ncutval(cut, x, ddata, A, d)
    SPLITPOINT = scipy.optimize.fmin(func=optme, x0=np.average(cut), ftol=1E-8, disp=False)
    # print SPLITPOINT, np.average(cut)

    ncut = ncutval(cut, SPLITPOINT, ddata, A, d)
    X = ((cut > SPLITPOINT).astype('float') - 1 / 2.) * 2

    if ncut > NORMLIMIT and sqrt(area.shape[0] * area.shape[1]) < FORCESPLITSIZE:
        raise EnoughException("You've got enough, dude")

    for i, n in enumerate(X):
        y = i / area.shape[1]
        x = i % area.shape[1]
        if n > 0:
            ret[y, x] = 1
        else:
            ret[y, x] = 0
        if not mask[y, x]:
            ret[y, x] = -1
    return ret


def normcut_bbox(what):
    rows = np.any(what, axis=1)
    cols = np.any(what, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax + 1, cmin, cmax + 1




def normcut_recurse(img, mask, depth):
    if (np.count_nonzero(mask) < TOSTOP) or depth > MAXDEPTH:
        return [mask]
    bbox = normcut_bbox(mask)
    # print bbox
    imgcut = img[bbox[0]:bbox[1], bbox[2]:bbox[3]]
    maskcut = mask[bbox[0]:bbox[1], bbox[2]:bbox[3]]
    try:
        rx = normcut(imgcut, maskcut)
    except KeyboardInterrupt:
        raise
    except EnoughException:
        return [mask]
    except RuntimeError:
        return [mask]
    mask1 = np.logical_and(rx == 0, rx != -1)
    mask2 = np.logical_and(rx == 1, rx != -1)
    r = normcut_recurse(imgcut, mask1, depth + 1) + normcut_recurse(imgcut, mask2, depth + 1)
    # Un-bound-box
    retval = []
    for x in r:
        truex = np.zeros_like(mask)
        truex[bbox[0]:bbox[1], bbox[2]:bbox[3]] = x
        retval += [truex]
    return retval


def norm_cut(INPUT_IMG, OUTPUT_IMG):
    im = Image.open(INPUT_IMG).convert('RGB')
    # im=im.resize(WORKSIZE, Image.ANTIALIAS)
    img = np.array(im)

    draw = ImageDraw.Draw(im)
    loaded = im.load()
    ret = normcut_recurse(img, np.ones(img.shape[:2], dtype=bool), 0)
    for r in ret:
        clrr = random.randint(0, 0x100)
        clrg = random.randint(0, 0x100)
        clrb = random.randint(0, 0x100)
        for y in xrange(0, img.shape[0]):
            for x in xrange(0, img.shape[1]):
                if r[y, x]:
                    loaded[x, y] = (clrr, clrg, clrb)

    im.save(OUTPUT_IMG)
