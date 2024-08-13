#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from typing import Any, Callable, List, TypeVar
from getgauge.python import data_store
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from .app_context import app_context_key, timeout_key
from .bymapper import ByMapper
from .config import common_config as config
from .substitute import substitute


T = TypeVar('T')


def find_element(by_param: str, by_value_param: str) -> WebElement:
    by = substitute(by_param)
    by_value = substitute(by_value_param)
    marker = get_marker(by, by_value)
    return wait_until(lambda driver: driver.find_element(*marker))


def find_elements(by_param: str, by_value_param: str) -> List[WebElement]:
    by = substitute(by_param)
    by_value = substitute(by_value_param)
    marker = get_marker(by, by_value)
    return wait_until(lambda driver: driver.find_elements(*marker))


def get_text_from_element(by_param: str, by_value_param: str) -> str:
    element = find_element(by_param, by_value_param)
    if "input" == element.tag_name:
        res = element.get_attribute("value")
        if res is None:
            # workaround for some mobile devices
            res = _driver().execute_script("return arguments[0].value", element)
        if res is not None:
            return res
    return element.text


def find_attribute(by_param: str, by_value_param: str, attribute: str) -> str | bool:
    """
    This will return the string value of the attribute.
    Empty attributes will return 'true', never an empty string.
    If the attribute does not exist, it will return `False`.
    """
    def _element_attribute(driver: Remote) -> Any:
        marker = get_marker(substitute(by_param), substitute(by_value_param))
        element = driver.find_element(*marker)
        value = element.get_dom_attribute(attribute)
        return value if value is not None else False
    return wait_until(_element_attribute)


def wait_until(condition: Callable[[Remote], T], message: str = "") -> T:
    timeout = data_store.scenario.get(timeout_key, config.get_implicit_timeout())
    return WebDriverWait(_driver(), timeout=timeout, poll_frequency=0.25, ignored_exceptions=[WebDriverException])\
        .until(condition, message)


def get_marker(by_string: str, by_value: str) -> tuple[str, str]:
    mapped_by = ByMapper.map_string(by_string)
    if mapped_by == By.ID:
        mapped_by = By.CSS_SELECTOR
        by_value = f"#{by_value}"
    return mapped_by, by_value


def _driver() -> Remote:
    return data_store.spec[app_context_key].driver
