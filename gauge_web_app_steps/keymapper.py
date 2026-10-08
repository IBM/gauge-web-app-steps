#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import re
from collections.abc import Iterable
from typing import ClassVar

from selenium.webdriver.common.keys import Keys


class KeyMapper:

    # {'NULL': '\ue000', 'CANCEL': '\ue001' etc ... }
    _MAPPING: ClassVar = {key: getattr(Keys, key) for key in vars(Keys) if not key.startswith("_")}
    _KEYS: ClassVar = list(_MAPPING.keys())

    @classmethod
    def map_string(cls, key_string: str) -> str:
        return cls._MAPPING[key_string]

    def map_keys(keys_param: str) -> Iterable[str]:
        keys = re.split(r'[,\s]+', keys_param)
        unknown_keys = [k for k in keys if k not in KeyMapper._KEYS]
        assert len(unknown_keys) == 0,\
            f"Keys {unknown_keys} unknown.\nUse those instead: {KeyMapper._KEYS}"
        send_keys = [KeyMapper.map_string(k) for k in keys]
        return send_keys
