from lookahead import Lookahead, repeatable_takewhile


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
