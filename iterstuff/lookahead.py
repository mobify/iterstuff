import six

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

    def __init__(self, gen):
        """
        @param gen: the generator to be wrapped. The first element will be
        retrieved immediately.
        """
        self._g = iter(gen)
        self._atend = False
        self._advance()
        self._atstart = True

    def _advance(self):
        """
        Advance one element, setting L{_x}, L{_atstart} and L{_atend}
        """
        try:
            self._atstart = False
            self._x = six.advance_iterator(self._g)
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
