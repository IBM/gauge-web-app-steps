#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from selenium.webdriver.common.by import By


class ByMapper:

    _MAPPING = {
        "id": By.ID,
        "xpath": By.XPATH,
        "link text": By.LINK_TEXT,
        "partial link text": By.PARTIAL_LINK_TEXT,
        "name": By.NAME,
        "tag name": By.TAG_NAME,
        "class name": By.CLASS_NAME,
        "css selector": By.CSS_SELECTOR,
    }

    @classmethod
    def map_string(cls, by_string: str) -> str:
        return cls._MAPPING[by_string]
