#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import unittest

from parameterized import parameterized
from unittest.mock import patch

from gauge_web_app_steps.driver import Browser, OperatingSystem, SaucelabsOperatingSystem
from gauge_web_app_steps.driver.driver_factory import LocalDriverFactory, SaucelabsDriverFactory


class TestLocalDriverFactory(unittest.TestCase):

    @parameterized.expand([(OperatingSystem.ANDROID, Browser.SAFARI), (OperatingSystem.IOS, Browser.CHROME)])
    def test_create_unsupported_configuration(self, operating_system: OperatingSystem, browser: Browser):
        # arrange
        with patch.dict(os.environ, {
            "driver_operating_system": operating_system.value,
            "driver_browser": browser.value
        }):
            # act & assert
            self.assertRaises(AssertionError, lambda: LocalDriverFactory().create_driver())


class TestSaucelabsDriverFactory(unittest.TestCase):

    @parameterized.expand([
        (OperatingSystem.ANDROID, True),
        (OperatingSystem.IOS, True),
        (OperatingSystem.WINDOWS, False),
        (OperatingSystem.MACOS, False),
        (OperatingSystem.LINUX, False)
    ])
    def test__get_sauce_options__appium_version(self, operating_system: OperatingSystem, should_have_appium_version: bool):
        # arrange
        with patch.dict(os.environ, {
            "driver_platform_saucelabs_mobile_appium_version": "appium-version",
            "driver_operating_system": operating_system.value
        }):
            # act
            result = SaucelabsDriverFactory("test")._get_sauce_options()
            # assert
            self.assertEqual(should_have_appium_version, "appiumVersion" in result,
                f"result has appium version: {result}, OS: {operating_system}, is mobile: {operating_system.is_mobile()}")

    @parameterized.expand([("tunnel-name", True), (None, False)])
    def test__get_sauce_options__tunnel_name(self, tunnel_name: str, should_have_tunnel_name: bool):
        # arrange
        with patch.dict('os.environ'):
            if tunnel_name is not None: os.environ["driver_platform_saucelabs_tunnel_name"] = tunnel_name
            else: os.environ.pop("driver_platform_saucelabs_tunnel_name", None)
            # act
            result = SaucelabsDriverFactory("test")._get_sauce_options()
            # assert
            self.assertEqual(should_have_tunnel_name, "tunnelIdentifier" in result, f"tunnel name was in the result: {result}")

    @parameterized.expand([
        (OperatingSystem.WINDOWS, "11", SaucelabsOperatingSystem.WINDOWS_11.value),
        (OperatingSystem.WINDOWS, "10", SaucelabsOperatingSystem.WINDOWS_10.value),
        (OperatingSystem.WINDOWS, "8.1", SaucelabsOperatingSystem.WINDOWS_8_1.value),
        (OperatingSystem.WINDOWS, "8", SaucelabsOperatingSystem.WINDOWS_8.value),
        (OperatingSystem.WINDOWS, "7", SaucelabsOperatingSystem.WINDOWS_7.value),
        (OperatingSystem.WINDOWS, "foobar", SaucelabsOperatingSystem.WINDOWS_DEFAULT.value),
        (OperatingSystem.MACOS, "12", SaucelabsOperatingSystem.MACOS_12.value),
        (OperatingSystem.MACOS, "monterey", SaucelabsOperatingSystem.MACOS_12.value),
        (OperatingSystem.MACOS, "11", SaucelabsOperatingSystem.MACOS_11.value),
        (OperatingSystem.MACOS, "big sur", SaucelabsOperatingSystem.MACOS_11.value),
        (OperatingSystem.MACOS, "big_sur", SaucelabsOperatingSystem.MACOS_11.value),
        (OperatingSystem.MACOS, "big-sur", SaucelabsOperatingSystem.MACOS_11.value),
        (OperatingSystem.MACOS, "10.15", SaucelabsOperatingSystem.MACOS_10_15.value),
        (OperatingSystem.MACOS, "10", SaucelabsOperatingSystem.MACOS_10_15.value),
        (OperatingSystem.MACOS, "catalina", SaucelabsOperatingSystem.MACOS_10_15.value),
        (OperatingSystem.MACOS, "10.14", SaucelabsOperatingSystem.MACOS_10_14.value),
        (OperatingSystem.MACOS, "mojave", SaucelabsOperatingSystem.MACOS_10_14.value),
        (OperatingSystem.MACOS, "10.13", SaucelabsOperatingSystem.MACOS_10_13.value),
        (OperatingSystem.MACOS, "high sierra", SaucelabsOperatingSystem.MACOS_10_13.value),
        (OperatingSystem.MACOS, "high_sierra", SaucelabsOperatingSystem.MACOS_10_13.value),
        (OperatingSystem.MACOS, "high-sierra", SaucelabsOperatingSystem.MACOS_10_13.value),
        (OperatingSystem.MACOS, "10.12", SaucelabsOperatingSystem.MACOS_10_12.value),
        (OperatingSystem.MACOS, "sierra", SaucelabsOperatingSystem.MACOS_10_12.value),
        (OperatingSystem.MACOS, "10.11", SaucelabsOperatingSystem.MACOS_10_11.value),
        (OperatingSystem.MACOS, "el capitan", SaucelabsOperatingSystem.MACOS_10_11.value),
        (OperatingSystem.MACOS, "el_capitan", SaucelabsOperatingSystem.MACOS_10_11.value),
        (OperatingSystem.MACOS, "el-capitan", SaucelabsOperatingSystem.MACOS_10_11.value),
        (OperatingSystem.MACOS, "10.10", SaucelabsOperatingSystem.MACOS_10_10.value),
        (OperatingSystem.MACOS, "yosemite", SaucelabsOperatingSystem.MACOS_10_10.value),
        (OperatingSystem.MACOS, "foobar", SaucelabsOperatingSystem.MACOS_DEFAULT.value),
    ])
    def test__get_platform_name(self, operating_system: OperatingSystem, operating_system_version: str, expected_value: str):
        result = SaucelabsDriverFactory("test")._get_platform_name(operating_system, operating_system_version)
        self.assertEqual(expected_value, result)


if __name__ == '__main__':
    unittest.main()
