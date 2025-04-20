import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.template import *


def eg_template_operations_insert():
    template = {
        (s2path("<a, b, c>"), TYPE_VALUE_NUM),
        (s2path("<a, f>"), TYPE_VALUE_STR),
        (s2path("<a, d>"), TYPE_VALUE_BOOL),
        (s2path("<f>"), TYPE_VALUE_NUM),
    }
    print('Original Template: ')
    pprint_template(template)
    print('--' * 50)
    print('Insert a string field named "x" into <a, b>: ')
    inserted = Insert(s2path("<a, b>"), {(s2path("<x>"), TYPE_VALUE_STR)})
    pprint_template(inserted)
    print('Merge with the original template: ')
    merged = template | inserted
    pprint_template(merged)
    print('--' * 50)
    print('Nested Result: ')
    nested = Nested_t(merged)
    pprint_nested_template(nested)


if __name__ == '__main__':
    eg_template_operations_insert()
