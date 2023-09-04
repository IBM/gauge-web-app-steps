#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os

from typing import Optional
from warnings import warn

from ..driver import Browser, OperatingSystem, Platform


def get_driver_cache_days(default = 365) -> int:
    return int(os.environ.get("driver_cache_days", default))


def is_debug_log() -> bool:
    return os.environ.get("debug_log", "False").lower() in ("true", "1")


def get_diff_formats() -> str:
    return os.environ.get("diff_formats", "full")


def is_whole_page_screenshot() -> bool:
    return os.environ.get("screenshot_whole_page_no_scroll", "False").lower() in ("true", "1")


def get_time_pattern() -> str:
    return os.environ.get("time_pattern", "%Y-%m-%d_%H-%M-%S")


def get_file_name_pattern() -> str:
    return os.environ.get("filename_pattern", "%{browser}_%{name}.%{ext}")


def get_screenshot_dir() -> str:
    return os.environ.get("screenshot_dir", "screenshots")


def get_actual_screenshot_dir() -> str:
    return os.environ.get("actual_screenshot_dir", "actual_screenshots")


def get_expected_screenshot_dir() -> str:
    return os.environ.get("expected_screenshot_dir", "expected_screenshots")


def get_failure_screenshot_dir() -> str:
    return os.environ.get("failure_screenshot_dir", os.path.join("reports", "html-report", "images"))


def get_browser(default=Browser.FIREFOX) -> Browser:
    config_browser = os.environ.get("driver_browser", default.value)
    return Browser(config_browser)


def get_implicit_timeout(default=5) -> int:
    return int(os.environ.get("driver_implicit_timeout", default))


def get_operating_system(default=OperatingSystem.MACOS) -> OperatingSystem:
    config_os = os.environ.get("driver_operating_system", default.value)
    return OperatingSystem.parse(config_os)


def get_operating_system_version() -> Optional[str]:
    return os.environ.get("driver_operating_system_version")


def get_page_load_timeout(default=30) -> int:
    return int(os.environ.get("driver_page_load_timeout", default))


def get_platform(default=Platform.LOCAL) -> Platform:
    config_platform = os.environ.get("driver_platform", default.value).lower()
    return Platform(config_platform)


def is_headless() -> bool:
    headless = False
    if "driver_headless" in os.environ:
        warn("property 'driver_headless' is deprecated. Please use 'driver_platform_local_headless' instead")
        headless = os.environ.get("driver_headless").lower() in ("true", "1")
    if "driver_platform_local_headless" in os.environ:
        return os.environ.get("driver_platform_local_headless", "false").lower() in ("true", "1")
    return headless


def get_custom_args() -> list:
    args_prop = os.environ.get("driver_custom_args", "")
    return [arg.strip() for arg in args_prop.split(",") if arg.strip()]


def is_driver_binary_copy() -> bool:
    return os.environ.get("driver_binary_copy", "false").lower() in ("true", "1")


def is_selenium4_driver_manager() -> bool:
    return os.environ.get("driver_manager_selenium4", "false").lower() in ("true", "1")
