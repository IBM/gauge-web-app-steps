#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import unittest

from parameterized import parameterized
from unittest.mock import patch

from gauge_web_app_steps.config import local_config


class TestLocal(unittest.TestCase):

    def test_get_mobile_appium_server_url(self):
        with patch.dict(os.environ, {"driver_platform_local_mobile_appium_server_url": "http://foobar"}):
            result = local_config.get_mobile_appium_server_url()
            self.assertEqual("http://foobar", result)

    def test_get_mobile_device_name(self):
        with patch.dict(os.environ, {"driver_platform_local_mobile_device_name": "foo-device"}):
            result = local_config.get_mobile_device_name()
            self.assertEqual("foo-device", result)

    def test_get_mobile_device_udid(self):
        with patch.dict(os.environ, {"driver_platform_local_mobile_device_udid": "foo-device-udid"}):
            result = local_config.get_mobile_device_udid()
            self.assertEqual("foo-device-udid", result)

    @parameterized.expand([
        ("True", True),
        ("true", True),
        ("1", True),
        ("False", False),
        ("false", False),
        ("0", False),
    ])
    def test_get_mobile_real_device(self, is_real_device, expected_value):
        with patch.dict(os.environ, {"driver_platform_local_mobile_real_device": is_real_device}):
            result = local_config.get_mobile_real_device()
            self.assertEqual(expected_value, result)

    def test_get_mobile_real_device_should_return_false_as_default(self):
        result = local_config.get_mobile_real_device()
        self.assertFalse(result)

    def test_get_mobile_real_device_should_return_default(self):
        result = local_config.get_mobile_real_device("True")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
