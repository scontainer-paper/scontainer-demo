import json
import random
import sys
import time

from jsonschema import exceptions
from jsonschema.validators import validator_for

BATCH_NUM = 700000

variable_data = []
fixed_data = []
with open(f'datasets/A-schema-variable.json', 'r') as f:
    schema_A_variable = json.load(f)
with open(f'datasets/A-schema-variable-anyOf.json', 'r') as f:
    schema_A_variable_any_of = json.load(f)
with open(f'datasets/A-schema-fixed.json', 'r') as f:
    schema_A_fixed = json.load(f)


def generate_data():
    for i in range(BATCH_NUM):
        choices = [
            {'obj': {
                'b': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
                'c': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
            }},
            {'str': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))},
            {'num': random.randint(1, 100)}
        ]
        choice = random.choice(choices)
        variable_data.append({'a': list(choice.values())[0]})
        fixed_data.append({'a': choice})
    with open(f'datasets/A-dataset-{BATCH_NUM}-variable.json', 'w') as f:
        json.dump(variable_data, f, indent=2)
    with open(f'datasets/A-dataset-{BATCH_NUM}-fixed.json', 'w') as f:
        json.dump(fixed_data, f, indent=2)


def run_test(include_load_time: bool):
    cls_A_variable = validator_for(schema_A_variable)
    cls_A_variable.check_schema(schema_A_variable)
    schema_A_variable_validator = cls_A_variable(schema_A_variable)

    cls_A_variable_any_of = validator_for(schema_A_variable_any_of)
    cls_A_variable_any_of.check_schema(schema_A_variable_any_of)
    schema_A_variable_any_of_validator = cls_A_variable_any_of(schema_A_variable_any_of)

    cls_A_fixed = validator_for(schema_A_fixed)
    cls_A_fixed.check_schema(schema_A_fixed)
    schema_A_fixed_validator = cls_A_fixed(schema_A_fixed)

    start = time.time()
    with open(f'datasets/A-dataset-{BATCH_NUM}-variable.json', 'r') as f:
        variable_data = json.load(f)
    load_time_variable = time.time() - start
    start = time.time()
    for d in variable_data:
        error = exceptions.best_match(schema_A_variable_validator.iter_errors(d))
        if error is not None:
            raise error
    validation_time_variable = time.time() - start

    start = time.time()
    for d in variable_data:
        error = exceptions.best_match(schema_A_variable_any_of_validator.iter_errors(d))
        if error is not None:
            raise error
    validation_time_variable_any_of = time.time() - start

    start = time.time()
    with open(f'datasets/A-dataset-{BATCH_NUM}-fixed.json', 'r') as f:
        fixed_data = json.load(f)
    load_time_fixed = time.time() - start
    if not include_load_time:
        start = time.time()
    for d in fixed_data:
        error = exceptions.best_match(schema_A_fixed_validator.iter_errors(d))
        if error is not None:
            raise error
    validation_time_fixed = time.time() - start

    return {
        'load_time_variable': load_time_variable,
        'load_time_fixed': load_time_fixed,
        'validation_time_variable': validation_time_variable,
        'validation_time_variable_any_of': validation_time_variable_any_of,
        'validation_time_fixed': validation_time_fixed
    }


if __name__ == '__main__':
    for batch_size in (10000, 50000, 100000, 300000, 500000, 700000, 1000000):
        BATCH_NUM = batch_size
        result = run_test(include_load_time=True)
        print(f'Batch size: {BATCH_NUM}')
        print(f'Load time for variable: {result["load_time_variable"]:.3f}s')
        print(f'Load time for fixed: {result["load_time_fixed"]:.3f}s')
        print(f'Validation time for variable: {result["validation_time_variable"]:.3f}s')
        print(f'Validation time for variable anyOf: {result["validation_time_variable_any_of"]:.3f}s')
        print(f'Validation time for fixed: {result["validation_time_fixed"]:.3f}s')
        print(f'Load and validation time for variable: {result["load_time_variable"] + result["validation_time_variable"]:.3f}s')
        print(f'Load and validation time for variable anyOf: {result["load_time_variable"] + result["validation_time_variable_any_of"]:.3f}s')
        print(f'Load and validation time for fixed: {result["load_time_fixed"] + result["validation_time_fixed"]:.3f}s')

        print('-' * 50)