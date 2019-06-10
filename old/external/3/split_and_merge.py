import random

import numpy as np
from PIL import Image, ImageDraw

from dist import dist
from square import Square
from square_merged import SquareM

# WORKSIZE=(512, 512)
SPLIT_EPS = 14
UNITE_EPS = 14
MINSIZE = 2


# y0,x0,h,w
def split(img, node):
    y0 = node.rect[0]
    x0 = node.rect[1]
    h = node.rect[2]
    w = node.rect[3]
    if h == MINSIZE or w == MINSIZE:
        # Not something we going to work with
        return node
    # Quad-split first
    assert h % 2 == 0 and w % 2 == 0

    r00 = (y0, x0, h / 2, w / 2)
    r01 = (y0, x0 + w / 2, h / 2, w / 2)
    r10 = (y0 + h / 2, x0, h / 2, w / 2)
    r11 = (y0 + h / 2, x0 + w / 2, h / 2, w / 2)

    a00, a01, a10, a11 = (img[x[0]:x[0] + x[2], x[1]:x[1] + x[3]] for x in [r00, r01, r10, r11])

    d0001 = dist(a00, a01)
    d0010 = dist(a00, a10)
    d1101 = dist(a11, a01)
    d1110 = dist(a11, a10)

    if max([d0001, d0010, d1101, d1110]) < SPLIT_EPS:
        # This is the whole region
        return node
    else:
        node.add([split(img, Square(r00)), split(img, Square(r01)), split(img, Square(r10)), split(img, Square(r11))])
        return node


def square_candidates(n):
    global merge_squares
    if len(n.children) == 0:
        merge_squares += [SquareM(n.rect)]
    else:
        for x in n.children:
            square_candidates(x)


def split_and_merge(INPUT_IMG, OUTPUT_IMG):
    im = Image.open(INPUT_IMG).convert('RGB')
    img = np.array(im)

    draw = ImageDraw.Draw(im)

    root = Square([0, 0, img.shape[0], img.shape[1]])
    split(img, root)

    global merge_squares
    merge_squares = []
    square_candidates(root)
    final_list = []

    while len(merge_squares) > 0:
        couldmerge = False
        square1 = merge_squares[0]
        for x in merge_squares[1:]:
            t = square1.intersects(x)
            if t:
                r0 = t[0]
                r1 = t[1]
                if dist(img[r0[0]:r0[0] + r0[2], r0[1]:r0[1] + r0[3]],
                        img[r1[0]:r1[0] + r1[2], r1[1]:r1[1] + r1[3]]) < UNITE_EPS:
                    square1.merge(x)
                    merge_squares.remove(x)
                    couldmerge = True
        if not couldmerge:
            final_list += [square1]
            merge_squares = merge_squares[1:]

    for f in final_list:
        clr = random.randint(0, 0xFFFFFF)
        for rect in f.rects:
            draw.rectangle((rect[1], rect[0], rect[1] + rect[3], rect[0] + rect[2]), fill=clr)

    im.save(OUTPUT_IMG)
