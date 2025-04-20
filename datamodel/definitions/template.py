import time
from typing import Type as _TYPE

from datamodel.common import *
from datamodel.common import random_atomic_values
from datamodel.definitions.data import G, H
from datamodel.definitions.path import assert_is_data_path, assert_is_template_path, assert_is_index_path, Concat, Sub, \
    Parent_D, I_n, Parents
from datamodel.definitions.preliminaries import pi_2, pi_1, CartesianProduct


def assert_is_template(t: TYPE_TEMPLATE):
    """
    Definition 19, used to check if a given template is valid.
    """
    for tau_1 in t:
        for tau_2 in t:
            if tau_1 == tau_2:
                continue
            if (not pi_1(tau_1).issubset(pi_1(tau_2)) and not pi_1(tau_2).issubset(pi_1(tau_1))
            ):
                continue
            else:
                assert False, f"Template is not valid"


@ret_frozenset
def Extract(tmpl: TYPE_TEMPLATE, p: TYPE_PATH_TEMPLATE) -> TYPE_TEMPLATE | frozenset:
    if len(p) > 1:
        return {(Sub(pi_1(t), Parent_D(p)), pi_2(t)) for t in tmpl if p.issubset(pi_1(t))}
    return {t for t in tmpl if p.issubset(pi_1(t))}


@ret_frozenset
def Insert(p: TYPE_PATH_TEMPLATE, t: TYPE_TEMPLATE) -> TYPE_TEMPLATE:
    return {(Concat(p, pi_1(t)), pi_2(t)) for t in t}


@ret_frozenset
def Delete(tmpl: TYPE_TEMPLATE, p: TYPE_PATH_TEMPLATE) -> TYPE_TEMPLATE | frozenset:
    return {t for t in tmpl if not p.issubset(pi_1(t))}


@ret_frozenset
def Merge(t1: TYPE_TEMPLATE, t2: TYPE_TEMPLATE) -> TYPE_TEMPLATE:
    return t1 | t2


@ret_frozenset
def Mv(t: TYPE_TEMPLATE, src: TYPE_PATH_TEMPLATE, dst: TYPE_PATH_TEMPLATE) -> TYPE_TEMPLATE:
    return Delete(Merge(t, Insert(dst, Extract(t, src))), src)


@ret_frozenset
def J(pd: TYPE_PATH_DATA) -> tuple[TYPE_PATH_TEMPLATE, TYPE_PATH_INDEX]:
    assert_is_data_path(pd)
    pT = {
        ((pi_1(t) + 1) // 2, pi_2(t)) for t in pd if TypeEquals(pi_2(t), TYPE_VALUE_STR)
    }

    I = {
        (pi_1(t) // 2, pi_2(t)) for t in pd if TypeEquals(pi_2(t), TYPE_POSITIVE_INT)
    }

    return pT, I


@ret_frozenset
def J_inverse(p: tuple[TYPE_PATH_TEMPLATE, TYPE_PATH_INDEX]) -> TYPE_PATH_DATA:
    pT, I = p
    assert_is_template_path(pT)
    assert_is_index_path(I)
    return {(2 * pi_1(t) - 1, pi_2(t)) for t in pT} | {(2 * pi_1(t), pi_2(t)) for t in I}


@ret_frozenset
def Split(d: TYPE_DATA) -> TYPE_DATA_SPLIT:
    return BigUnion(frozenset({(J(pi_1(H(1, tau))), pi_2(H(1, tau)))}) for tau in G(d))


def Type(value: TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER) -> _TYPE[
    TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER]:
    return type(value)


@ret_frozenset
def Template(d: TYPE_TEMPLATE) -> TYPE_TEMPLATE:
    return {(pi_1(pi_1(tau), ), Type(pi_2(tau))) for tau in Split(d)}


def deref():
    pass


@ret_frozenset
def Full(tmplt: TYPE_TEMPLATE) -> set:
    # correction: Definition 16 in the paper misses the "- {pi_1(tau)}" part
    return tmplt | BigUnion(CartesianProduct(Parents(pi_1(tau)) - {pi_1(tau)}, {TYPE_VALUE_CONTAINER}) for tau in tmplt)


def E_t(f: TYPE_TEMPLATE_FIELD, t: TYPE_TEMPLATE):
    if pi_2(f) == TYPE_VALUE_CONTAINER:
        return (pi_1(f), frozenset({E_t(tau, t) for tau in t if tau != f and pi_1(f) == Parent_D(pi_1(tau))}))
    else:
        return f


@ret_frozenset
def Nested_t(tmplt: TYPE_TEMPLATE):
    # correction: definition of Nested_t in Definition 27 should be E_t(f, Full(tmplt)) rather than E_t(f, tmplt)
    return {E_t(f, Full(tmplt)) for f in Full(tmplt) if len(pi_1(f)) == 1}


@ret_frozenset
def T_ref_bar(t: TYPE_TEMPLATE, crefs: set[TYPE_REF]) -> TYPE_TEMPLATE:
    assert_is_template(t)
    return BigUnion(Insert(pi_1(ref), Extract(t, pi_2(ref))) for ref in crefs)


@ret_frozenset
def T_ref_n(t: TYPE_TEMPLATE, crefs: set[TYPE_REF], n) -> TYPE_TEMPLATE:
    if n > 1:
        return T_ref_bar(T_ref_n(t, crefs, n - 1), crefs) | t
    else:
        return T_ref_bar(t, crefs) | t


@ret_frozenset
def K(tmplt: TYPE_TEMPLATE, max_index) -> TYPE_DATA_SPLIT:
    random.seed(time.time())
    return BigUnion(CartesianProduct(
        CartesianProduct(
            {pi_1(tau)}, I_n(len(pi_1(tau)), max_index=max_index)
        ),
        # apparently we cannot use the infinite domains of strings and numbers
        # so we limit the domains to 1000 values each
        random_atomic_values(pi_2(tau), count=1000)
    ) for tau in tmplt)


@ret_frozenset
def DataSplit(tmplt: TYPE_TEMPLATE, max_index=3) -> TYPE_DATA_SPLIT:
    assert_is_template(tmplt)
    # we don't generate the powerset of K, as it will be too large.
    # instead, we randomly choose a subset to form one document that does not have missing fields.
    _dict = {pi_1(tau): tau for tau in K(tmplt, max_index)}
    return _dict.values()


@ret_frozenset
def DataFlatten(tmplt: TYPE_TEMPLATE):
    assert_is_template(tmplt)
    return {(J_inverse(pi_1(tau)), pi_2(tau)) for tau in DataSplit(tmplt)}


@ret_frozenset
def DataFlattenedSample(tmplt: TYPE_TEMPLATE, max_index) -> TYPE_DATA_FLATTENED:
    return {(J_inverse(pi_1(tau)), pi_2(tau)) for tau in DataSplit(tmplt, max_index)}
