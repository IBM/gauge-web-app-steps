#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest

from gauge_web_app_steps.driver import Browser, OperatingSystem


# noinspection DuplicatedCode
class TestBrowsers(unittest.TestCase):

    def test_is_supported(self):
        self.assertTrue(Browser.CHROME.is_supported(OperatingSystem.MACOS))
        self.assertTrue(Browser.EDGE.is_supported(OperatingSystem.MACOS))
        self.assertTrue(Browser.FIREFOX.is_supported(OperatingSystem.MACOS))
        self.assertFalse(Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.MACOS))
        self.assertTrue(Browser.OPERA.is_supported(OperatingSystem.MACOS))
        self.assertTrue(Browser.SAFARI.is_supported(OperatingSystem.MACOS))

        self.assertTrue(Browser.CHROME.is_supported(OperatingSystem.WINDOWS))
        self.assertTrue(Browser.EDGE.is_supported(OperatingSystem.WINDOWS))
        self.assertTrue(Browser.FIREFOX.is_supported(OperatingSystem.WINDOWS))
        self.assertTrue(Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.WINDOWS))
        self.assertTrue(Browser.OPERA.is_supported(OperatingSystem.WINDOWS))
        self.assertFalse(Browser.SAFARI.is_supported(OperatingSystem.WINDOWS))

        self.assertTrue(Browser.CHROME.is_supported(OperatingSystem.LINUX))
        self.assertFalse(Browser.EDGE.is_supported(OperatingSystem.LINUX))
        self.assertTrue(Browser.FIREFOX.is_supported(OperatingSystem.LINUX))
        self.assertFalse(Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.LINUX))
        self.assertTrue(Browser.OPERA.is_supported(OperatingSystem.LINUX))
        self.assertFalse(Browser.SAFARI.is_supported(OperatingSystem.LINUX))

        self.assertFalse(Browser.CHROME.is_supported(OperatingSystem.IOS))
        self.assertFalse(Browser.EDGE.is_supported(OperatingSystem.IOS))
        self.assertTrue(Browser.FIREFOX.is_supported(OperatingSystem.IOS))
        self.assertFalse(Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.IOS))
        self.assertTrue(Browser.OPERA.is_supported(OperatingSystem.IOS))
        self.assertTrue(Browser.SAFARI.is_supported(OperatingSystem.IOS))

        self.assertTrue(Browser.CHROME.is_supported(OperatingSystem.ANDROID))
        self.assertFalse(Browser.EDGE.is_supported(OperatingSystem.ANDROID))
        self.assertTrue(Browser.FIREFOX.is_supported(OperatingSystem.ANDROID))
        self.assertFalse(Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.ANDROID))
        self.assertTrue(Browser.OPERA.is_supported(OperatingSystem.ANDROID))
        self.assertFalse(Browser.SAFARI.is_supported(OperatingSystem.ANDROID))


if __name__ == '__main__':
    unittest.main()
