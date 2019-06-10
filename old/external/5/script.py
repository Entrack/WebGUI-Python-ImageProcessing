import math
import sys

import numpy as np
from PIL import Image, ImageDraw


def diff(c1, c2):
    neg = side_size / 2
    p1l = c1 - neg
    p1r = c1 + neg + 1
    p2l = c2 - neg
    p2r = c2 + neg + 1
    return sum((im1[p1l[0]:p1r[0], p1l[1]:p1r[1]] - im2[p2l[0]:p2r[0], p2l[1]:p2r[1]]).flatten() ** 2)


def search(c1):
    c1 = np.asarray(c1)
    if diff(c1, c1) == 0:
        return c1
    minp = None
    minv = 9000 ** 2
    for off in np.ndindex((srch_size, srch_size)):
        c2 = c1 + off - srch_size / 2
        v = diff(c1, c2)
        if v < minv:
            minp = c2[:]
            minv = v
    return minp


fname1 = 'sources/frame07.png'
fname2 = 'sources/frame08.png'
im1 = np.array(Image.open(fname1).convert('L'))
im2 = np.array(Image.open(fname2).convert('L'))

side_size = 5
srch_size = 17
skip_size = 30

assert side_size % 2 == 1
assert srch_size % 2 == 1

offt_size = max(side_size, srch_size)

out = Image.open(fname1).convert('RGB')
draw = ImageDraw.Draw(out)
iarr = out.load()
lp = 0
for p in np.ndindex(tuple((np.asarray(im1.shape) - 2 * offt_size - 2).tolist())):
    px = np.array(p) + offt_size
    if px[0] % skip_size != 0 or px[1] % skip_size != 0:
        continue
    if px[0] != lp:
        lp = px[0]
    rt = search(px)
    if not (rt == px).all():
        tt = rt - px
        angv = math.atan2(tt[0], tt[1])
        j, i = px[1], px[0]
        lenv = np.linalg.norm(tt)
        p0 = (j, i)
        p1 = ((j + lenv * math.cos(angv)), (i + lenv * math.sin(angv)))
        hdr = lenv / 3
        a1 = ((p1[0] + hdr * math.cos(angv + 3 * math.pi / 4)), (p1[1] + hdr * math.sin(angv + 3 * math.pi / 4)))
        a2 = ((p1[0] + hdr * math.cos(angv - 3 * math.pi / 4)), (p1[1] + hdr * math.sin(angv - 3 * math.pi / 4)))
        if True:
            draw.line(p0 + p1, fill=(255, 0, 0), width = 2)
            draw.line(p1 + a1, fill=(255, 0, 0))
            draw.line(p1 + a2, fill=(255, 0, 0))
out.save('output.png')