import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from unittest.mock import MagicMock, patch
from datamodel.definitions.template import *


def eg_coverage_of_a_template():
    template = {
        (s2path("<a, b, c>"), TYPE_VALUE_STR),
        (s2path("<a, d>"), TYPE_VALUE_NUM),
        (s2path("<f>"), TYPE_VALUE_BOOL),
    }
    # as this set is theoretically infinite,
    # we only generate a random subset that forms a document without missing fields.
    data_split = DataSplit(template, max_index=2)
    print('Sample Data (split): ')
    pprint(data_split)
    print('--' * 50)
    print('Pretty print sample data (split): ')
    pprint_split_data(data_split)
    print('--' * 50)
    # DataFlatten will call DataSplit again with different random values,
    # so we patch DataSplit to return the data above for consistency
    mock = MagicMock(return_value=data_split)
    with patch('definitions.template.DataSplit', mock):
        flattened_d = DataFlatten(template)
    print('Sample Flattened (split): ')
    pprint(flattened_d)
    print('--' * 50)
    print('Pretty print sample flattened (split): ')
    pprint_flattened_data(flattened_d)
    print('--' * 50)


if __name__ == "__main__":
    eg_coverage_of_a_template()
