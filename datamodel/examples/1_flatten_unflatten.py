import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.data import *


def eg_flatten_and_unflatten_a_document():
    # we'll first use unflatten to create a document as it's cumbersome to compose a document by hand
    d = {
        (s2path("<a,1,b,1,c,1>"), 1),
        (s2path("<a,1,b,1,c,2>"), 1.2),
        (s2path("<a,1,b,2,c,2>"), 3.14),
        (s2path("<a,1,b,2,d,2>"), "hello"),
        (s2path("<a,2,b,1,c,1>"), 9.9),
        (s2path("<a,2,e,1>"), True),
        (s2path("<f,1>"), "world"),
    }

    # unflatten the data
    d = Nested(d)
    print('Original Document: ')
    pprint(d)
    print('--' * 50)

    # G(d)
    g_d = G(d)
    print('G(d): ')
    pprint(g_d)
    print('--' * 50)

    # Flatten(d)
    flattened_d = flatten(d)
    print('Flatten(d): ')
    pprint(flattened_d)
    print('--' * 50)
    print('Pretty print Flatten(d): ')
    pprint_flattened_data(flattened_d)
    print('--' * 50)


    # Unflatten(d), which should be the same as d
    unflattened_d = Nested(flattened_d)
    print('Unflatten(d): ')
    pprint(unflattened_d)
    print('--' * 50)
    assert unflattened_d == d  # will pass as Unflatten(d) equals d


if __name__ == "__main__":
    eg_flatten_and_unflatten_a_document()
