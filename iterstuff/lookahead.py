class Lookahead(object):
    """
    A Lookahead is a wrapper for any generator that lets you look at the
    next element to be returned (one-element lookahead). It also provides
    a way to check for end-of-iterator.

    If L{atstart} and L{atend} are both True, the generator is empty.

    @ivar _g: the wrapped generator.
    @ivar _x: the next element.
    @ivar _atend: True when the Lookahead is at the last element.
    @ivar _atstart: True when the Lookahead is at the first element.
    """
    _g = None

    _x = None

    _atend = False

    def __init__(self, gen):
        """
        @param gen: the generator to be wrapped. The first element will be
        retrieved immediately.
        """
        self._g = iter(gen)
        self._advance()
        self._atstart = True

    def _advance(self):
        """
        Advance one element, setting L{_x}, L{_atstart} and L{_atend}
        """
        try:
            self._atstart = False
            self._x = self._g.next()
        except StopIteration:
            self._x = None
            self._atend = True

    @property
    def atend(self):
        """
        When C{atend} is True, L{peek} will return None, and L{next} will
        raise StopIteration.

        @return: True when the Lookahead is B{past} the last element.
        """
        return self._atend

    _atstart = True

    @property
    def atstart(self):
        """
        If this property is True, it does not mean that there is
        necessarily a next element: the iterator could be empty.

        @return: True when the Lookahead is at the first element.
        """
        return self._atstart

    @property
    def peek(self):
        """
        @return: the value of the next element that will be yielded from the
        generator (from L{next}), or C{None} if L{atend} is True.
        """
        return self._x

    # Iterator protocol support

    def __iter__(self):
        """
        Support iterator protocol
        @return: self
        """
        return self

    def next(self):
        # If we're already at the end, stop iteration
        if self._atend:
            raise StopIteration

        # Save the value to yield
        _x = self._x

        self._advance()

        return _x

    def __next__(self):
        """
        Python3 - compatible variant of next()
        @return: value of next()
        """
        return self.next()

    # Static utility functions

    @staticmethod
    def chunked(i, f=lambda _x: _x):
        """
        Given an iterable i, apply f over it to extract a value from
        each element and yield successive iterables where the result
        of f for all elements is the same.

        In simpler language, if i is an iterable sorted on some key, yield
        chunks of that list where the key value is the same, each chunk being
        a separate iterable.

        Note that this function yields B{iterators}, not lists, and they refer
        back to the iterator passed in, so each B{must} be consumed completely
        before the next one is requested.

        @param i: an iterable.
        @param f: a function to be applied to each element of the iterable to
        extract the key.
        """
        # Build a generator that return tuples of (element, key-of-element),
        # so that we only apply the key method to each element once.
        lah = Lookahead((_x, f(_x)) for _x in i)

        def takechunk():
            """
            A generator closure that will yield values while the keys remain
            the same. Note that we cannot use L{itertools.takewhile} for this,
            because that takes elements and B{then} checks the predicate, so
            successive calls to itertools.takewhile for the same generator will
            skip elements.
            """
            while True:
                # Always yield the first element: if we're at the end of the
                # generator, this will raise StopIteration and we're done.
                (_x, key) = lah.next()
                yield _x

                # Check the lookahead's peek value to see if we should break now.
                # We also break when we're at the end of the generator.
                if lah.atend or key != lah.peek[1]:
                    break

        # Yield successive instances of takechunk.
        while not lah.atend:
            yield takechunk()


def repeatable_takewhile(predicate, iterable):
    """
    repeatable_takewhile(predicate, iterable) --> generator

    Return successive entries from an iterable as long as the
    predicate evaluates to true for each entry.

    Like itertools.takewhile, but does not consume the first
    element of the iterable that fails the predicate test.

    :param predicate: a single-element callable that returns True
    for elements that satisfy a condition, False for those that
    do not.
    :param iterable: must be a Lookahead
    """
    # Assert that the iterable is a Lookahead. The act of wrapping
    # an iterable in a Lookahead consumes the first element, so we
    # cannot do the wrapping inside this function.
    if not isinstance(iterable, Lookahead):
        raise TypeError("The iterable parameter must be a Lookahead")

    # Use 'peek' to check if the next element will satisfy the
    # predicate, and yield while this is True, or until we reach
    # the end of the iterable.
    while (not iterable.atend) and predicate(iterable.peek):
        yield iterable.next()
