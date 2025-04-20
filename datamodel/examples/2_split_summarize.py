import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.data import *
from datamodel.definitions.template import *


def eg_split_and_summarize():
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

    # Split(d)
    print("Split(d): ")
    split_d = Split(d)
    pprint(split_d)
    print('--' * 50)

    # Summarize
    # Template(d)
    print("Template(d): ")
    template = Template(d)
    pprint(template)
    print('--' * 50)

    print("Pretty print Template(d): ")
    pprint_template(template)
    print('--' * 50)


if __name__ == "__main__":
    eg_split_and_summarize()
