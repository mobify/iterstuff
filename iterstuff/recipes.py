from __future__ import absolute_import
from iterstuff.lookahead import Lookahead


def repeatable_takewhile(predicate, iterable):
    """
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


def batch(iterable, size):
    """
    Yield iterables for successive slices of `iterable`, each containing
    up to `size` items, with the last being less than `size` if there are
    not sufficient items in `iterable`. Pass over the input iterable once
    only. Yield iterables, not lists.

    @note: each output iterable must be consumed in full before the next
     one is yielded. So list(batch(xrange(10), 3)) won't work as expected,
     because the iterables are not consumed.

    @param iterable: an input iterable.
    @param size: the maximum number of items yielded by any output iterable.
    """
    # Wrap an enumeration of the iterable in a Lookahead so that it
    # yields (count, element) tuples
    it = Lookahead(enumerate(iterable))

    while not it.atend:
        # Set the end_count using the count value
        # of the next element.
        end_count = it.peek[0] + size

        # Yield a generator that will then yield up to
        # 'size' elements from 'it'.
        yield (
            element
            for counter, element in repeatable_takewhile(
                # t[0] is the count part of each element
                lambda t: t[0] < end_count,
                it
            )
        )


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
    it = Lookahead((_x, f(_x)) for _x in i)

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
            (_x, key) = it.next()
            yield _x

            # Check the lookahead's peek value to see if we should break now.
            # We also break when we're at the end of the generator.
            if it.atend or key != it.peek[1]:
                break

    # Yield successive instances of takechunk.
    while not it.atend:
        yield takechunk()

