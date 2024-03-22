#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import re

from typing import Iterable
from selenium.webdriver.common.keys import Keys


class KeyMapper:

    # {'NULL': '\ue000', 'CANCEL': '\ue001' etc ... }
    _MAPPING = dict((key, getattr(Keys, key)) for key in vars(Keys) if not key.startswith("_"))
    _KEYS = list(_MAPPING.keys())

    @classmethod
    def map_string(cls, key_string: str) -> str:
        return cls._MAPPING[key_string]

    def map_keys(keys_param: str) -> Iterable[str]:
        keys = re.split(r'[,\s]+', keys_param)
        unknown_keys = [k for k in keys if k not in KeyMapper._KEYS]
        assert len(unknown_keys) == 0,\
            "Keys %s unknown.\nUse those instead: %s" % (unknown_keys, KeyMapper._KEYS)
        send_keys = [KeyMapper.map_string(k) for k in keys]
        return send_keys
