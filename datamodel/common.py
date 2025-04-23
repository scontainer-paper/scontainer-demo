import json
import random
import re
from functools import wraps
from pprint import pprint  # noqa
from typing import Type as _Type

TYPE_PATH = set[tuple[int, str | int]]
TYPE_PATH_DATA = set[tuple[int, str | int]]
TYPE_PATH_INDEX = set[tuple[int, int]]
TYPE_PATH_TEMPLATE = set[tuple[int, str]]
TYPE_VALUE_STR = str
TYPE_VALUE_INT = int
TYPE_VALUE_NUM = int | float
TYPE_VALUE_BOOL = bool
TYPE_POSITIVE_INT = int
TYPE_ATOMIC_VALUE = TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL
TYPE_COMPONENTS = set[
    tuple[int, TYPE_VALUE_NUM | TYPE_VALUE_STR | TYPE_VALUE_BOOL | _Type['TYPE_VALUE_CONTAINER']]]
TYPE_VALUE_CONTAINER = set[tuple[str, set[TYPE_COMPONENTS]]]
TYPE_DATA = TYPE_VALUE_CONTAINER  # A piece of data is just the field value of a container (Definition 4)
TYPE_DATA_FLATTENED = set[tuple[TYPE_PATH_DATA, TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL]]
TYPE_DATA_SPLIT = set[
    tuple[tuple[TYPE_PATH_TEMPLATE], TYPE_PATH_INDEX], TYPE_VALUE_STR | TYPE_VALUE_NUM | TYPE_VALUE_BOOL]
TYPE_TEMPLATE = tuple[TYPE_PATH_TEMPLATE, _Type[TYPE_VALUE_STR] | _Type[TYPE_VALUE_NUM] | _Type[TYPE_VALUE_BOOL]]
TYPE_TEMPLATE_FIELD = tuple[
    TYPE_PATH_TEMPLATE, _Type[TYPE_VALUE_STR] | _Type[TYPE_VALUE_NUM] | _Type[TYPE_VALUE_BOOL] | TYPE_VALUE_CONTAINER]
TYPE_TEMPLATE_FULL = tuple[
    TYPE_PATH_TEMPLATE, _Type[TYPE_VALUE_STR] | _Type[TYPE_VALUE_NUM] | _Type[TYPE_VALUE_BOOL] | _Type[
        TYPE_VALUE_CONTAINER]]
TYPE_RELATION = set[tuple[TYPE_PATH_DATA, TYPE_PATH_DATA]]
TYPE_QUOTIENT_SET = set[frozenset[TYPE_PATH]]

_DATA_LINE_REGEX = re.compile(r'^<([^\s<>]+)>,[ ]?(.+)')
_DATA_PATH_REGEX = re.compile(r'^[^\s,]+,[1-9]\d*(,[^\s,]+,[1-9]\d*)*$')
EMPTY_SET = frozenset()
TYPE_EMPTY_SET = frozenset
TYPE_REF = tuple[TYPE_PATH_TEMPLATE, TYPE_PATH_TEMPLATE]


def type_name(_type):
    if _type in (int, float, int | float):
        return 'Num'
    if _type == str:
        return 'String'
    if _type == bool:
        return 'Bool'
    if _type == TYPE_VALUE_CONTAINER:
        return 'D'
    return str(_type)


def flattened_data_from_string(data_string) -> TYPE_DATA_FLATTENED:
    """
    Parse a string into a data. (a set of fields)
    :param data_string:
    :return:
    """
    lines = []
    data_flattened = set()
    for line in data_string.splitlines():
        if line.strip():
            lines.append(line)
        # every line should be a pair (<Data Path>, Atomic Value), with no parentheses
        match = _DATA_LINE_REGEX.match(line)
        if match is None:
            raise ValueError(
                f'Invalid data line {line}. Each line should be a pair: (<data path>, atomic value). (with <> and without parentheses). '
                f'For example: <a,1,b,2>, "abc"')
        data_path = match.group(1)

        data_path_match = _DATA_PATH_REGEX.match(data_path)
        if not data_path_match:
            raise ValueError(f"Invalid data path: {data_path}")
        data_path = data_path_match.group(0)
        atomic_value = match.group(2)
        # Case-insensitive boolean literals
        if atomic_value.strip().upper() == "TRUE":
            atomic_value = 'True'
        elif atomic_value.strip().upper() == "FALSE":
            atomic_value = 'False'
        try:
            # Just for the sake of simplicity
            # No need to consider the risk of eval() since this is only for demonstration purposes.
            atomic_value = eval(atomic_value)
        except (NameError, SyntaxError, ValueError, TypeError, ValueError):
            raise ValueError(f'{atomic_value} is not a valid atomic value. For strings, please add quotes.')

        data_flattened.add((data_path, atomic_value))

    return data_flattened


def ret_frozenset(func):
    """
    Decorator to return a frozenset of the result of the function.
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, tuple):
            return tuple(frozenset(t) for t in res)
        return frozenset(res)

    return wrapper


TypeEquals = isinstance

BigUnion = frozenset.union


@ret_frozenset
def BigUnion(_set):
    union = set()
    for t in _set:
        union |= t
    return union


@ret_frozenset
def s2path(s: str) -> TYPE_PATH:
    """
    Given a path denoted as <a, b, c>, return the set {(1, a), (2, b), (3, c)}
    :param s:
    :return:
    """
    res = set()
    s = s.replace('.', ',')
    if not s.startswith('<') or not s.endswith('>'):
        raise ValueError(f"String {s} does not represent a path")
    for i, char in enumerate(s[1:-1].strip().split(',')):
        chr = char.strip()
        if (i + 1) % 2 == 0 and chr in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            chr = int(chr)
        res.add((i + 1, chr))
    return res


def path2s(p: TYPE_PATH, api=False) -> str:
    if api:
        return [str(x[1]) for x in sorted(p)][-1]
    return f"<{','.join([str(x[1]) for x in sorted(p)])}>"


def data_to_dict(data: TYPE_DATA | TYPE_ATOMIC_VALUE) -> dict | TYPE_ATOMIC_VALUE:
    res = {}
    for field in data:
        children = []
        field_name = field[0]
        components = field[1]
        for child in components:
            index = child[0]
            value = child[1]
            if TypeEquals(value, TYPE_ATOMIC_VALUE):
                children.append(child)
            else:
                children.append((index, data_to_dict(value)))
        children = [x[1] for x in sorted(children, key=lambda x: x[0])]
        res[field_name] = children

    return res


def data_to_dict_with_multi_value_option(data: TYPE_DATA | TYPE_ATOMIC_VALUE):
    res = {}
    for field in data:
        children = []
        field_name = field[0]
        components = field[1]
        for child in components:
            index = child[0]
            value = child[1]
            if TypeEquals(value, TYPE_ATOMIC_VALUE):
                children.append(child)
            else:
                children.append((index, data_to_dict_with_multi_value_option(value)))
        children = [x[1] for x in sorted(children, key=lambda x: x[0])]
        if len(children) == 1:
            res[field_name] = children[0]
        else:
            res[field_name] = children

    return res


def pprint_template(template: TYPE_TEMPLATE, do_print=True):
    max_field_length = 0
    temp = []
    for field in template:
        field_name = field[0]
        ppath = path2s(field_name)
        if len(ppath) > max_field_length:
            max_field_length = len(ppath)
        field_type = field[1]
        temp.append((ppath, field_type))
    temp.sort(key=lambda x: x[0])
    res = []
    for ppath, field_type in temp:
        if do_print:
            print(f'{ppath:>{max_field_length}}: {type_name(field_type)}')
        res.append([ppath, field_type])

    return res


def pprint_split_data(d: TYPE_DATA):
    res = []
    for (pT, I), value in d:
        res.append(((path2s(pT), path2s(I)), value))
    res.sort(key=lambda x: x[0])
    for (pT, I), value in res:
        print(f'({pT}, {I}): {value}')


def pprint_flattened_data(d: TYPE_DATA_FLATTENED):
    res = []
    for tau in d:
        res.append((path2s(tau[0]), tau[1]))
    res.sort(key=lambda x: x[0])
    for tau in res:
        print(f'{tau[0]}: {tau[1]}')


def pprint_nested_template(template: set, do_print=True, api=False):
    """
    Pretty print a template
    :param template:
    :return:
    """

    def _recursive(item: tuple):
        if TypeEquals(item[1], frozenset):
            res = {}
            for child_field in item[1]:
                res.update(_recursive(child_field))
            return {path2s(item[0], api): res}
        else:
            return {path2s(item[0], api): type_name(item[1])}

    _dict = {}
    for field in template:
        _dict.update(_recursive(field))
    if do_print:
        print(json.dumps(_dict, indent=2))
    return _dict


def random_atomic_value(_type: type[TYPE_ATOMIC_VALUE]):
    if _type == TYPE_VALUE_NUM:
        return random.choice([random.randint(0, 100), random.uniform(0, 100)])
    if _type == TYPE_VALUE_STR:
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6))
    if _type == TYPE_VALUE_BOOL:
        return random.choice([True, False])


def random_atomic_values(_type: type[TYPE_ATOMIC_VALUE], count):
    res = []
    for _ in range(count):
        if _type in (TYPE_VALUE_NUM, TYPE_VALUE_BOOL, TYPE_VALUE_STR):
            res.append(random_atomic_value(_type))
    return res


def split_data_to_dict(data: TYPE_DATA_SPLIT, format=False) -> dict | str:
    res = {}
    sorted_res = []
    for tau in data:
        (pT, I), value = tau
        res[(pT, I)] = value
        sorted_res.append(((path2s(pT), path2s(I)), value))
    if not format:
        return res

    sorted_res.sort(key=lambda x: x[0])
    res_str = ""
    for item in sorted_res:
        res_str += f"({item[0][0]}, {item[0][1]}): {item[1]}\n"
    return res_str
