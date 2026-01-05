import time
from typing import Type as _TYPE

from datamodel.common import *
from datamodel.common import random_atomic_values
from datamodel.definitions.data import flatten
from datamodel.definitions.path import assert_is_data_path, assert_is_template_path, assert_is_index_path, Concat, Sub, \
    Parent_D, I_n, Parents
from datamodel.definitions.preliminaries import CartesianProduct, Pi_1


def assert_is_template(tmplt: TYPE_TEMPLATE):
    """
    Definition 18, used to check if a given template is valid.
    """
    for (pT, t) in tmplt:
        for (pT1, t1) in tmplt:
            if pT1 == pT and t == t1:
                continue
            elif pT1 != pT and not pT.issubset(pT1) and not pT1.issubset(pT):
                continue
            assert False, f"Template is not valid"


@ret_frozenset
def Extract(tmpl: TYPE_TEMPLATE, pT: TYPE_PATH_TEMPLATE) -> TYPE_TEMPLATE | frozenset:
    if len(pT) > 1:
        return {(Sub(pT1, Parent_D(pT)), t1) for (pT1, t1) in tmpl if pT.issubset(pT1)}
    return {(pT1, t1) for (pT1, t1) in tmpl if pT.issubset(pT1)}


@ret_frozenset
def Insert(pT: TYPE_PATH_TEMPLATE, tmplt: TYPE_TEMPLATE) -> TYPE_TEMPLATE:
    return {(Concat(pT, pT1), t1) for (pT1, t1) in tmplt}


@ret_frozenset
def Delete(tmpl: TYPE_TEMPLATE, pT: TYPE_PATH_TEMPLATE) -> TYPE_TEMPLATE | frozenset:
    return {(pT1, t) for (pT1, t) in tmpl if not pT.issubset(pT1)}


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
        ((i + 1) // 2, v) for (i, v) in pd if TypeEquals(v, TYPE_VALUE_STR)
    }

    I = {
        (i // 2, v) for (i, v) in pd if TypeEquals(v, TYPE_POSITIVE_INT)
    }

    return pT, I


@ret_frozenset
def J_inverse(p: tuple[TYPE_PATH_TEMPLATE, TYPE_PATH_INDEX]) -> TYPE_PATH_DATA:
    pT, I = p
    assert_is_template_path(pT)
    assert_is_index_path(I)
    return {(2 * i - 1, v) for (i, v) in pT} | {(2 * i, v) for (i, v) in I}


@ret_frozenset
def Split(d: TYPE_DOCUMENT) -> TYPE_DATA_SPLIT:
    return {(J(pd), v) for (pd, v) in flatten(d)}


def Type(value: TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER) -> _TYPE[
    TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER]:
    if isinstance(value, (int,float)):
        return float
    return type(value)


@ret_frozenset
def Template(d: TYPE_TEMPLATE) -> TYPE_TEMPLATE:
    return {(pT, Type(v)) for ((pT, I), v) in Split(d)}


@ret_frozenset
def Full(tmplt: TYPE_TEMPLATE) -> set:
    return tmplt | BigUnion(CartesianProduct(Parents(pT) - {pT}, {TYPE_VALUE_CONTAINER}) for (pT, t) in tmplt)


@ret_frozenset
def Nested_t(tmplt: TYPE_TEMPLATE):
    full_t = Full(tmplt)

    def E_t(pT: TYPE_PATH_TEMPLATE, t):
        if t == TYPE_VALUE_CONTAINER:
            return (pT, frozenset({E_t(pT1, t1) for (pT1, t1) in full_t if pT1 != pT and pT == Parent_D(pT1)}))
        else:
            return (pT, t)

    return {E_t(pT, t) for (pT, t) in Full(tmplt) if len(pT) == 1}


@ret_frozenset
def T_ref_bar(t: TYPE_TEMPLATE, crefs: set[TYPE_REF]) -> TYPE_TEMPLATE:
    assert_is_template(t)
    return BigUnion(Insert(pT1, Extract(t, pT2)) for (pT1, pT2) in crefs)


@ret_frozenset
def T_ref_n(t: TYPE_TEMPLATE, crefs: set[TYPE_REF], n) -> TYPE_TEMPLATE:
    if n > 1:
        return T_ref_bar(T_ref_n(t, crefs, n - 1), crefs) | t
    else:
        return T_ref_bar(t, crefs) | t


@ret_frozenset
def K(tmplt: TYPE_TEMPLATE, max_index) -> TYPE_DATA_SPLIT:
    random.seed(time.time())
    # we are not doing powerset here as it will explode in size.
    # instead, we randomly form 3 subsets
    return BigUnion(CartesianProduct(
        CartesianProduct(
            {pT}, I_n(len(pT), max_index=max_index)
        ),
        # apparently we cannot use the infinite domains of strings and numbers
        # so we limit the domains to 10 values each
        random_atomic_values(t, count=10)
    ) for (pT, t) in tmplt)


@ret_frozenset
def DataSplit(tmplt: TYPE_TEMPLATE, max_index=3) -> TYPE_DATA_SPLIT:
    assert_is_template(tmplt)
    # we don't generate the powerset of K, as it will be too large.
    # instead, we randomly choose a subset to form one document that does not have missing fields.
    _dict = {a: (a,b) for (a,b) in K(tmplt, max_index)}
    return _dict.values()


@ret_frozenset
def DataFlattenedSample(tmplt: TYPE_TEMPLATE, max_index) -> TYPE_DATA_FLATTENED:
    return {(J_inverse(pD), v) for (pD, v) in DataSplit(tmplt, max_index)}
