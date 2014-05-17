# TODO: add comments to this file mirroring Regexp.hs
class Re(object):
    def match(self, str, idx, cont):
        raise NotImplementedError()

    def matches(self, str):
        return self.match(str, 0, lambda i: i == len(str))

class ReChar(Re):
    # ReChar(c) represents the character literal c.
    def __init__(self, char): self.char = char
    def match(self, str, idx, cont):
        # If the character at idx is the one we're looking for, we match!
        if len(str) > idx and str[idx] == self.char:
            # If we match, we call our continuation, to check that the rest of
            # the string matches
            return cont(idx+1)
        return False            # we didn't match

class ReSeq(Re):
    # ReSeq(a, b) represents /ab/
    def __init__(self, first, second): self.first, self.second = first, second
    def match(self, str, idx, cont):
        # first try matching self.first
        return self.first.match(str, idx,
                                # giving a modified continuation that checks
                                # whether self.second matches
                                lambda idx: self.second.match(str, idx, cont))

class ReOr(Re):
    # ReOr(a,b) represents /a|b/
    def __init__(self, first, second): self.first, self.second = first, second
    def match(self, str, idx, cont):
        return (self.first.match(str, idx, cont) # try matching self.first
                or self.second.match(str, idx, cont) # else try self.second
        )
        # Note how we might call our continuation twice - backtracking!

class ReStar(Re):
    # ReStar(a) represents /a*/
    def __init__(self, inner): self.inner = inner
    def match(self, str, idx, cont):
        return (
            # the one-or-more case, like /aa*/
            self.inner.match(str, idx,
                                 lambda idx: self.match(str, idx, cont))
            # the empty case, like //
            or cont(idx))
