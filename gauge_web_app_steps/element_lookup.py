#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import time

from appium.webdriver.webelement import WebElement as AppiumElement
from dataclasses import dataclass
from typing import Any, Callable, List, TypeVar
from getgauge.python import data_store
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from .app_context import AppContext, app_context_key, timeout_key
from .bymapper import ByMapper
from .config import common_config as config
from .report import Report
from .substitute import substitute


T = TypeVar('T')


def find_element(by_param: str, by_value_param: str, immediately=False) -> WebElement | None:
    by = substitute(by_param)
    by_value = substitute(by_value_param)
    marker = get_marker(by, by_value)
    if immediately:
        try:
            return _driver().find_element(*marker)
        except WebDriverException:
            return None
    else:
        return wait_until(lambda driver: driver.find_element(*marker))


def find_elements(by_param: str, by_value_param: str, immediately=False) -> List[WebElement] | None:
    by = substitute(by_param)
    by_value = substitute(by_value_param)
    marker = get_marker(by, by_value)
    try:
        if immediately:
            return _driver().find_elements(*marker)
        else:
            return wait_until(lambda driver: driver.find_elements(*marker))
    except WebDriverException:
        return []


def get_text_from_element(by_param: str, by_value_param: str, immediately=False) -> str | None:
    element = find_element(by_param, by_value_param, immediately)
    if element is None:
        return None
    elif "input" == element.tag_name:
        res = element.get_attribute("value")
        if res is None:
            # workaround for some mobile devices
            res = _driver().execute_script("return arguments[0].value", element)
        if res is not None:
            return res
    return element.text


def find_attribute(by_param: str, by_value_param: str, attribute: str, immediately=False) -> str | bool | None:
    marker = get_marker(substitute(by_param), substitute(by_value_param))
    def _element_attribute(driver: Remote) -> Any:
        """
        This will return the string value of the attribute.
        Empty attributes will return 'true', never an empty string.
        If the attribute does not exist, it will return `False`.
        """
        element = driver.find_element(*marker)
        value = element.get_dom_attribute(attribute)
        return value if value is not None else False
    if immediately:
        try:
            res = _element_attribute(_driver())
            return res if res else None
        except WebDriverException:
            return None
    else:
        return wait_until(_element_attribute)


@dataclass
class ViewportOffset:
    """The position of the element's top left corner in the viewport."""
    top: int
    left: int


def wait_for_idle_element(by: str, by_value: str):
    element = find_element(by, by_value)
    previous_offset = _offset(element)
    def element_stable(_: Remote):
        time.sleep(0.2)
        potentially_moving_element = find_element(by, by_value)
        current_offset = _offset(potentially_moving_element)
        print(f"Got offset: {current_offset}")
        nonlocal previous_offset
        if previous_offset == current_offset:
            return True
        previous_offset = current_offset
        return False
    try:
        wait_until(element_stable)
    except TimeoutException:
        # Best effort approach
        _report().log_debug(f"element {element} keeps moving after scrolling into view")


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


def _offset(element: WebElement) -> ViewportOffset:
    if isinstance(element, AppiumElement) and config.is_app_test():
        elem: AppiumElement = element
        location_in_view = elem.location_in_view
        return ViewportOffset(round(location_in_view['y']), round(location_in_view['x']))
    else:
        viewport_offset = _driver().execute_script("return arguments[0].getBoundingClientRect();", element)
        return ViewportOffset(round(viewport_offset['top']), round(viewport_offset['left']))


def _driver() -> Remote:
    app_ctx: AppContext = data_store.spec[app_context_key]
    return app_ctx.driver


def _report() -> Report:
    app_ctx: AppContext = data_store.spec[app_context_key]
    return app_ctx.report
