import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.template import *


def eg_template_operations_nested():
    template = {
        (s2path("<a, b, c>"), TYPE_VALUE_NUM),
        (s2path("<a, f>"), TYPE_VALUE_STR),
        (s2path("<a, d>"), TYPE_VALUE_BOOL),
        (s2path("<f>"), TYPE_VALUE_NUM),
    }
    print('Original Template: ')
    pprint_template(template)
    print('--' * 50)
    nested_template = Nested_t(template)
    print('Nested Template: ')
    pprint_nested_template(nested_template)


if __name__ == '__main__':
    eg_template_operations_nested()
   