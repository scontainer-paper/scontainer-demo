from datamodel.common import *
from datamodel.common import ret_frozenset
from datamodel.definitions.preliminaries import pi_2, Pi_1, pi_1


def sigma(at: int, components: TYPE_PATH) -> TYPE_VALUE_STR | type[EMPTY_SET]:
    for component in components:
        if pi_1(component) == at:
            return pi_2(component)
    return EMPTY_SET


def assert_is_path(x: TYPE_PATH):
    # indices start from 1 and are consecutive
    # indices are also unique
    if not x:
        assert False, "Empty set is not a path"
    if len(x) != max(Pi_1(x)):
        raise AssertionError(f"Indices are not consecutive")
    indices = set()
    for t in x:
        if pi_1(t) in indices:
            raise AssertionError(f"Index {pi_1(t)} is not unique")
        indices.add(pi_1(t))


def assert_is_data_path(p: TYPE_PATH):
    assert_is_path(p)
    if len(p) % 2 != 0:
        assert False, f"Path {p} is not a data path as its length is not even"
    for i in range(1, len(p) // 2 + 1):
        if not TypeEquals(sigma(2 * i - 1, p), str) or not TypeEquals(sigma(2 * i, p), int):
            assert False, f"Path {p} is not a data path"


def assert_is_template_path(p: TYPE_PATH):
    assert_is_path(p)
    for i in range(1, len(p) + 1):
        if not TypeEquals(sigma(i, p), str):
            assert False, f"Path {p} is not a template path"


def assert_is_index_path(p: TYPE_PATH):
    assert_is_path(p)
    for i in range(1, len(p) + 1):
        if not TypeEquals(sigma(i, p), int):
            assert False, f"Path {p} is not an index path"


@ret_frozenset
def Parent_D(x: TYPE_PATH) -> TYPE_PATH:
    assert_is_path(x)
    return x - {(len(x), sigma(len(x), x))} | {(1, sigma(1, x))}


@ret_frozenset
def Concat(x: TYPE_PATH, y: TYPE_PATH) -> TYPE_PATH:
    assert_is_path(x)
    assert_is_path(y)
    return x | {(pi_1(t) + len(x), pi_2(t)) for t in y}


@ret_frozenset
def Sub(x: TYPE_PATH, y: TYPE_PATH) -> TYPE_PATH:
    assert_is_path(x)
    assert_is_path(y)
    if y.issubset(x) and y != x:
        return {(pi_1(t) - len(y), pi_2(t)) for t in x - y}
    else:
        return x


@ret_frozenset
def I_n(n: int, max_index: int = 2) -> set[TYPE_PATH_INDEX]:
    from itertools import product
    """
    Apparently we are not able to generate an infinite I_n set.
    So we use max_index to limit the range of indices.
    """
    res = set()
    for t in product(range(1, max_index + 1), repeat=n):
        res.add(
            frozenset({(i, t[i - 1]) for i in range(1, n + 1)})
        )
    return res


@ret_frozenset
def Parents(x: TYPE_PATH) -> set[TYPE_PATH]:
    parent = None
    res = set()
    while Parent_D(x) != parent:
        x = Parent_D(x)
        res.add(x)
        parent = x
    return res
