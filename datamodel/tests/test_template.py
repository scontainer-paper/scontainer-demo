import unittest

from datamodel.definitions.template import *


class TestTemplate(unittest.TestCase):
    def test_J_splits_path_data_correctly(self):
        pd = {(1, "name"), (2, 1), (3, "age"), (4, 2)}
        expected_pt = {(1, "name"), (2, "age")}
        expected_pi = {(1, 1), (2, 2)}
        pt, pi = J(pd)
        self.assertEqual(pt, expected_pt)
        self.assertEqual(pi, expected_pi)

    def test_J_with_non_data_path(self):
        with self.assertRaises(AssertionError):
            J({(1, "name"), (2, "age")})
        with self.assertRaises(AssertionError):
            J({(1, 1), (2, 2)})
        with self.assertRaises(AssertionError):
            J(EMPTY_SET)

    def test_assert_template_ok(self):
        template = {
            (s2path("<a, b>"), int),
            (s2path("<a, c>"), str),
        }
        # No exception should be raised
        assert_is_template(template)
        template = {
            (s2path("<a, b, c>"), TYPE_VALUE_NUM),
            (s2path("<a, d>"), TYPE_VALUE_NUM),
            (s2path("<f>"), TYPE_VALUE_NUM),
        }
        # No exception should be raised
        assert_is_template(template)

    def test_assert_template_same_path_with_multi_types(self):
        template = {
            (s2path("<a, b>"), int),
            (s2path("<a, b>"), str),
        }
        with self.assertRaises(AssertionError):
            assert_is_template(template)

    def test_assert_template_one_path_is_subset_of_another(self):
        template = {
            (s2path("<a, b>"), int),
            (s2path("<a, b, c>"), str),
        }
        with self.assertRaises(AssertionError):
            assert_is_template(template)
        template = {
            (s2path("<a, b>"), int),
            (s2path("<a, c>"), str),
            (s2path("<a, c>"), set),
        }
        with self.assertRaises(AssertionError):
            assert_is_template(template)

    def test_insert_OK(self):
        new_path = s2path("<a, b>")
        template = {
            (s2path("<a, b>"), int),
            (s2path("<a, c>"), str),
        }
        expected = {
            (s2path("<a, b, a, b>"), int),
            (s2path("<a, b, a, c>"), str),
        }
        self.assertEqual(Insert(new_path, template), expected)

    def test_extract_OK(self):
        template = {
            (s2path("<a,b,c,d>"), int),
            (s2path("<a,b,e>"), str),
            (s2path("<a,b,c,g>"), str),
        }
        p1 = s2path("<a,b>")
        expected = {
            (s2path("<b,c,d>"), int),
            (s2path("<b,c,g>"), str),
            (s2path("<b,e>"), str),
        }
        self.assertEqual(Extract(template, p1), expected)
        p2 = s2path("<a,b,c>")
        expected = {
            (s2path("<c,d>"), int),
            (s2path("<c,g>"), str),
        }
        self.assertEqual(Extract(template, p2), expected)
        p3 = s2path("<a>")
        expected = template
        self.assertEqual(Extract(template, p3), expected)

    def test_extract_no_children(self):
        template = {
            (s2path("<a,b,c,d>"), int),
            (s2path("<a,b,e>"), str),
            (s2path("<a,b,c,g>"), str),
        }
        expected = {
            (s2path("<d>"), int),
        }
        self.assertEqual(Extract(template, s2path('<a,b,c,d>')), expected)

    def test_extract_result_empty(self):
        template = {
            (s2path("<a,b,c,d>"), int),
            (s2path("<a,b,e>"), str),
            (s2path("<a,b,c,g>"), str),
        }
        self.assertEqual(Extract(template, s2path('<b>')), EMPTY_SET)
        self.assertEqual(Extract(template, s2path('<a,b,c,d,e>')), EMPTY_SET)
        self.assertEqual(Extract(template, s2path('<a,c>')), EMPTY_SET)

    def test_delete_ok(self):
        template = {
            (s2path("<a,b,c,d>"), int),
            (s2path("<a,b,e>"), str),
            (s2path("<a,b,c,g>"), str),
            (s2path("<b,c,g>"), str),
        }
        p1 = s2path("<a,b>")
        expected = {
            (s2path("<b,c,g>"), str),
        }
        self.assertEqual(Delete(template, p1), expected)
        p2 = s2path("<a,b,c>")
        expected = {
            (s2path("<a,b,e>"), str),
            (s2path("<b,c,g>"), str),
        }
        self.assertEqual(Delete(template, p2), expected)
        p3 = s2path("<a,b,c,d>")
        expected = {
            (s2path("<a,b,e>"), str),
            (s2path("<a,b,c,g>"), str),
            (s2path("<b,c,g>"), str),
        }
        self.assertEqual(Delete(template, p3), expected)

    def test_delete_empty_result(self):
        template = {
            (s2path("<a,b,c,d>"), int),
            (s2path("<a,b,e>"), str),
            (s2path("<a,b,c,g>"), str),
        }
        self.assertEqual(Delete(template, s2path('<a>')), EMPTY_SET)
