from itertools import islice, chain


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
    it = iter(iterable)
    while True:
        batchiter = islice(it, size)

        # The call to next() is done so that when we have sliced to the
        # end of the input and get an empty generator, StopIteration will
        # be raised, and bubble up to be raised in batch(), and thus
        # iteration over the whole batch will stop.
        yield chain([next(batchiter)], batchiter)
