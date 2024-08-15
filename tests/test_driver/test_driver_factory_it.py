#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import unittest

from appium.webdriver import Remote as MobileRemote
from parameterized import parameterized
from pathlib import Path
from selenium.webdriver import Chrome, Firefox, Remote
from selenium.webdriver.common.by import By
from unittest.mock import patch

from gauge_web_app_steps.driver.browsers import Browser
from gauge_web_app_steps.driver.operating_system import OperatingSystem
from gauge_web_app_steps.driver.driver_factory import LocalDriverFactory, RemoteDriverFactory, SaucelabsDriverFactory
from tests import TEST_OUT_DIR


# noinspection DuplicatedCode
@unittest.skipIf(os.environ.get("TEST_SKIP_IT", "0") == "1", "TEST_SKIP_IT env variable is set")
class TestLocalDriverFactoryIT(unittest.TestCase):

    @parameterized.expand([(Browser.CHROME, Chrome), (Browser.FIREFOX, Firefox)])
    def test_create_desktop_systems(self, browser: Browser, expected_driver):
        # arrange
        Path(f"{TEST_OUT_DIR}/logs").mkdir(exist_ok=True)
        with patch.dict(os.environ, {
            "driver_manager_selenium4": "true",
            "driver_operating_system": OperatingSystem.MACOS.value,
            "driver_browser": browser.value,
            "GAUGE_PROJECT_ROOT": TEST_OUT_DIR,
        }):
            # act
            result = LocalDriverFactory().create_driver()
            # assert
            self.assertIsNotNone(result)
            self.assertIsInstance(result, expected_driver)
            # clean up
            result.quit()

    @unittest.skipUnless(os.environ.get("driver_platform_local_mobile_appium_server_url"), "no appium url is given")
    @unittest.skipIf(os.environ.get("TEST_SKIP_ANDROID", "0") == "1", "TEST_SKIP_ANDROID env variable is set")
    def test_create_android(self):
        # arrange
        with patch.dict(os.environ, {
            "driver_operating_system": "android",
            "driver_browser": "chrome"
        }):
            # act
            result = LocalDriverFactory().create_driver()
            # assert
            self.assertIsNotNone(result)
            self.assertIsInstance(result, MobileRemote)
            # clean up
            result.quit()

    @unittest.skipUnless(os.environ.get("driver_platform_local_mobile_appium_server_url"), "no appium url is given")
    @unittest.skipIf(os.environ.get("TEST_SKIP_IOS", "0") == "1", "TEST_SKIP_IOS env variable is set")
    def test_create_ios(self):
        # arrange
        with patch.dict(os.environ, {
            "driver_browser": "safari",
            "driver_operating_system": "ios"
        }):
            # act
            result = LocalDriverFactory().create_driver()
            # assert
            self.assertIsNotNone(result)
            self.assertIsInstance(result, MobileRemote)
            # clean up
            result.quit()


@unittest.skipIf(os.environ.get("TEST_SKIP_IT", "0") == "1", "TEST_SKIP_IT env variable is set")
@unittest.skipUnless(os.environ.get("driver_platform_local_mobile_appium_server_url"), "no executor is given")
class TestRemoteDriverFactoryIT(unittest.TestCase):

    @parameterized.expand([(Browser.CHROME, Remote), (Browser.FIREFOX, Remote), (Browser.EDGE, Remote)])
    def test_remote_driver(self, browser: Browser, expected):
        # arrange
        with patch.dict(os.environ, {
            "driver_browser": browser.value
        }):
            # act
            result = RemoteDriverFactory().create_driver()
            # assert
            self.assertIsInstance(result, expected)
            # clean up
            result.quit()


@unittest.skipIf(os.environ.get("TEST_SKIP_IT", "0") == "1", "TEST_SKIP_IT env variable is set")
@unittest.skipUnless(os.environ.get("driver_platform_saucelabs_executor"), "no executor is given")
class TestSaucelabsDriverFactoryIT(unittest.TestCase):

    def test_create(self):
        # arrange
        with patch.dict(os.environ, {
            "driver_platform": "saucelabs",
            "driver_browser": "firefox",
            "driver_operating_system": "win",
            "driver_operating_system_version": "11"
        }):
            # act
            result = SaucelabsDriverFactory("test", "suite-id").create_driver()
            # assert
            self.assertIsNotNone(result)
            self.assertIsInstance(result, Remote)
            # clean up
            result.quit()

    @unittest.skipUnless(os.environ.get("driver_platform_saucelabs_tunnel_name"), "no tunnel name is given")
    def test_create_tunneled(self):
        # arrange
        with patch.dict(os.environ, {
            "driver_platform": "saucelabs",
            "driver_browser": "firefox",
            "driver_operating_system": "win",
            "driver_operating_system_version": "11"
        }):
            # act
            result = SaucelabsDriverFactory("test", "suite-id").create_driver()
            # assert
            result.get("http://localhost:3000")
            result.find_element(By.CLASS_NAME, "title")
            # clean up
            result.quit()


if __name__ == '__main__':
    unittest.main()
