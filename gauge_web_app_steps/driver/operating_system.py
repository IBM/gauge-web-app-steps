#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from __future__ import annotations

from enum import Enum


class OperatingSystem(Enum):

    ANDROID = "android"
    IOS = "ios"
    MACOS = "macos"
    LINUX = "linux"
    WINDOWS = "windows"

    def is_desktop(self) -> bool:
        """Checks if the given operating system a desktop system."""
        return self in [OperatingSystem.WINDOWS, OperatingSystem.MACOS, OperatingSystem.LINUX]

    def is_mobile(self) -> bool:
        """Checks if the given operating system a mobile system."""
        return self in [OperatingSystem.ANDROID, OperatingSystem.IOS]

    @staticmethod
    def parse(operating_system: str) -> OperatingSystem:
        """Try to determine an operating system from the given string."""
        operating_system = operating_system.lower()
        if operating_system in ["win", "windows"]:
            return OperatingSystem.WINDOWS
        elif operating_system in ["mac", "macos", "darwin"]:
            return OperatingSystem.MACOS
        else:
            return OperatingSystem(operating_system)

    def __str__(self) -> str:
        return self.value


class SaucelabsOperatingSystem(Enum):

    MACOS_DEFAULT = "macOS 13"
    MACOS_13 = "macOS 13"
    MACOS_12 = "macOS 12"
    MACOS_11 = "macOS 11"
    MACOS_10_15 = "macOS 10.15"
    MACOS_10_14 = "macOS 10.14"
    MACOS_10_13 = "macOS 10.13"
    MACOS_10_12 = "macOS 10.12"
    MACOS_10_11 = "macOS 10.11"
    MACOS_10_10 = "macOS 10.10"

    WINDOWS_DEFAULT = "Windows 11"
    WINDOWS_11 = "Windows 11"
    WINDOWS_10 = "Windows 10"
    WINDOWS_8_1 = "Windows 8.1"
    WINDOWS_8 = "Windows 8"
    WINDOWS_7 = "Windows 7"

    def __str__(self) -> str:
        return self.value

