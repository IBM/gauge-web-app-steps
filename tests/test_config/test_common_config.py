#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import unittest

from parameterized import parameterized
from unittest.mock import patch

from gauge_web_app_steps.config import common_config as config
from gauge_web_app_steps.driver import Browser, OperatingSystem, Platform


class TestCommonConfig(unittest.TestCase):

    def test_get_browser(self):
        with patch.dict(os.environ, {"driver_browser": "chrome"}):
            result = config.get_browser()
            self.assertEqual(Browser.CHROME, result)

    def test_get_browser_should_return_firefox_as_default_browser(self):
        result = config.get_browser()
        self.assertEqual(Browser.FIREFOX, result)

    def test_get_implicit_timeout(self):
        with patch.dict(os.environ, {"driver_implicit_timeout": "10"}):
            result = config.get_implicit_timeout()
            self.assertEqual(10, result)

    def test_get_implicit_timeout_should_return_5_as_default_value(self):
        result = config.get_implicit_timeout()
        self.assertEqual(5, result)

    def test_get_implicit_timeout_should_return_default_value(self):
        result = config.get_implicit_timeout(111)
        self.assertEqual(111, result)

    def test_get_operating_system(self):
        with patch.dict(os.environ, {"driver_operating_system": "win"}):
            result = config.get_operating_system()
            self.assertEqual(OperatingSystem.WINDOWS, result)

    def test_get_operating_system_version(self):
        with patch.dict(os.environ, {"driver_operating_system_version": "111"}):
            result = config.get_operating_system_version()
            self.assertEqual("111", result)

    def test_get_page_load_timeout(self):
        with patch.dict(os.environ, {"driver_page_load_timeout": "10"}):
            result = config.get_page_load_timeout()
            self.assertEqual(10, result)

    def test_get_page_load_timeout_should_return_30_as_default_value(self):
        result = config.get_page_load_timeout()
        self.assertEqual(30, result)

    def test_get_page_load_timeout_should_return_default_value(self):
        result = config.get_page_load_timeout(111)
        self.assertEqual(111, result)

    def test_get_platform(self):
        with patch.dict(os.environ, {"driver_platform": "saucelabs"}):
            result = config.get_platform()
            self.assertEqual(Platform.SAUCELABS, result)

    def test_get_platform_should_return_local_as_default_platform(self):
        result = config.get_platform()
        self.assertEqual(Platform.LOCAL, result)

    @parameterized.expand([
        ("True", "False", False),
        ("True", "True", True),
        ("True", None, True),
        ("False", "True", True),
        ("False", "False", False),
        ("False", None, False),
        (None, "True", True),
        (None, "False", False),
        (None, None, False),
    ])
    def test_is_headless(self, deprecated_headless, current_headless, expected_value):
        # arrange
        patched_environ = {}
        if deprecated_headless:
            patched_environ["driver_headless"] = deprecated_headless
        if current_headless:
            patched_environ["driver_platform_local_headless"] = current_headless
        with patch.dict(os.environ, patched_environ):
            # act
            result = config.is_headless()
            # assert
            self.assertEqual(expected_value, result)


if __name__ == '__main__':
    unittest.main()
