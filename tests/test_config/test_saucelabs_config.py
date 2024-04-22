#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import unittest

from unittest.mock import patch

from gauge_web_app_steps.config import saucelabs_config


class TestLocal(unittest.TestCase):

    def test_get_appium_version(self):
        with patch.dict(os.environ, {"driver_platform_saucelabs_mobile_appium_version": "foo-appium-version"}):
            result = saucelabs_config.get_appium_version()
            self.assertEqual("foo-appium-version", result)

    def test_get_browser_version(self):
        with patch.dict(os.environ, {"driver_platform_saucelabs_desktop_browser_version": "foo-browser-version"}):
            result = saucelabs_config.get_browser_version()
            self.assertEqual("foo-browser-version", result)

    def test_get_browser_version_should_return_latest_as_default(self):
        result = saucelabs_config.get_browser_version()
        self.assertEqual("latest", result)

    def test_get_browser_version_should_return_default(self):
        result = saucelabs_config.get_browser_version("foo-default")
        self.assertEqual("foo-default", result)

    def test_get_device_name(self):
        with patch.dict(os.environ, {"driver_platform_saucelabs_mobile_device_name": "foo-device"}):
            result = saucelabs_config.get_device_name()
            self.assertEqual("foo-device", result)

    def test_get_executor(self):
        with patch.dict(os.environ, {"driver_platform_saucelabs_executor": "foo-executor"}):
            result = saucelabs_config.get_executor()
            self.assertEqual("foo-executor", result)

    def test_get_tunnel_name(self):
        with patch.dict(os.environ, {"SAUCE_TUNNEL_NAME": "foo-tunnel"}):
            result = saucelabs_config.get_tunnel_name()
            self.assertEqual("foo-tunnel", result)


if __name__ == '__main__':
    unittest.main()
