import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from datamodel.definitions.template import *


def eg_template_operations_extract():
    template = {
        (s2path("<a, b, c>"), TYPE_VALUE_NUM),
        (s2path("<a, f>"), TYPE_VALUE_STR),
        (s2path("<a, d>"), TYPE_VALUE_BOOL),
        (s2path("<f>"), TYPE_VALUE_NUM),
    }
    print('Original Template: ')
    pprint_template(template)
    print('Extract <a,b>: ')
    extracted = Extract(template, s2path("<a,b>"))
    extracted = Nested_t(extracted)
    pprint_nested_template(extracted)
    print('Extract <f>: ')
    extracted = Extract(template, s2path("<f>"))
    extracted = Nested_t(extracted)
    pprint_nested_template(extracted)
    print('Extract <a>: ')
    extracted = Extract(template, s2path("<a>"))
    extracted = Nested_t(extracted)
    pprint_nested_template(extracted)
    print('Extract <a, b, c>: ')
    extracted = Extract(template, s2path("<a, b, c>"))
    extracted = Nested_t(extracted)
    pprint_nested_template(extracted)

if __name__ == '__main__':
    eg_template_operations_extract()