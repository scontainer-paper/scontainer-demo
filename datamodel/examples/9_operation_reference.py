import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.template import *


def eg_template_operations_reference():
    template = {
        (s2path("<a, b, c>"), TYPE_VALUE_NUM),
        (s2path("<a, f>"), TYPE_VALUE_STR),
        (s2path("<a, d>"), TYPE_VALUE_BOOL),
        (s2path("<x, y>"), TYPE_VALUE_BOOL),
    }
    print('Original Template: ')
    pprint_template(template)
    print('--' * 50)
    print('Dereferenced with {(<x>, <a>)}: ')
    deref_template = T_ref_n(template, {(s2path("<x>"), s2path("<a>"))}, n=1)
    print('Result: ')
    pprint_template(deref_template)
    print('--' * 50)
    print('First dereference with circular reference {(<x>, <a>), (<a>, <x>)}: ')
    deref_template = T_ref_n(template, {(s2path("<x>"), s2path("<a>")), (s2path("<a>"), s2path("<x>"))}, n=1)
    print('Result: ')
    pprint_template(deref_template)
    print('--' * 50)
    print('Second dereference with circular reference {(<x>, <a>), (<a>, <x>)}: ')
    deref_template = T_ref_n(template, {(s2path("<x>"), s2path("<a>")), (s2path("<a>"), s2path("<x>"))}, n=2)
    print('Result: ')
    pprint_template(deref_template)
    print('--' * 50)
    print('Third dereference with circular reference {(<x>, <a>), (<a>, <x>)}: ')
    deref_template = T_ref_n(template, {(s2path("<x>"), s2path("<a>")), (s2path("<a>"), s2path("<x>"))}, n=3)
    print('Result: ')
    pprint_template(deref_template)
    print('--' * 50)
    print('Nested template after 3rd dereference: ')
    nested = Nested_t(deref_template)
    pprint_nested_template(nested)


if __name__ == '__main__':
    eg_template_operations_reference()
