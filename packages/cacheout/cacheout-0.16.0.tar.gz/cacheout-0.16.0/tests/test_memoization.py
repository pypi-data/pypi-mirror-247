import typing as t
from unittest import mock

import pytest

from cacheout import (
    Cache,
    FIFOCache,
    LFUCache,
    LIFOCache,
    LRUCache,
    MRUCache,
    RRCache,
    fifo_memoize,
    lfu_memoize,
    lifo_memoize,
    lru_memoize,
    memoize,
    mru_memoize,
    rr_memoize,
)


parametrize = pytest.mark.parametrize


@parametrize(
    "memoizer,cache_class",
    [
        (memoize, Cache),
        (fifo_memoize, FIFOCache),
        (lfu_memoize, LFUCache),
        (lifo_memoize, LIFOCache),
        (lru_memoize, LRUCache),
        (mru_memoize, MRUCache),
        (rr_memoize, RRCache),
    ],
)
def test_memoize_cache(memoizer: t.Callable, cache_class: t.Type[Cache]):
    @memoizer()
    def func():
        pass

    assert isinstance(func.cache, cache_class)

    patch = f"cacheout.memoization.{cache_class.__name__}"

    with mock.patch(patch) as mocked:

        @memoizer()
        def func2():
            pass

        assert mocked.called
        assert mocked().memoize.called
