from datamodel.definitions.template import *
from datamodel.schema import schema

DISCARD_KEYS = frozenset([
    '$schema', 'self', 'description', 'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum', 'multipleOf',
    'required', 'additionalProperties', 'patternProperties', 'minProperties', 'maxProperties',
    'dependencies', 'minLength', 'maxLength', 'pattern', 'format', 'unevaluatedItems', 'minContains',
    'maxContains', 'unevaluatedProperties', 'default', 'examples', 'minItems', 'maxItems',
    'uniqueItems', 'discriminator', 'readOnly', 'writeOnly', 'deprecated', 'title', 'description',
    'examples', 'contentEncoding', 'contentMediaType', 'contentSchema', 'contentMediaType',
    'minProperties', 'maxProperties', 'propertyNames', 'if', 'then', 'else',
    'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum', 'multipleOf',
])

_TYPE_STRING_TYPE_MAP = {
    'string': TYPE_VALUE_STR,
    'integer': TYPE_VALUE_INT,
    'number': TYPE_VALUE_NUM,
    'boolean': TYPE_VALUE_BOOL,
}


@ret_frozenset
def handle_array(field_name, value: dict) -> TYPE_TEMPLATE:
    if 'prefixItems' in value:
        raise NotImplementedError("prefixItems is not supported")
    if TypeEquals(value.get('items'), list):
        raise Exception("items as an array is not supported")
    if 'contains' in value:
        raise NotImplementedError("contains is not supported")
    sub_field_item = value['items']
    sub_field_type = sub_field_item['type']
    fields = set()
    if sub_field_type == 'object':
        # handle object
        fields.add(handle_object(field_name, sub_field_item))
    elif sub_field_type == 'array':
        # handle array
        fields.add(handle_array(field_name, sub_field_item))
    else:
        # handle atomic types
        fields.add(handle_atomic(field_name, sub_field_item))
    assert len(fields) == 1
    if len(fields) > 1:
        # generator
        raise Exception("generator is not supported")

    return fields.pop()


def handle_element_of_any_of(field_name, value: dict):
    pass


@ret_frozenset
def handle_atomic(field_name, value: dict) -> TYPE_TEMPLATE:
    for key in DISCARD_KEYS:
        value.pop(key, None)
    return {(s2path(f'<{field_name}>'), _TYPE_STRING_TYPE_MAP[value['type']])}


@ret_frozenset
def handle_object(field_name, item: dict) -> TYPE_TEMPLATE:
    if 'enum' in item:
        # type is enum
        _type = type(item['enum'])
    for key in DISCARD_KEYS:
        item.pop(key, None)
    fields = set()
    # handle properties
    for sub_field_name, item_object in item.get('properties').items():
        item_type = item_object.get('type')
        if not item_type:
            # no type, so there must be an anyOf or oneOf
            raise NotImplementedError("anyOf and oneOf are not supported")
        if item_type == 'object':
            fields |= handle_object(sub_field_name, item_object)
        elif item_type == 'array':
            fields |= handle_array(sub_field_name, item_object)
        else:
            # handle atomic types
            fields |= handle_atomic(sub_field_name, item_object)
    if field_name:
        return Insert(s2path(f'<{field_name}>'), fields)
    return fields


print(handle_object(None, schema))
