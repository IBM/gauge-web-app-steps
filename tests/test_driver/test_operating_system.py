#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest

from gauge_web_app_steps.driver import OperatingSystem


class TestOperatingSystem(unittest.TestCase):

    def test_is_desktop(self):
        self.assertTrue(OperatingSystem.WINDOWS.is_desktop())
        self.assertTrue(OperatingSystem.MACOS.is_desktop())
        self.assertTrue(OperatingSystem.LINUX.is_desktop())
        self.assertFalse(OperatingSystem.ANDROID.is_desktop())
        self.assertFalse(OperatingSystem.IOS.is_desktop())

    def test_is_mobile(self):
        self.assertTrue(OperatingSystem.ANDROID.is_mobile())
        self.assertTrue(OperatingSystem.IOS.is_mobile())
        self.assertFalse(OperatingSystem.WINDOWS.is_mobile())
        self.assertFalse(OperatingSystem.MACOS.is_mobile())
        self.assertFalse(OperatingSystem.LINUX.is_mobile())

    def test_parse(self):
        self.assertEqual(OperatingSystem.WINDOWS, OperatingSystem.parse("win"))
        self.assertEqual(OperatingSystem.WINDOWS, OperatingSystem.parse("windows"))
        self.assertEqual(OperatingSystem.WINDOWS, OperatingSystem.parse("WINDOWS"))
        self.assertEqual(OperatingSystem.MACOS, OperatingSystem.parse("mac"))
        self.assertEqual(OperatingSystem.MACOS, OperatingSystem.parse("macos"))
        self.assertEqual(OperatingSystem.MACOS, OperatingSystem.parse("darwin"))
        self.assertEqual(OperatingSystem.MACOS, OperatingSystem.parse("MAC"))
        self.assertEqual(OperatingSystem.LINUX, OperatingSystem.parse("linux"))
        self.assertEqual(OperatingSystem.LINUX, OperatingSystem.parse("LINUX"))
        self.assertEqual(OperatingSystem.ANDROID, OperatingSystem.parse("android"))
        self.assertEqual(OperatingSystem.ANDROID, OperatingSystem.parse("ANDROID"))
        self.assertEqual(OperatingSystem.IOS, OperatingSystem.parse("ios"))
        self.assertEqual(OperatingSystem.IOS, OperatingSystem.parse("IOS"))
        self.assertRaises(ValueError, lambda: OperatingSystem.parse("foo"))


if __name__ == '__main__':
    unittest.main()
