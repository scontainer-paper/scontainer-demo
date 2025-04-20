import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.template import *


def eg_template_operations_move():
    template = {
        (s2path("<a, b, c>"), TYPE_VALUE_NUM),
        (s2path("<a, f>"), TYPE_VALUE_STR),
        (s2path("<a, d>"), TYPE_VALUE_BOOL),
        (s2path("<f>"), TYPE_VALUE_NUM),
    }
    print('Original Template: ')
    pprint_template(template)
    print('--' * 50)
    print('Move <a, f> into <a, b>: ')
    moved = Mv(template, s2path("<a, f>"), s2path("<a, b>"))
    print('Result: ')
    pprint_template(moved)
    print('--' * 50)
    print('Before moving:')
    nested = Nested_t(template)
    pprint_nested_template(nested)
    print('--' * 50)
    print('After moving:')
    moved_nested = Nested_t(moved)
    pprint_nested_template(moved_nested)


if __name__ == '__main__':
    eg_template_operations_move()
