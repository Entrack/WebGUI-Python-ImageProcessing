class SquareM:
    def __init__(self, onerect):
        self.rects = [onerect]

    def merge(self, other):
        self.rects += other.rects

    def intersects(self, other):
        for a in self.rects:
            for b in other.rects:
                y0, x0, h0, w0 = a
                y1, x1, h1, w1 = b
                if y0 == y1 + h1 or y0 + h0 == y1:
                    if x0 > x1 and x0 < x1 + w1:
                        return [a, b]
                    if x1 > x0 and x1 < x0 + w0:
                        return [a, b]
                    if x0 + w0 > x1 and x0 + w0 < x1 + w1:
                        return [a, b]
                    if x1 + w1 > x0 and x1 + w1 < x0 + w0:
                        return [a, b]
                    if x0 == x1:
                        return [a, b]
                if x0 == x1 + w1 or x0 + w0 == x1:
                    if y0 > y1 and y0 < y1 + h1:
                        return [a, b]
                    if y1 > y0 and y1 < y0 + h0:
                        return [a, b]
                    if y0 + h0 > y1 and y0 + h0 < y1 + h1:
                        return [a, b]
                    if y1 + h1 > y0 and y1 + h1 < y0 + h0:
                        return [a, b]
                    if y0 == y1:
                        return [a, b]
        return None
