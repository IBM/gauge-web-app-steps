#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest

from gauge_web_app_steps.driver import OperatingSystem
import pytest


class TestOperatingSystem(unittest.TestCase):

    def test_is_desktop(self):
        assert OperatingSystem.WINDOWS.is_desktop()
        assert OperatingSystem.MACOS.is_desktop()
        assert OperatingSystem.LINUX.is_desktop()
        assert not OperatingSystem.ANDROID.is_desktop()
        assert not OperatingSystem.IOS.is_desktop()

    def test_is_mobile(self):
        assert OperatingSystem.ANDROID.is_mobile()
        assert OperatingSystem.IOS.is_mobile()
        assert not OperatingSystem.WINDOWS.is_mobile()
        assert not OperatingSystem.MACOS.is_mobile()
        assert not OperatingSystem.LINUX.is_mobile()

    def test_parse(self):
        assert OperatingSystem.WINDOWS == OperatingSystem.parse("win")
        assert OperatingSystem.WINDOWS == OperatingSystem.parse("windows")
        assert OperatingSystem.WINDOWS == OperatingSystem.parse("WINDOWS")
        assert OperatingSystem.MACOS == OperatingSystem.parse("mac")
        assert OperatingSystem.MACOS == OperatingSystem.parse("macos")
        assert OperatingSystem.MACOS == OperatingSystem.parse("darwin")
        assert OperatingSystem.MACOS == OperatingSystem.parse("MAC")
        assert OperatingSystem.LINUX == OperatingSystem.parse("linux")
        assert OperatingSystem.LINUX == OperatingSystem.parse("LINUX")
        assert OperatingSystem.ANDROID == OperatingSystem.parse("android")
        assert OperatingSystem.ANDROID == OperatingSystem.parse("ANDROID")
        assert OperatingSystem.IOS == OperatingSystem.parse("ios")
        assert OperatingSystem.IOS == OperatingSystem.parse("IOS")
        with pytest.raises(ValueError):
            OperatingSystem.parse("foo")


if __name__ == '__main__':
    unittest.main()
