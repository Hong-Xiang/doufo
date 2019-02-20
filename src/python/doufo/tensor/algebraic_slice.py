import typing as T
import itertools

__all__ = ["as_", "indexing"]


class LazyView:
    def __init__(self, index_like=None):
        self.index = index_like

    def __getitem__(self, item):
        if self.index is None:
            return LazyView(item)
        else:
            return LazyView(reduce_index_exp(self.index, item))


as_ = LazyView()


def indexing(arr, lv):
    return arr[lv.index]


SLICE_LIKE = T.Union[int, slice, type(...)]
SLICES_LIKE = T.Union[SLICE_LIKE, T.Tuple[slice]]


def map_if(target, predicate, fn_true, fn_false):
    if predicate(target):
        return fn_true(target)
    else:
        return fn_false(target)


def zip_longest_with(fn, *iterables):
    return (fn(*x) for x in itertools.zip_longest(*iterables))


def simplify(index_exp):
    if isinstance(index_exp, tuple) and len(index_exp) == 1:
        return index_exp[0]
    return index_exp


def reduce_index_exp(pre, now=...) -> T.Tuple:
    """
    IndexTerm: int | slice
    IndexExpression: (IndexTerm,) | (IndexTerm, ...) | (IndexTerm, *IndexExpression)
    :param pre: IndexExpression
    :param now: IndexExpression
    :return: index expression
    """

    def to_tuple(x):
        if isinstance(x, tuple):
            return x
        if isinstance(x, list):
            return tuple(x)
        return (x,)

    pre, now = to_tuple(pre), to_tuple(now)
    result = []
    p_i, n_i = 0, 0

    def get_term(xs, i):
        if i >= len(xs):
            return ...
        else:
            return xs[i]

    while p_i < len(pre) or n_i < len(now):
        p_t, n_t = get_term(pre, p_i), get_term(now, n_i)
        if p_t is ... and n_t is ...:
            break
        if p_t is ...:
            result.append(n_t)
            n_i += 1
            continue
        if n_t is ...:
            result.append(p_t)
            p_i += 1
            continue
        if isinstance(p_t, int):
            result.append(p_t)
            p_i += 1
            continue

        result.append(reduce_term(p_t, n_t))
        p_i, n_i = p_i + 1, n_i + 1
    return simplify(tuple(result))


def reduce_term(pre, now):
    if pre is None or pre is ...:
        return now
    if now is None or now is ...:
        return pre
    if isinstance(pre, slice):
        if isinstance(now, int):
            return reduce_slice_int(pre, now)
        if isinstance(now, slice):
            return reduce_slice_slice(pre, now)
        raise TypeError(f"Invalid now index term: {now}")
    if isinstance(pre, int):
        raise TypeError(f"Can not index 1D slice {pre} with {now}")
    raise TypeError(f"Invalid previous index term: {pre}")


def complete_slice(slice_: slice):
    return slice(slice_.start or 0, slice_.stop, slice_.step or 1)


def is_index_out_of_range(slice_: slice, index: int):
    slice_ = complete_slice(slice_)
    if (slice_.start >= 0 and index < 0) or (slice_.start < 0 and index > 0):
        return True
    if slice_.stop is None:
        return False
    if slice_.step > 0 and index >= slice_.stop:
        return True
    if slice_.step < 0 and index <= slice_.stop:
        return True
    return False


def reduce_slice_int_unsafe(slice_: slice, index: int) -> int:
    s = complete_slice(slice_)
    return s.start + s.step * index


def reduce_slice_int(slice_: slice, index: int) -> int:
    result = reduce_slice_int_unsafe(slice_, index)
    if is_index_out_of_range(slice_, result):
        raise IndexError(f"Indexing slice {slice_}[{index}] out of range.")
    else:
        return result


def reduce_slice_slice(previous: slice, current: slice) -> slice:
    p, c = complete_slice(previous), complete_slice(current)
    step = p.step * c.step

    start = reduce_slice_int_unsafe(p, c.start)
    if c.stop is not None:
        stop_result = reduce_slice_int_unsafe(p, reduce_slice_int_unsafe(c, c.stop))
        if p.stop is None:
            stop = stop_result
        else:
            stop = min(p.stop, stop_result) if step > 0 else max(p.stop, stop_result)
    else:
        stop = p.stop
    return slice(start, stop, step)
