#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest

from gauge_web_app_steps.driver import Platform


class TestOperatingSystem(unittest.TestCase):

    def test_is_local(self):
        self.assertTrue(Platform.LOCAL.is_local())
        self.assertFalse(Platform.SAUCELABS.is_local())

    def test_is_remote(self):
        self.assertTrue(Platform.SAUCELABS.is_remote())
        self.assertFalse(Platform.LOCAL.is_remote())


if __name__ == '__main__':
    unittest.main()
