#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from enum import Enum
from selenium.webdriver.support.select import Select


class SelectKey(Enum):
    """
    Enum for the selection type of list ements.
    """

    INDEX = "index"
    VALUE = "value"
    VISIBLE_TEXT = "visible text"

    @staticmethod
    def to_enum(key: str = ''):
        assert len(key) > 0, "expected a non empty string"
        return SelectKey[key.upper().replace(' ', '_')]


class Selector:
    """
    This class encapsulates the interaction with a select element.
    """

    @staticmethod
    def get_selected_value(element):
        return Select(element).first_selected_option.get_attribute("value")

    @staticmethod
    def select(element, select_value, select_key: SelectKey = SelectKey.INDEX):
        Selector._select(Select(element), select_value, select_key)

    @staticmethod
    def _select(select_object, select_value, select_key: SelectKey = SelectKey.INDEX):
        if select_key == SelectKey.INDEX:
            select_object.select_by_index(select_value)
        elif select_key == SelectKey.VALUE:
            select_object.select_by_value(select_value)
        elif select_key == SelectKey.VISIBLE_TEXT:
            select_object.select_by_visible_text(select_value)
