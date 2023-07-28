#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from enum import Enum

from .operating_system import OperatingSystem


class Browser(Enum):

    CHROME = "chrome"
    EDGE = "edge"
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "internet explorer"
    OPERA = "opera"
    SAFARI = "safari"

    def is_supported(self, operating_system: OperatingSystem) -> bool:
        """Checks if given browser is supported by the specified operating system."""
        supported = {
            OperatingSystem.MACOS: [Browser.CHROME, Browser.EDGE, Browser.FIREFOX , Browser.OPERA, Browser.SAFARI],
            OperatingSystem.WINDOWS: [Browser.CHROME, Browser.EDGE, Browser.FIREFOX, Browser.INTERNET_EXPLORER, Browser.OPERA],
            OperatingSystem.LINUX: [Browser.CHROME, Browser.FIREFOX, Browser.OPERA],
            OperatingSystem.IOS: [Browser.FIREFOX, Browser.OPERA, Browser.SAFARI],
            OperatingSystem.ANDROID: [Browser.CHROME, Browser.FIREFOX, Browser.OPERA]
        }
        return self in supported[operating_system]

    def __str__(self) -> str:
        return self.value
