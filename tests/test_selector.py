#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest
from unittest.mock import MagicMock
from gauge_web_app_steps.selector import SelectKey, Selector


class TestSelector(unittest.TestCase):

    def test_to_enum(self):
        key = SelectKey.to_enum("visible text")
        self.assertEqual(SelectKey.VISIBLE_TEXT, key)

    def test_to_enum_invalid(self):
        self.assertRaises(AssertionError, lambda: SelectKey.to_enum())

    def test_select_index(self):
        elm = MagicMock()
        Selector._select(elm, 0)
        self.assertTrue(elm.select_by_index(0))

    def test_select_value(self):
        elm = MagicMock()
        Selector._select(elm, 0, SelectKey.VALUE)
        self.assertTrue(elm.select_by_value(0))

    def test_select_visible_text(self):
        elm = MagicMock()
        Selector._select(elm, 0, SelectKey.VISIBLE_TEXT)
        self.assertTrue(elm.select_by_visible_text(0))


if __name__ == '__main__':
    unittest.main()
