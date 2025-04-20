from datamodel.definitions.path import *
from datamodel.definitions.preliminaries import CartesianProduct


@ret_frozenset
def G(d: TYPE_COMPONENTS | TYPE_DATA | TYPE_ATOMIC_VALUE) -> set | frozenset:
    if TypeEquals(d, TYPE_ATOMIC_VALUE):
        return {d}
    else:
        return BigUnion(CartesianProduct({pi_1(tau)}, G(pi_2(tau))) for tau in d)


@ret_frozenset
def R_sigma_n(n: int, df: TYPE_DATA_FLATTENED) -> TYPE_RELATION:
    return {(x, y) for x in df for y in df if sigma(n, pi_1(x)) == sigma(n, pi_1(y)) and sigma(n, pi_1(x)) != EMPTY_SET}


@ret_frozenset
def equivalent_class(t: tuple[TYPE_PATH_DATA, TYPE_ATOMIC_VALUE], R: TYPE_RELATION) -> TYPE_DATA_FLATTENED:
    return {pi_2(relation_pair) for relation_pair in R if pi_1(pi_1(relation_pair)) == pi_1(t)}


@ret_frozenset
def E_n(n: int, f: TYPE_DATA_FLATTENED):
    R_sigma_n_plus_1 = R_sigma_n(n + 1, f)
    if R_sigma_n_plus_1 == EMPTY_SET:
        return {(sigma(n, pi_1(t)), pi_2(t)) for t in f}
    else:
        singleton = BigUnion({sigma(n, pi_1(t))} for t in f)
        assert len(singleton) == 1, "The union of {sigma_n(pi_1(t))} for all t in f is not a singleton"

        union = BigUnion(E_n(n + 1, equivalent_class(t, R_sigma_n_plus_1)) for t in f)
        singleton = frozenset(singleton)
        return CartesianProduct(singleton, frozenset({union}))


@ret_frozenset
def Nested(d: TYPE_DATA_FLATTENED) -> TYPE_DATA:
    equivalence_relation = R_sigma_n(1, d)
    return BigUnion(E_n(1, equivalent_class(t, equivalence_relation)) for t in d)


def H(i: TYPE_VALUE_INT, tau: tuple) -> TYPE_DATA_FLATTENED:
    if not TypeEquals(pi_2(tau), TYPE_ATOMIC_VALUE):
        h_i_plus_1_tau = H(i + 1, pi_2(tau))
        return (frozenset({(i, pi_1(tau))}) | pi_1(h_i_plus_1_tau), pi_2(h_i_plus_1_tau))
    else:
        return (frozenset({(i, pi_1(tau))}), pi_2(tau))


@ret_frozenset
def flatten(d: TYPE_DATA) -> TYPE_DATA_FLATTENED:
    return {H(1, tau) for tau in G(d)}
