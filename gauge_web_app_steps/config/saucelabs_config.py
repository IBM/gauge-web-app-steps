#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os

from typing import Optional

from ..driver.operating_system import OperatingSystem


def get_appium_version() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_mobile_appium_version")


def get_browser_version(default="latest") -> str:
    return os.environ.get("driver_platform_saucelabs_desktop_browser_version", default)


def get_device_name() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_mobile_device_name")


def get_executor() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_executor")


def get_tunnel_name() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_tunnel_name")


def get_test_title() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_test_title")


def get_build() -> Optional[str]:
    return os.environ.get("driver_platform_saucelabs_build")


def get_sauce_status_address() -> Optional[str]:
    return os.environ.get("SAUCE_STATUS_ADDRESS")


def is_sauce_tunnel_active() -> bool:
    return os.environ.get("SAUCE_TUNNEL_ACTIVE", "false").lower() in ('true', '1')


def is_sauce_tunnel_pooling() -> bool:
    """ This property is needed for parallel executions, so that multiple tunnels do not interfere with each other """
    return os.environ.get("SAUCE_TUNNEL_POOLING", "false").lower() in ('true', '1')


def get_host_os() -> Optional[OperatingSystem]:
    # TODO: determine during runtime
    host_os = os.environ.get("SAUCE_HOST")
    return OperatingSystem.parse(host_os) if host_os is not None else None


def get_sauce_path() -> str:
    return os.environ.get("SAUCE_PATH", "sc")


def get_sauce_user_name() -> Optional[str]:
    return os.environ.get("SAUCE_USERNAME")


def get_sauce_access_key() -> Optional[str]:
    return os.environ.get("SAUCE_ACCESS_KEY")


def get_sauce_region() -> Optional[str]:
    return os.environ.get("SAUCE_REGION")


def get_sauce_dns() -> Optional[str]:
    return os.environ.get("SAUCE_DNS")


def get_sauce_no_ssl_bump_domains() -> Optional[str]:
    return os.environ.get("SAUCE_NO_SSL_BUMP_DOMAINS")


def get_sauce_log_file() -> str:
    project_root = os.environ.get("GAUGE_PROJECT_ROOT")
    default_sc_log = os.path.join(project_root, "logs", "sc.log")
    return os.getenv("SAUCE_LOG_FILE", default_sc_log)
