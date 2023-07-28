#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os

from typing import Optional


def get_mobile_appium_server_url() -> Optional[str]:
    return os.environ.get("driver_platform_local_mobile_appium_server_url")


def get_mobile_device_name() -> Optional[str]:
    return os.environ.get("driver_platform_local_mobile_device_name")


def get_mobile_device_udid() -> Optional[str]:
    return os.environ.get("driver_platform_local_mobile_device_udid")


def get_mobile_real_device(default="false") -> bool:
    return os.environ.get("driver_platform_local_mobile_real_device", default).lower() in ("true", "1")
