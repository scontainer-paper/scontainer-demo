import unittest

from datamodel.definitions.path import *


class TestPathOperations(unittest.TestCase):

    def test_indices_not_consecutive(self):
        x = {(1, 'a'), (3, 'b')}
        with self.assertRaises(AssertionError):
            Concat(x, x)
        with self.assertRaises(AssertionError):
            Sub(x, x)

    def test_assert_is_path_with_valid_path(self):
        valid_path = {(1, 'a'), (2, 'b'), (3, 'c')}
        # No exception should be raised
        assert_is_path(valid_path)

    def test_assert_is_path_with_invalid_indices(self):
        invalid_path = {(1, 'a'), (3, 'b'), (4, 'c')}
        with self.assertRaises(AssertionError):
            assert_is_path(invalid_path)

    def test_assert_is_path_with_duplicate_indices(self):
        invalid_path = {(1, 'a'), (1, 'b'), (2, 'c')}
        with self.assertRaises(AssertionError):
            assert_is_path(invalid_path)

    def test_Concat_empty_paths(self):
        with self.assertRaises(AssertionError):
            Concat(EMPTY_SET, EMPTY_SET)

    def test_Sub_with_empty_paths(self):
        with self.assertRaises(AssertionError):
            Sub(EMPTY_SET, EMPTY_SET)

    def test_Sub_when_y_equals_x(self):
        x = {(1, 'a'), (2, 'b')}
        self.assertEqual(Sub(x, x), x)

    def test_Sub_when_irrelevant(self):
        x = {(1, 'a'), (2, 'b')}
        y = {(1, 'f'), (2, 'g')}
        self.assertEqual(Sub(x, y), x)

    def test_Sub_OK(self):
        x = {(1, 'a'), (2, 'b'), (3, 'c')}
        y = {(1, 'a'), (2, 'b')}
        self.assertEqual(Sub(x, y), {(1, 'c')})

    def test_Concat_OK(self):
        x = {(1, 'a'), (2, 1)}
        y = {(1, 'c'), (2, 2)}
        self.assertEqual(Concat(x, y), {(1, 'a'), (2, 1), (3, 'c'), (4, 2)})

    def test_assert_is_template_path_with_valid_template_path(self):
        valid_template_path = {(1, 'a'), (2, 'b'), (3, 'c'), (4,'d')}
        assert_is_template_path(valid_template_path)

    def test_assert_is_template_path_with_invalid_template_path(self):
        invalid_template_path = {(1, 'a'), (2, 123), (3, 'c')}
        with self.assertRaises(AssertionError):
            assert_is_template_path(invalid_template_path)

    def test_assert_is_data_path_with_valid_data_path(self):
        valid_data_path = {(1, 'a'), (2, 1), (3, 'b'), (4, 2)}
        assert_is_data_path(valid_data_path)

    def test_assert_is_data_path_with_invalid_data_path(self):
        invalid_data_path = {(1, 'a'), (2, 'b'), (3, 'c')}
        with self.assertRaises(AssertionError):
            assert_is_data_path(invalid_data_path)

        invalid_data_path = {(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')}
        with self.assertRaises(AssertionError):
            assert_is_data_path(invalid_data_path)

    def test_assert_is_index_path_with_valid_index_path(self):
        valid_index_path = {(1, 1), (2, 2), (3, 3)}
        assert_is_index_path(valid_index_path)

    def test_assert_is_index_path_with_invalid_index_path(self):
        invalid_index_path = {(1, 'a'), (2, 'b'), (3, 'c')}
        with self.assertRaises(AssertionError):
            assert_is_index_path(invalid_index_path)

    def test_direct_path_OK(self):
        x = s2path('<a,b,c,d>')
        expected = s2path('<a,b,c>')
        self.assertEqual(Parent_D(x), expected)

    def test_direct_path_is_self(self):
        x = s2path('<a>')
        self.assertEqual(Parent_D(x), x)
