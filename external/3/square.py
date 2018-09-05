class Square:
    def __init__(self, rect):
        self.rect = rect
        self.children = []
        self.connections = []

    def add(self, children):
        assert 4 == len(children)
        self.children = children


