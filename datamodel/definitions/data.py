from datamodel.definitions.path import *
from datamodel.definitions.preliminaries import CartesianProduct

def H(n: TYPE_VALUE_INT, kv: tuple) -> TYPE_DATA_FLATTENED:
    k, v = kv
    if not TypeEquals(v, TYPE_ATOMIC_VALUE):
        S, x = H(n + 1, v)
        return (frozenset({(n, k)} | S), x)
    else:
        return (frozenset({(n, k)}), v)


@ret_frozenset
def G(d: TYPE_ARRAY | TYPE_DOCUMENT | TYPE_ATOMIC_VALUE) -> set | frozenset:
    if TypeEquals(d, TYPE_ATOMIC_VALUE):
        return {d}
    else:
        return BigUnion(CartesianProduct({k}, G(v)) for (k, v) in d)


def K(df: TYPE_DATA_FLATTENED) -> set:
    return {sigma(1, pd) for (pd, v) in df}


@ret_frozenset
def Nested(df: TYPE_DATA_FLATTENED) -> set:
    result = set()
    for n in K(df):
        if any(len(pd) == 1 for (pd, v) in df):
            # result |= CartesianProduct({n}, {(sigma(1, pd), v) for (pd, v) in df})
            result |= {(sigma(1, pd), v) for (pd, v) in df}
        else:
            result |= CartesianProduct({n}, {Nested({(Sub(pd, {(1, n)}), v) for (pd, v) in df if sigma(1, pd) == n})})
    return result


@ret_frozenset
def flatten(d: TYPE_DOCUMENT) -> TYPE_DATA_FLATTENED:
    return {H(1, (k, v)) for (k, v) in G(d)}
