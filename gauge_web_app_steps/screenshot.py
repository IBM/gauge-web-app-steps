#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import time

from getgauge.python import data_store
from selenium.webdriver import Remote
from typing import Iterable

from .app_context import app_context_key
from .config import common_config as config
from .imagepaths import ImagePath
from .images import Images


def create_screenshot(image_file_name: str) -> str:
    screenshot_file_path = _image_path().create_screenshot_file_path(image_file_name)
    _driver().save_screenshot(screenshot_file_path)
    return screenshot_file_path


def create_failure_screenshot() -> str:
    screenshot_path = _image_path().create_failure_screenshot_file_path()
    _driver().save_screenshot(screenshot_path)
    return screenshot_path


def ssim_screenshot_noscrolling(image_file_name: str, threshold: float) -> Iterable[str]:
    failed_asserts = []
    actual_screenshot_full_path = _image_path().create_actual_screenshot_file_path(image_file_name)
    _driver().save_full_page_screenshot(actual_screenshot_full_path)
    expected_screenshot_full_path = _image_path().create_expected_screenshot_file_path(image_file_name)
    if not os.path.isfile(expected_screenshot_full_path):
        failed_asserts.append("screenshot {} does not exist".format(expected_screenshot_full_path))
    else:
        append_structured_similarity(failed_asserts, expected_screenshot_full_path, actual_screenshot_full_path, threshold)
    return failed_asserts


def ssim_screenshot_scrolling(image_file_name: str, threshold: float) -> Iterable[str]:
    failed_asserts = []
    postfix = 1
    should_continue = True
    while should_continue:
        actual_screenshot_full_path = _image_path().create_actual_screenshot_file_path(image_file_name, postfix)
        _driver().save_screenshot(actual_screenshot_full_path)
        expected_screenshot_full_path = _image_path().create_expected_screenshot_file_path(image_file_name, postfix)
        should_continue = _scroll() and postfix <= 32
        postfix += 1
        if not os.path.isfile(expected_screenshot_full_path):
            failed_asserts.append("screenshot {} does not exist".format(expected_screenshot_full_path))
        else:
            append_structured_similarity(failed_asserts, expected_screenshot_full_path, actual_screenshot_full_path, threshold)
    return failed_asserts


def append_structured_similarity(asserts: list, expected_screenshot: str, actual_screenshot: str, threshold: float) -> Iterable[str]:
    diff_formats = config.get_diff_formats()
    ssim = _images().adapt_and_compare_images(expected_screenshot, actual_screenshot, diff_formats)
    if ssim < threshold:
        asserts.append("SSIM {} is less than threshold {} for {}".format(ssim, threshold, actual_screenshot))


def get_structured_similarity_to_expected(image_file_name: str, location: int, size: int, pixel_ratio: int, viewport_offset: int):
    """
    Get the structured similarity of a croped screenshot to an existing one.
    """
    actual_screenshot_full_path = _image_path().create_actual_screenshot_file_path(image_file_name)
    _driver().save_screenshot(actual_screenshot_full_path)
    crop_image(
        actual_screenshot_full_path,
        location,
        size,
        pixel_ratio,
        viewport_offset
    )
    expected_screenshot_full_path = _image_path().create_expected_screenshot_file_path(image_file_name)
    diff_formats = config.get_diff_formats()
    return _images().adapt_and_compare_images(expected_screenshot_full_path, actual_screenshot_full_path, diff_formats)


def crop_image(screenshot_path: str, location: int, size: int, pixel_ratio: int, viewport_offset: int):
    _images().crop_image_file(
        screenshot_path,
        location,
        size,
        pixel_ratio,
        viewport_offset
    )

def _scroll() -> int:
    """
    Scrolls down the size of the current window height and returns True, if scrolling down is still possible
    (The page is not ended yet)
    """
    current_offset: int = _driver().execute_script("return window.pageYOffset")
    _driver().execute_script("window.scrollBy(0, window.innerHeight)")
    time.sleep(0.3)
    after_scroll_offset: int = _driver().execute_script("return window.pageYOffset")
    return after_scroll_offset > current_offset

def create_actual_screenshot_file_path(image_file_name: str, page: int) -> str:
    path = _image_path().create_actual_screenshot_file_path(image_file_name, page)
    _driver().save_screenshot(path)
    return path


def create_expected_screenshot_file_path(image_file_name: str, page: int) -> str:
    return _image_path().create_expected_screenshot_file_path(image_file_name, page)


def _driver() -> Remote:
    return data_store.spec[app_context_key].driver


def _image_path() -> ImagePath:
    return data_store.spec[app_context_key].image_path


def _images() -> Images:
    return data_store.spec[app_context_key].images
