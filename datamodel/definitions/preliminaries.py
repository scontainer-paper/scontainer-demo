from datamodel.common import TYPE_COMPONENTS, TYPE_VALUE_STR, TYPE_VALUE_NUM, TYPE_VALUE_BOOL, TYPE_VALUE_CONTAINER, \
    ret_frozenset


# from itertools import chain, combinations  # The only external library used in this program
# def powerset(iterable: set):
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def pi_1(pair: tuple):
    return pair[0]


def pi_2(pair: tuple):
    return pair[1]


@ret_frozenset
def Pi_1(pair: tuple[int, TYPE_COMPONENTS]) -> set[
    TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER]:
    return {pi_1(x) for x in pair}


@ret_frozenset
def Pi_2(pair: tuple[int, TYPE_COMPONENTS]) -> set[
    TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL | TYPE_VALUE_CONTAINER]:
    return {pi_2(x) for x in pair}


@ret_frozenset
def CartesianProduct(x: set | frozenset, y: set | frozenset) -> set[tuple]:
    return {(t1, t2) for t1 in x for t2 in y}
