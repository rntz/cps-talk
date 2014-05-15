class Re(object):
    def match(self, str, idx, cont):
        raise NotImplementedError()

    def matches(self, str):
        return self.match(str, 0, lambda i: i == len(str))

class ReChar(Re):
    def __init__(self, char): self.char = char
    def match(self, str, idx, cont):
        if len(str) > idx and str[idx] == self.char:
            return cont(idx+1)
        return False


class ReSeq(Re):
    def __init__(self, first, second): self.first, self.second = first, second
    def match(self, str, idx, cont):
        return self.first.match(str, idx,
                                lambda idx: self.second.match(str, idx, cont))

class ReOr(Re):
    def __init__(self, first, second): self.first, self.second = first, second
    def match(self, str, idx, cont):
        return (self.first.match(str, idx, cont)
                or self.second.match(str, idx, cont))

class ReStar(Re):
    def __init__(self, inner): self.inner = inner
    def match(self, str, idx, cont):
        return (self.inner.match(str, idx,
                                 lambda idx: self.match(str, idx, cont))
                or cont(idx))
