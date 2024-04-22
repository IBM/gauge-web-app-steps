#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os

from typing import Optional


def get_appium_version() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_mobile_appium_version")


def get_browser_version(default="latest") -> str:
    return os.environ.get("driver_platform_saucelabs_desktop_browser_version", default)


def get_device_name() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_mobile_device_name")


def get_executor() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_executor")


def get_test_title() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_test_title")


def get_build() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_build")


def is_device_cached() -> bool:
    return os.environ.get("driver_platform_saucelabs_devicecache", "false").lower() in ('true', '1')


def is_extended_debugging_enabled() -> bool:
    return os.environ.get("driver_platform_saucelabs_extended_debugging", "false").lower() in ('true', '1')


def is_sauce_tunnel_active() -> bool:
    return os.environ.get("SAUCE_TUNNEL_ACTIVE", "false").lower() in ('true', '1')


def get_sauce_path() -> str:
    return os.environ.get("SAUCE_PATH", "sc")


def get_sauce_user_name() -> Optional[str]:
    return os.environ.get("SAUCE_USERNAME")


def get_sauce_access_key() -> Optional[str]:
    return os.environ.get("SAUCE_ACCESS_KEY")


def get_tunnel_name() -> Optional[str]:
    return os.environ.get("SAUCE_TUNNEL_NAME")


def get_sauce_api_address() -> Optional[str]:
    return os.environ.get("SAUCE_API_ADDRESS", "127.0.0.1:8080")
