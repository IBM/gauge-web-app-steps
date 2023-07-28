#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from selenium.webdriver.common.keys import Keys


class KeyMapper:

    # {'NULL': '\ue000', 'CANCEL': '\ue001' etc ... }
    _MAPPING = dict((key, getattr(Keys, key)) for key in vars(Keys) if not key.startswith("_"))
    _KEYS = list(_MAPPING.keys())

    @classmethod
    def map_string(cls, key_string: str) -> str:
        return cls._MAPPING[key_string]
