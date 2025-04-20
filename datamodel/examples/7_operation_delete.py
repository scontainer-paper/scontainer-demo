import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.template import *


def eg_template_operations_delete():
    template = {
        (s2path("<a, b, c>"), TYPE_VALUE_NUM),
        (s2path("<a, f>"), TYPE_VALUE_STR),
        (s2path("<a, d>"), TYPE_VALUE_BOOL),
        (s2path("<f>"), TYPE_VALUE_NUM),
    }
    print('Original Template: ')
    pprint_template(template)
    print('--' * 50)
    print('Delete <a, b>: ')
    deleted = Delete(template, s2path("<a, b>"))
    print('Result: ')
    pprint_template(deleted)
    print('--' * 50)
    print('Delete <a>: ')
    deleted = Delete(template, s2path("<a>"))
    print('Result ')
    pprint_template(deleted)


if __name__ == '__main__':
    eg_template_operations_delete()
