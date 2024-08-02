#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest

from gauge_web_app_steps.driver import Browser, OperatingSystem


# noinspection DuplicatedCode
class TestBrowsers(unittest.TestCase):

    def test_is_supported(self):
        assert Browser.CHROME.is_supported(OperatingSystem.MACOS)
        assert Browser.EDGE.is_supported(OperatingSystem.MACOS)
        assert Browser.FIREFOX.is_supported(OperatingSystem.MACOS)
        assert not Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.MACOS)
        assert Browser.OPERA.is_supported(OperatingSystem.MACOS)
        assert Browser.SAFARI.is_supported(OperatingSystem.MACOS)

        assert Browser.CHROME.is_supported(OperatingSystem.WINDOWS)
        assert Browser.EDGE.is_supported(OperatingSystem.WINDOWS)
        assert Browser.FIREFOX.is_supported(OperatingSystem.WINDOWS)
        assert Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.WINDOWS)
        assert Browser.OPERA.is_supported(OperatingSystem.WINDOWS)
        assert not Browser.SAFARI.is_supported(OperatingSystem.WINDOWS)

        assert Browser.CHROME.is_supported(OperatingSystem.LINUX)
        assert not Browser.EDGE.is_supported(OperatingSystem.LINUX)
        assert Browser.FIREFOX.is_supported(OperatingSystem.LINUX)
        assert not Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.LINUX)
        assert Browser.OPERA.is_supported(OperatingSystem.LINUX)
        assert not Browser.SAFARI.is_supported(OperatingSystem.LINUX)

        assert not Browser.CHROME.is_supported(OperatingSystem.IOS)
        assert not Browser.EDGE.is_supported(OperatingSystem.IOS)
        assert Browser.FIREFOX.is_supported(OperatingSystem.IOS)
        assert not Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.IOS)
        assert Browser.OPERA.is_supported(OperatingSystem.IOS)
        assert Browser.SAFARI.is_supported(OperatingSystem.IOS)

        assert Browser.CHROME.is_supported(OperatingSystem.ANDROID)
        assert not Browser.EDGE.is_supported(OperatingSystem.ANDROID)
        assert Browser.FIREFOX.is_supported(OperatingSystem.ANDROID)
        assert not Browser.INTERNET_EXPLORER.is_supported(OperatingSystem.ANDROID)
        assert Browser.OPERA.is_supported(OperatingSystem.ANDROID)
        assert not Browser.SAFARI.is_supported(OperatingSystem.ANDROID)


if __name__ == '__main__':
    unittest.main()
