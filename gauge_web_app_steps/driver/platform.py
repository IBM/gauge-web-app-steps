#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from enum import Enum


class Platform(Enum):

    LOCAL = "local"
    SAUCELABS = "saucelabs"

    def is_local(self) -> bool:
        return self == Platform.LOCAL

    def is_remote(self) -> bool:
        return self == Platform.SAUCELABS

    def __str__(self) -> str:
        return self.value

