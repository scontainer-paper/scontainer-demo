from datamodel.common import TYPE_ARRAY, TYPE_VALUE_STR, TYPE_VALUE_NUM, TYPE_VALUE_BOOL, TYPE_VALUE_CONTAINER, \
    ret_frozenset


# from itertools import chain, combinations  # The only external library used in this program
# def powerset(iterable: set):
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


@ret_frozenset
def Pi_1(pairs: set[tuple[int, TYPE_ARRAY]]) -> set[
    TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER]:
    return {a for (a, b) in pairs}


@ret_frozenset
def Pi_2(pairs: set[tuple[int, TYPE_ARRAY]]) -> set[
    TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER]:
    return {b for (a, b) in pairs}


@ret_frozenset
def CartesianProduct(x: set | frozenset, y: set | frozenset) -> set[tuple]:
    return {(t1, t2) for t1 in x for t2 in y}
