#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from typing import Any, Callable, List
from getgauge.python import data_store
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from .app_context import app_context_key, timeout_key
from .bymapper import ByMapper
from .config import common_config as config
from .substitute import substitute


def find_element(by_param: str, by_value_param: str) -> WebElement:
    by = substitute(by_param)
    by_value = substitute(by_value_param)
    marker = get_marker(by, by_value)
    return _driver().find_element(*marker)


def find_elements(by_param: str, by_value_param: str) -> List[WebElement]:
    by = substitute(by_param)
    by_value = substitute(by_value_param)
    marker = get_marker(by, by_value)
    return _driver().find_elements(*marker)


def get_text_from_element(by: str, by_value: str) -> str:
    element = find_element(by, by_value)
    if "input" == element.tag_name:
        return element.get_attribute("value")
    else:
        return element.text


def find_attribute(by: str, by_value: str, attribute: str) -> str | bool:
    """
    This will return the string value of the attribute.
    Empty attributes will return 'true', never an empty string.
    If the attribute does not exist, it will return `False`.
    """
    def _element_attribute(driver: Remote) -> Any:
        marker = get_marker(substitute(by), substitute(by_value))
        element = driver.find_element(*marker)
        value = element.get_dom_attribute(attribute)
        return value if value is not None else False
    return wait_until(_element_attribute)


def wait_until(condition: Callable[[Remote], Any]) -> Any:
    timeout = data_store.scenario.get(timeout_key, config.get_implicit_timeout())
    try:
        return WebDriverWait(_driver(), timeout).until(condition)
    except TimeoutException:
        return False


def get_marker(by_string: str, by_value: str) -> tuple[str, str]:
    mapped_by = ByMapper.map_string(by_string)
    if mapped_by == By.ID:
        mapped_by = By.CSS_SELECTOR
        by_value = f"#{by_value}"
    return mapped_by, by_value


def _driver() -> Remote:
    return data_store.spec[app_context_key].driver
