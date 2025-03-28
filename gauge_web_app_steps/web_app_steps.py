#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import base64
import os
import re
import sys
import time
import traceback
import urllib
from uuid import uuid4

from itertools import filterfalse
from typing import Tuple
from getgauge.python import data_store, step, before_spec, after_spec, custom_screenshot_writer, before_suite, after_suite, before_step, ExecutionContext
from selenium.common.exceptions import JavascriptException, NoSuchWindowException, TimeoutException, WebDriverException
from selenium.webdriver import Remote
from appium.webdriver import Remote as AppiumRemote
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from .app_context import AppContext, app_context_key, timeout_key
from .config import common_config as config
from .driver.browsers import Browser
from .element_lookup import find_element, find_elements, find_attribute, get_text_from_element, get_marker, wait_until, wait_for_idle_element
from .keymapper import KeyMapper
from .report import Report
from .sauce_tunnel import SauceTunnel
from .selector import SelectKey, Selector
from .screenshot import (append_structured_similarity, create_screenshot, create_failure_screenshot, 
                        create_actual_screenshot_file_path, create_expected_screenshot_file_path, crop_image,
                        get_structured_similarity_to_expected, ssim_screenshot_scrolling, ssim_screenshot_noscrolling)
from .substitute import substitute


# Repeat an action a number of times before failing
max_attempts = 12
basic_auth_key = "_basic_auth"
error_message_key = "_err_msg"
suite_id_key = "_suite_id"


@before_suite
def before_suite_hook() -> None:
    try:
        SauceTunnel.start()
        data_store.suite[suite_id_key] = str(uuid4())
    except BaseException as e:
        # Gauge swallows some exceptions, so they are handled here
        print(f"An exception occured while SauceConnect initiated: {str(e)}", file=sys.stderr)
        traceback.print_exception(e)
        raise e


@after_suite
def after_suite_hook() -> None:
    try:
        SauceTunnel.terminate()
    except BaseException as e:
        # Gauge swallows some exceptions, so they are handled here
        print(f"An exception occured while SauceConnect terminated: {str(e)}", file=sys.stderr)
        traceback.print_exception(e)
        raise e


@before_spec
def before_spec_hook(exe_ctx: ExecutionContext) -> None:
    try:
        suite_id = data_store.suite[suite_id_key]
        app_ctx = AppContext(exe_ctx, suite_id)
        data_store.spec[app_context_key] = app_ctx
    except BaseException as e:
        # Gauge swallows some exceptions, so they are handled here
        print(f"An exception occured while instantiating the driver: {str(e)}", file=sys.stderr)
        traceback.print_exception(e)
        raise e


@after_spec
def after_spec_hook() -> None:
    try:
        app_ctx: AppContext = data_store.spec.get(app_context_key)
        if app_ctx is not None and app_ctx.driver is not None:
            app_ctx.report.log_debug("closing driver")
            app_ctx.driver.quit()
    except BaseException as e:
        # Gauge swallows some exceptions, so they are handled here
        print(f"An exception occured while closing the driver: {str(e)}", file=sys.stderr)
        traceback.print_exception(e)
        raise e


@before_step
def before_step_hook(exe_ctx:  ExecutionContext) -> None:
    step_text = exe_ctx.step.text
    def warn_using_deprecated_step(step_text: str, mapping: Tuple[str]) -> None:
        match = re.fullmatch(mapping[0], step_text)
        if match is not None:
            new_step = mapping[1].replace("<by>", match.group(1)).replace("<by_value>", match.group(2))
            report().log(f"The step '{step_text}' is deprecated, please use '{new_step}'")
    warn_using_deprecated_step(step_text, (r'Assert (".*?") = (".*?") is displayed', "Assert <by> = <by_value> exists",))
    warn_using_deprecated_step(step_text, (r'Assert (".*?") = (".*?") is invisible', "Assert <by> = <by_value> does not exist",))


@custom_screenshot_writer
def take_screenshot_on_failure() -> str:
    if driver() is None:
        # Error before driver initialization
        return None
    try:
        screenshot_file_path = create_failure_screenshot()
        #report().log_image(screenshot_file_path, "Step Failure Screenshot")
        return screenshot_file_path
    except Exception as e:
        report().log(str(e))
        return None


# Steps -------------------------------------------


@step("Wait <secs>")
def wait_for(secs_param: str) -> None:
    secs = substitute(secs_param)
    time.sleep(float(secs))


@step("Wait for window <secs> and save handle as <placeholder>")
def wait_for_window(secs_param: str, placeholder_name_param: str) -> None:
    secs = substitute(secs_param)
    placeholder_name = substitute(placeholder_name_param)
    assert placeholder_name in data_store.scenario.keys(), "Expected saved window handles. Did you use '* Save window handles'?"
    time.sleep(float(secs))
    wh_now = driver().window_handles
    #previous saved window handles
    wh_then = data_store.scenario[placeholder_name]
    if len(wh_now) > len(wh_then):
        win_handle = set(wh_now).difference(set(wh_then)).pop()
        data_store.scenario[placeholder_name] = win_handle


@step("Fullscreen")
def fullscreen() -> None:
    driver().fullscreen_window()
    _page_ready()


@step("Maximize")
def maximize() -> None:
    driver().maximize_window()
    _page_ready()


@step("Window size <width>x<height>")
def window_size(width_param: str, height_param: str) -> None:
    width = int(substitute(width_param))
    height = int(substitute(height_param))
    outer_width, inner_width, outer_height, inner_height = driver().execute_script("""
    return [window.outerWidth, window.innerWidth, window.outerHeight, window.innerHeight]""")
    if outer_width == 0:
        outer_width = inner_width
    if outer_height == 0:
        outer_height = inner_height
    report().log_debug("outer width: {}, inner width: {}, width: {}, outer height: {}, inner height: {}, height: {}"\
        .format(outer_width, inner_width, width, outer_height, inner_height, height))
    driver().set_window_size(outer_width - inner_width + width, outer_height - inner_height + height)
    _page_ready()


@step("Close current window")
def close_current_window() -> None:
    driver().close()
    window_handles = driver().window_handles
    last_handle = len(window_handles) - 1
    if last_handle >= 0:
        driver().switch_to.window(window_handles[last_handle])
    _page_ready()


@step("Close other windows")
def close_other_windows() -> None:
    current_handle = driver().current_window_handle
    for handle in driver().window_handles:
        if handle != current_handle:
            driver().switch_to.window(handle)
            driver().close()
    driver().switch_to.window(current_handle)
    _page_ready()


@step("Refresh")
def refresh() -> None:
    driver().refresh()
    _page_ready()


@step("Back")
def back() -> None:
    driver().back()
    _page_ready()


@step("Forward")
def forward() -> None:
    driver().forward()
    _page_ready()


@step("Open <page>")
def open_page(page_param: str) -> None:
    page = substitute(page_param)
    basic_auth_list = data_store.spec.get(basic_auth_key, [])
    webdriver = driver()
    uses_basic_auth = False
    for regexp, authorization in basic_auth_list:
        if re.match(regexp, page):
            uses_basic_auth = True
            report().log(f"URL matches `{regexp}` - using basic auth")
            # ToDo: rewrite this, when the BiDi API is more mature and there is a way to
            # reuse the connection over multiple Gauge steps with async/trio.
            webdriver.execute_cdp_cmd("Network.enable", {})
            webdriver.execute_cdp_cmd("Network.setExtraHTTPHeaders", ({"headers": {"Authorization": f"Basic {authorization}"}}))
            webdriver.get(page)
            webdriver.execute_cdp_cmd("Network.disable", {})
            break
    if not uses_basic_auth:
        webdriver.get(page)
    _init_opened_page(page)


@step("Open <page> for <user>: <password>")
def open_page_for_user_and_password(page_param: str, user_param: str, password_param: str) -> None:
    report().log("This step is deprecated for security concerns. Instead use:")
    report().log("`* Register authentication <user>: <password> for <regexp>`")
    page = substitute(page_param)
    prefix_match = re.match(r"https?://", page)
    prefix = prefix_match.group(0) if prefix_match else ""
    page = page[len(prefix):]
    user = urllib.parse.quote_plus(substitute(user_param))
    password = urllib.parse.quote_plus(substitute(password_param))
    url = "{}{}:{}@{}".format(prefix, user, password, page)
    driver().get(url)
    _init_opened_page(page)


@step("Register authentication <user>: <password> for <regexp>")
def register_basic_auth_for_regexp(user_param: str, password_param: str, regexp_param: str):
    # Basic auth with CDP is not supported by all browsers yet
    username = substitute(user_param)
    password = substitute(password_param)
    regexp = substitute(regexp_param)
    authorization = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    auth_list = data_store.spec.get(basic_auth_key, [])
    auth_list.append((regexp, authorization, ))
    data_store.spec[basic_auth_key] = auth_list


@step("Remove authentication for <regexp>")
def remove_basic_auth_for_regexp(regexp_param: str):
    regexp = substitute(regexp_param)
    auth_list = data_store.spec.get(basic_auth_key, [])
    auth_list[:] = filterfalse(lambda t: regexp == t[0], auth_list)


@step("Print window handles")
def print_window_handles() -> None:
    window_handles = driver().window_handles
    report().log("Windows: [{}]".format(", ".join(window_handles)))


@step("Print contexts")
def print_contexts() -> None:
    contexts = driver().contexts
    report().log("Contexts: [{}]".format(", ".join(contexts)))


@step("Switch to window <window_param>")
def switch_to_window(window_param: str) -> None:
    target_window = substitute(window_param)
    if target_window.isdigit():
        window_num = int(target_window)
        wait_until(lambda driver: len(driver.window_handles) > window_num, f"number of window handles is less than {window_num + 1}")
        window_name = driver().window_handles[window_num]
        driver().switch_to.window(window_name)
        report().log(f"Switched to window with index {window_num} and name {window_name}")
        _page_ready()
    else:
        original_window = driver().current_window_handle
        def find_and_switch_window(driver: Remote) -> bool:
            try:
                driver.switch_to.window(target_window)
                return True
            except NoSuchWindowException:
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    if driver.title == target_window:
                        return True
                return False
        try:
            wait_until(find_and_switch_window)
            _page_ready()
            report().log(f"Switched to window with name {target_window}")
        except TimeoutException:
            #switch back to default when we did not find the desired window
            driver().switch_to.window(original_window)
            raise AssertionError(f"did not find window {target_window}")


@step("Switch to default content")
def switch_to_default_content() -> None:
    driver().switch_to.default_content()


@step("Switch to frame <frame_param>")
def switch_to_frame(frame_name_or_index_param: str) -> None:
    frame_param = substitute(frame_name_or_index_param)
    if frame_param.isdigit():
        index = int(frame_param)
        frames = find_elements("tag name", "frame")
        if len(frames) == 0:
            frames = find_elements("tag name", "iframe")
        assert len(frames) > 0, "no frames or iframes found in current page."
        assert len(frames) >= index, f"frame index {index} is higher than number of frames in current page: {len(frames)}"
        driver().switch_to.frame(frames[index])
    else:
        driver().switch_to.frame(frame_param)


@step("Switch to frame <by> = <by_value>")
def switch_to_frame_by_selector(by: str, by_value: str) -> None:
    frame = find_element(by, by_value)
    driver().switch_to.frame(frame)


@step("Switch to context <context_regexp>")
def switch_to_context(context_regexp_param) -> None:
    context_regexp = substitute(context_regexp_param)
    def find_context(driver: AppiumRemote) -> str | bool:
        for c in driver.contexts:
            if re.match(context_regexp, c):
                return c
        return False
    target_context = wait_until(find_context, f"no context found that matches {context_regexp}")
    report().log(f"Switching to context '{target_context}'")
    driver().switch_to.context(target_context)


@step("Dismiss alert")
def dismiss_alert() -> None:
    wait_until(EC.alert_is_present()).dismiss()
    driver().switch_to.default_content()


@step("Accept alert")
def accept_alert() -> None:
    wait_until(EC.alert_is_present()).accept()
    driver().switch_to.default_content()


@step("Answer in prompt <text>")
def answer_in_prompt(text: str) -> None:
    prompt_text = substitute(text)
    alert = wait_until(EC.alert_is_present())
    alert.send_keys(prompt_text)
    alert.accept()
    driver().switch_to.default_content()


@step("Take a screenshot <file>")
def take_screenshot(image_file_name_param: str) -> None:
    image_file_name = substitute(image_file_name_param)
    screenshot_file_path = create_screenshot(image_file_name)
    report().log_image(screenshot_file_path)


@step("Take a screenshot of <by> = <by_value> <file>")
def take_screenshot_of_element(by: str, by_value: str, image_file_name_param: str) -> None:
    element = find_element(by, by_value)
    image_file_name = substitute(image_file_name_param)
    screenshot_file_path = create_screenshot(image_file_name)
    pixel_ratio = _device_pixel_ratio()
    viewport_offset = _viewport_offset()
    crop_image(
        screenshot_file_path,
        element.location,
        element.size,
        pixel_ratio,
        viewport_offset
    )
    report().log_image(screenshot_file_path)


@step("Take screenshots of whole page <file>")
def take_screenshots_of_whole_page(image_file_name_param: str) -> None:
    if _is_firefox_page_screenshot_no_scrolling():
        image_file_name = substitute(image_file_name_param)
        screenshot_file_path = create_screenshot(image_file_name)
        report().log_image(screenshot_file_path)
    else:
        image_file_name = substitute(image_file_name_param)
        _screenshot_of_whole_page_with_scrolling(image_file_name)


def _screenshot_of_whole_page_with_scrolling(image_file_name: str) -> None:
    postfix = 1
    should_continue = True
    while should_continue:
        filename_with_postfix = "".join((image_file_name, "_", str(postfix)))
        postfix += 1
        take_screenshot(filename_with_postfix)
        current_offset = driver().execute_script("return window.pageYOffset")
        driver().execute_script("window.scrollBy(0, window.innerHeight)")
        time.sleep(0.3)
        after_scroll_offset = driver().execute_script("return window.pageYOffset")
        if after_scroll_offset <= current_offset or postfix > 32:
            should_continue = False


@step("Check <by> = <by_value>")
def check_element(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    if not element.is_selected():
        element.click()


@step("Uncheck <by> = <by_value>")
def uncheck_element(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    if element.is_selected():
        element.click()


@step("Select <by> = <by_value> option <select_key> = <select_value>")
def select_option(by: str, by_value: str, select_key_param: str, select_value_param: str) -> None:
    element = find_element(by, by_value)
    select_key = substitute(select_key_param)
    select_value = substitute(select_value_param)
    key = SelectKey.to_enum(select_key)
    Selector.select(element, select_value, key)


@step("Click <by> = <by_value>")
def click_element(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    element.click()


@step("Double click <by> = <by_value>")
def double_click_element(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    ActionChains(driver()).double_click(element).perform()


@step("Click <by> = <by_value> <key_down>")
def click_element_with_key_down(by: str, by_value: str, key_down_param: str) -> None:
    keys_down = KeyMapper.map_keys(substitute(key_down_param))
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    ac = ActionChains(driver())
    for key in keys_down:
        ac.key_down(key)
    ac.click(element)
    for key in keys_down:
        ac.key_up(key)
    ac.perform()


@step("Right click <by> = <by_value>")
def right_click_element(by: str, by_value: str) -> None:
    actionChains = ActionChains(driver())
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    actionChains.context_click(element).perform()


@step("Type <string>")
def type_string(a_string_param: str) -> None:
    a_string = substitute(a_string_param)
    if not _is_mobile_operating_system():
        ActionChains(driver())\
            .send_keys(a_string)\
            .perform()
    else:
        element = _focused_element()
        _ready_for_interaction(element)
        element.send_keys(a_string)


@step("Type <key_down> <string>")
def type_string_with_key_down(key_down_param: str, a_string_param: str) -> None:
    keys_down = KeyMapper.map_keys(substitute(key_down_param))
    a_string = substitute(a_string_param)
    ac = ActionChains(driver())
    for key in keys_down:
        ac.key_down(key)
    ac.send_keys(a_string)
    for key in keys_down:
        ac.key_up(key)
    ac.perform()


@step("Type <by> = <by_value> <string>")
def type_string_into_element(by: str, by_value: str, a_string_param: str) -> None:
    a_string = substitute(a_string_param)
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    element.clear()
    if not _is_mobile_operating_system():
        ActionChains(driver())\
            .click(element)\
            .send_keys(a_string)\
            .perform()
    elif config.is_app_test():
        element.click()
        _focused_element().send_keys(a_string)
    else:
        element.click()
        element.send_keys(a_string)


@step("Type <by> = <by_value> <key_down> <string>")
def type_string_into_element_with_key_down(by: str, by_value: str, key_down_param: str, a_string_param: str) -> None:
    keys_down = KeyMapper.map_keys(substitute(key_down_param))
    a_string = substitute(a_string_param)
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    element.clear()
    ac = ActionChains(driver())\
        .click(element)
    for key in keys_down:
        ac.key_down(key)
    ac.send_keys(a_string)
    for key in keys_down:
        ac.key_up(key)
    ac.perform()


@step("Send keys <keys>")
def send_keys(keys_param: str) -> None:
    send_keys = KeyMapper.map_keys(substitute(keys_param))
    ActionChains(driver())\
        .send_keys(send_keys)\
        .perform()


@step("Send keys <key_down> <keys>")
def send_keys_with_key_down(key_down_param: str, keys_param: str) -> None:
    keys_down = KeyMapper.map_keys(substitute(key_down_param))
    send_keys = KeyMapper.map_keys(substitute(keys_param))
    ac = ActionChains(driver())
    for key in keys_down:
        ac.key_down(key)
    ac.send_keys(send_keys)
    for key in keys_down:
        ac.key_up(key)
    ac.perform()


@step("Send <by> = <by_value> keys <keys>")
def send_keys_to_element(by: str, by_value: str, keys_param: str) -> None:
    send_keys = KeyMapper.map_keys(substitute(keys_param))
    element = find_element(by, by_value)
    wait_until(EC.element_to_be_clickable(element))
    ActionChains(driver())\
        .click(element)\
        .send_keys(send_keys)\
        .perform()


@step("Send <by> = <by_value> keys <key_down> <keys>")
def send_keys_to_element_with_key_down(by: str, by_value: str, key_down_param: str, keys_param: str) -> None:
    keys_down = KeyMapper.map_keys(substitute(key_down_param))
    send_keys = KeyMapper.map_keys(substitute(keys_param))
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    ac = ActionChains(driver())\
        .click(element)
    for key in keys_down:
        ac.key_down(key)
    ac.send_keys(send_keys)
    for key in keys_down:
        ac.key_up(key)
    ac.perform()


@step("Clear <by> = <by_value>")
def clear_element(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    element.clear()


@step("Mouse down <by> = <by_value>")
def mouse_down(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    ActionChains(driver()).move_to_element(element).click_and_hold(element).perform()


@step("Mouse up <by> = <by_value>")
def mouse_up(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    ActionChains(driver()).move_to_element(element).release(element).perform()


@step(["Move to <by> = <by_value>", "Scroll <by> = <by_value> into view"])
def move_into_view(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    # the following script is needed for some browsers
    driver().execute_script("arguments[0].scrollIntoView(true);", element)
    try:
        ActionChains(driver()).move_to_element(element).perform()
    except WebDriverException as e:
        # in some mobile browsers it fails
        report().log_debug(f"received exception while moving to {element}: {e}")
    wait_for_idle_element(by, by_value)


@step("Move to and center <by> = <by_value>")
def move_into_view_and_center(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    driver().execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
    wait_for_idle_element(by, by_value)


@step("Move out")
def move_out_of_view() -> None:
    element = find_element("css selector", "body")
    ActionChains(driver()).move_to_element_with_offset(element, 0, 0).perform()


@step(["Move over <by> = <by_value>", "Hover over <by> = <by_value>"])
def hover_over(by: str, by_value: str) -> None:
    element = find_element(by, by_value)
    ActionChains(driver()).move_to_element(element).perform()


@step("Drag and drop <by_source> = <by_value_source> into <by_dest> = <by_value_dest>")
def dragAndDropElement(by_source: str, by_value_source: str, by_dest: str, by_value_dest: str) -> None:
    sourceElement = find_element(by_source, by_value_source)
    destinationElement = find_element(by_dest, by_value_dest)
    _ready_for_interaction(sourceElement)
    _ready_for_interaction(destinationElement)
    ActionChains(driver()).drag_and_drop(sourceElement, destinationElement).perform()


@step("Upload file = <file_path> into <by> = <by_value>")
def uploadFile(file_path_param: str, by: str, by_value: str) -> None:
    file_path = substitute(file_path_param)
    element = find_element(by, by_value)
    _ready_for_interaction(element)
    element.send_keys(file_path)


@step("Execute <script>")
def execute_script(script_param: str) -> None:
    script = substitute(script_param)
    driver().execute_script(script)


@step("Execute <script> and save result in <placeholder>")
def execute_script_save_result(script_param: str, placeholder_name_param: str) -> None:
    script = substitute(script_param)
    placeholder_name = substitute(placeholder_name_param)
    res = driver().execute_script(script)
    data_store.scenario[placeholder_name] = res


@step("Execute <script> with <by> = <by_value> as <elem>")
def execute_script_on_element(script_param: str, by: str, by_value: str, elem_param: str) -> None:
    script = substitute(script_param)
    elem = substitute(elem_param)
    assert elem in script, f"no element with name '{elem}' is referred to in the script"
    found = find_element(by, by_value)
    driver().execute_script(f"var {elem}=arguments[0]; {script}", found)


@step("Execute <script> with <by> = <by_value> as <elem> and save result in <placeholder>")
def execute_script_on_element_save_result(script_param: str, by: str, by_value: str, elem_param: str, placeholder_name_param: str) -> None:
    script = substitute(script_param)
    elem = substitute(elem_param)
    placeholder_name = substitute(placeholder_name_param)
    assert elem in script, f"no element with name '{elem}' is referred to in the script"
    found = find_element(by, by_value)
    res = driver().execute_script(f"var {elem}=arguments[0]; {script}", found)
    data_store.scenario[placeholder_name] = res


@step("Execute async <script>")
def execute_async_script(script_param: str) -> None:
    script = substitute(script_param)
    driver().execute_async_script(script)


@step("Execute async <script> and save result in <placeholder> with callback <callback>")
def execute_async_script_save_result(script_param: str, placeholder_name_param: str, callback_param: str) -> None:
    script = substitute(script_param)
    placeholder_name = substitute(placeholder_name_param)
    callback = substitute(callback_param)
    assert callback in script, f"no callback with name '{callback}' is invoked in the script"
    res = driver().execute_async_script(f"var {callback}=arguments[arguments.length-1]; {script}")
    data_store.scenario[placeholder_name] = res


@step("Execute async <script> with <by> = <by_value> as <elem>")
def execute_async_script_on_element(script_param: str, by: str, by_value: str, elem_param: str) -> None:
    script = substitute(script_param)
    elem = substitute(elem_param)
    assert elem in script, f"no element with name '{elem}' is referred to in the script"
    found = find_element(by, by_value)
    driver().execute_async_script(f"var {elem}=arguments[0]; {script}", found)


@step("Execute async <script> with <by> = <by_value> as <elem> and save result in <placeholder> with callback <callback>")
def execute_async_script_on_element_save_result(
    script_param: str,
    by: str,
    by_value: str,
    elem_param: str,
    placeholder_name_param: str,
    callback_param: str
) -> None:
    script = substitute(script_param)
    elem = substitute(elem_param)
    placeholder_name = substitute(placeholder_name_param)
    callback = substitute(callback_param)
    assert elem in script, f"no element with name '{elem}' is referred to in the script"
    assert callback in script, f"no callback with name '{callback}' is invoked in the script"
    found = find_element(by, by_value)
    res = driver().execute_async_script(f"var {elem}=arguments[0]; var {callback}=arguments[arguments.length-1]; {script}", found)
    data_store.scenario[placeholder_name] = res


@step("Save placeholder <placeholder> = <value>")
def save_placeholder(placeholder_name_param: str, placeholder_value_param: str) -> None:
    placeholder_name = substitute(placeholder_name_param)
    placeholder_value = substitute(placeholder_value_param)
    data_store.scenario[placeholder_name] = placeholder_value


@step("Save placeholder <placeholder> from <by> = <by_value>")
def save_placeholder_from_element(placeholder_name_param: str, by: str, by_value: str) -> None:
    placeholder_name = substitute(placeholder_name_param)
    text = get_text_from_element(by, by_value)
    data_store.scenario[placeholder_name] = text


@step("Save placeholder <placeholder> from attribute <attribute_param> of <by> = <by_value>")
def save_placeholder_from_element_attribute(placeholder_name_param: str, attribute_param: str, by: str, by_value: str) -> None:
    placeholder_name = substitute(placeholder_name_param)
    attribute = substitute(attribute_param)
    attribute_value = find_attribute(by, by_value, attribute)
    data_store.scenario[placeholder_name] = attribute_value


@step("Save window handles as <placeholder>")
def save_window_handles(placeholder_name_param: str) -> None:
    placeholder_name = substitute(placeholder_name_param)
    data_store.scenario[placeholder_name] = driver().window_handles


@step("Save window title as <placeholder>")
def save_window_title(placeholder_name_param: str) -> None:
    placeholder_name = substitute(placeholder_name_param)
    data_store.scenario[placeholder_name] = driver().title


@step("Set timeout <seconds>")
def set_timeout(seconds_param: str):
    seconds = substitute(seconds_param)
    assert seconds.replace('.', '', 1).isdigit(),\
        _err_msg(f"argument '{seconds_param}' should be a number")
    data_store.scenario[timeout_key] = float(seconds)


@step("Reset timeout")
def reset_timeout():
    del data_store.scenario[timeout_key]


# Steps Asserts ------------------------------------------------


@step("Show message in an error case <error_message>")
def show_error_message_in_case(error_msg_param: str) -> None:
    error_msg = substitute(error_msg_param)
    data_store.scenario[error_message_key] = error_msg


@step("Assert window handles is <windows_num>")
def assert_window_handle_num(window_num_param: str) -> None:
    window_num = substitute(window_num_param)
    expected = int(window_num)
    try:
        wait_until(lambda driver: expected == len(driver.window_handles))
    except TimeoutException:
        actual = len(driver().window_handles)
        raise AssertionError(_err_msg(f"expected {expected} window handles, got {actual}"))


@step("Assert title equals <title>")
def assert_title(expected_title_param: str) -> None:
    expected_title = substitute(expected_title_param)
    try:
        wait_until(lambda driver: driver.title == expected_title)
    except TimeoutException:
        current_title = driver().title
        raise AssertionError(_err_msg(f"expected title: {expected_title}, actual {current_title}"))


@step("Assert dialog text equals <text>")
def assert_dialog_text(expected_text_param: str) -> None:
    expected_text = substitute(expected_text_param)
    try:
        wait_until(lambda driver: driver.switch_to.alert.text == expected_text)
    except TimeoutException:
        dialog_text = driver().switch_to.alert.text
        # if no alert is present, a NoAlertPresentException is raised, which is fine
        raise AssertionError(_err_msg(f"expected dialog text: {expected_text}, actual {dialog_text}"))


@step("Assert url equals <url>")
def assert_url(expected_url_param: str) -> None:
    expected_url = substitute(expected_url_param)
    try:
        wait_until(lambda driver: driver.current_url == expected_url)
    except TimeoutException:
        current_url = driver().current_url
        raise AssertionError(_err_msg(f"url does not equal {expected_url}, got {current_url}"))


@step("Assert url starts with <url>")
def assert_url_starts_with(expected_url_param: str) -> None:
    expected_url = substitute(expected_url_param)
    try:
        wait_until(lambda driver: driver.current_url.startswith(expected_url))
    except TimeoutException:
        current_url = driver().current_url
        raise AssertionError(_err_msg(f"url does not start with {expected_url}, got {current_url}"))


@step("Assert url ends with <url>")
def assert_url_ends_with(expected_url_param: str) -> None:
    expected_url = substitute(expected_url_param)
    try:
        wait_until(lambda driver: driver.current_url.endswith(expected_url))
    except TimeoutException:
        current_url = driver().current_url
        raise AssertionError(_err_msg(f"url does not end with {expected_url}, got {current_url}"))


@step("Assert url contains <url>")
def assert_url_contains(expected_url_param: str) -> None:
    expected_url = substitute(expected_url_param)
    try:
        wait_until(lambda driver: expected_url in driver.current_url)
    except TimeoutException:
        current_url = driver().current_url
        raise AssertionError(_err_msg(f"url does not contain {expected_url}, got {current_url}"))


# see also before_step_hook
@step(["Assert <by> = <by_value> exists", "Assert <by> = <by_value> is displayed"])
def assert_element_exists(by: str, by_value: str) -> None:
    marker = get_marker(substitute(by), substitute(by_value))
    try:
        wait_until(EC.visibility_of_element_located(marker))
    except TimeoutException:
        raise AssertionError(_err_msg(f"element {by} = {by_value} does not exist"))


# see also before_step_hook
@step(["Assert <by> = <by_value> does not exist", "Assert <by> = <by_value> is invisible"])
def assert_element_does_not_exist(by_param: str, by_value_param: str) -> None:
    by = substitute(by_param)
    by_value = substitute(by_value_param)
    marker = get_marker(by, by_value)
    try:
        wait_until(EC.invisibility_of_element(marker))
    except TimeoutException:
        raise AssertionError(_err_msg(f"element {by} = {by_value} exists"))


@step("Assert <by> = <by_value> is enabled")
def assert_element_is_enabled(by: str, by_value: str) -> None:
    try:
        wait_until(lambda _: find_element(by, by_value).is_enabled())
    except TimeoutException:
        raise AssertionError(_err_msg(f"element {by} = {by_value} is disabled"))


@step("Assert <by> = <by_value> is disabled")
def assert_element_is_disabled(by: str, by_value: str) -> None:
    try:
        wait_until(lambda _: not find_element(by, by_value).is_enabled())
    except TimeoutException:
        raise AssertionError(_err_msg(f"element {by} = {by_value} is enabled"))


@step("Assert <by> = <by_value> is selected")
def assert_element_is_selected(by: str, by_value: str) -> None:
    try:
        wait_until(lambda _: find_element(by, by_value).is_selected())
    except TimeoutException:
        element = find_element(by, by_value, immediately=True)
        if element is None:
            raise AssertionError(_err_msg(f"no element {by} = {by_value} found"))
        raise AssertionError(_err_msg(f"element {by} = {by_value} is not selected"))


@step("Assert <by> = <by_value> has selected value <value>")
def assert_selected_option(by: str, by_value: str, expected_param: str) -> None:
    expected = substitute(expected_param)
    try:
        wait_until(lambda _: Selector.get_selected_value(find_element(by, by_value)) == expected)
    except TimeoutException:
        element = find_element(by, by_value, immediately=True)
        if element is None:
            raise AssertionError(_err_msg(f"no element {by} = {by_value} found"))
        actual = Selector.get_selected_value(element)
        raise AssertionError(_err_msg(f"expected value: {expected}, actual {actual}"))


@step("Assert <by> = <by_value> is not selected")
def assert_element_is_not_selected(by: str, by_value: str) -> None:
    try:
        wait_until(lambda _: not find_element(by, by_value).is_selected())
    except TimeoutException:
        element = find_element(by, by_value, immediately=True)
        if element is None:
            raise AssertionError(_err_msg(f"no element {by} = {by_value} found"))
        raise AssertionError(_err_msg(f"element {by} = {by_value} is selected"))


@step("Assert <by> = <by_value> equals <string>")
def assert_text_equals(by: str, by_value: str, expected_text_param: str) -> None:
    expected_text = substitute(expected_text_param)
    try:
        wait_until(lambda _: get_text_from_element(by, by_value) == expected_text)
    except TimeoutException:
        text = get_text_from_element(by, by_value, immediately=True)
        raise AssertionError(_err_msg(f"element {by} = {by_value} expected text {expected_text}, actual {text}"))


@step("Assert <by> = <by_value> does not equal <string>")
def assert_text_does_not_equal(by: str, by_value: str, expected_text_param: str) -> None:
    expected_text = substitute(expected_text_param)
    try:
        wait_until(lambda _: get_text_from_element(by, by_value) != expected_text)
    except TimeoutException:
        text = get_text_from_element(by, by_value, immediately=True)
        raise AssertionError(_err_msg(f"element {by} = {by_value} has unexpected text {text}"))


@step("Assert <by> = <by_value> regexp <regexp>")
def assert_regexp_in_element(by: str, by_value: str, regexp_param: str) -> None:
    regexp = substitute(regexp_param)
    try:
        wait_until(lambda _: re.match(regexp, get_text_from_element(by, by_value)))
    except TimeoutException:
        text = get_text_from_element(by, by_value, immediately=True)
        raise AssertionError(_err_msg(f"element {by} = {by_value}: regexp {regexp} does not match {text}"))


@step("Assert <by> = <by_value> contains <string>")
def assert_text_contains(by: str, by_value: str, contains_text_param: str) -> None:
    contains_text = substitute(contains_text_param)
    try:
        wait_until(lambda _: contains_text in get_text_from_element(by, by_value))
    except TimeoutException:
        text = get_text_from_element(by, by_value, immediately=True)
        raise AssertionError(_err_msg(f"element {by} = {by_value} expected actual {text} to contain {contains_text}"))


@step("Assert <by> = <by_value> does not contain <string>")
def assert_text_does_not_contain(by: str, by_value: str, contains_text_param: str) -> None:
    contains_text = substitute(contains_text_param)
    try:
        wait_until(lambda _: contains_text not in get_text_from_element(by, by_value))
    except TimeoutException:
        text = get_text_from_element(by, by_value, immediately=True)
        raise AssertionError(_err_msg(f"element {by} = {by_value} expected actual {text} to not contain {contains_text}"))


@step("Assert <by> = <by_value> css <css_property_name> is <css_expected_value>")
def assert_css_property(by: str, by_value: str, css_property_name_param: str, css_expected_value_param: str) -> None:
    css_property_name = substitute(css_property_name_param)
    css_expected_value = substitute(css_expected_value_param)
    try:
        wait_until(lambda _: css_expected_value == find_element(by, by_value).value_of_css_property(css_property_name))
    except TimeoutException:
        element = find_element(by, by_value, immediately=True)
        css_actual_value = element.value_of_css_property(css_property_name) if element is not None else "None"
        raise AssertionError(_err_msg(f"element {by} = {by_value}: css property {css_property_name} expected: {css_expected_value}, actual: {css_actual_value}"))


@step("Assert <by> = <by_value> is focused")
def assert_element_is_focused(by: str, by_value: str) -> None:
    try:
        wait_until(lambda _: find_element(by, by_value) == _focused_element())
    except TimeoutException:
        raise AssertionError(_err_msg(f"element {by} = {by_value} is not in focus"))


@step("Assert <by> = <by_value> attribute <attribute> exists")
def assert_attribute_exists(by: str, by_value: str, attribute_param: str) -> None:
    attribute = substitute(attribute_param)
    try:
        wait_until(lambda _: find_attribute(by, by_value, attribute))
    except TimeoutException:
        raise AssertionError(_err_msg(f"element {by} = {by_value} has no attribute {attribute}"))


@step("Assert <by> = <by_value> attribute <attribute> contains <value>")
def assert_attribute_contains(by: str, by_value: str, attribute_param: str, value_param: str) -> None:
    attribute = substitute(attribute_param)
    value = substitute(value_param)
    def attribute_contains_value(_: Remote) -> bool:
        found = find_attribute(by, by_value, attribute)
        return isinstance(found, str) and value in found
    try:
        wait_until(attribute_contains_value)
    except TimeoutException:
        found_value = find_attribute(by, by_value, attribute, immediately=True)
        if found_value is None:
            msg = _err_msg(f"element {by} = {by_value} has no attribute {attribute}")
        elif found_value is True:
            msg = _err_msg(f"attribute {attribute} in element {by} = {by_value} is empty")
        else:
            msg = _err_msg(f"attribute {attribute} in element {by} = {by_value} does not contain {value} - found: {found_value}")
        raise AssertionError(msg)


@step("Assert <by> = <by_value> attribute <attribute> equals <value>")
def assert_attribute_equals(by: str, by_value: str, attribute_param: str, value_param: str) -> None:
    attribute = substitute(attribute_param)
    value = substitute(value_param)
    try:
        wait_until(lambda _: value == find_attribute(by, by_value, attribute))
    except TimeoutException:
        found_value = find_attribute(by, by_value, attribute, immediately=True)
        if found_value is None:
            msg = _err_msg(f"element {by} = {by_value} has no attribute {attribute}")
        elif found_value is True:
            msg = _err_msg(f"attribute {attribute} in element {by} = {by_value} is empty")
        else:
            msg = _err_msg(f"attribute {attribute} in element {by} = {by_value} does not equal {value} - found: {found_value}")
        raise AssertionError(msg)


@step("Assert <by> = <by_value> attribute <attribute> does not contain <value>")
def assert_attribute_does_not_contain(by: str, by_value: str, attribute_param: str, value_param: str) -> None:
    attribute = substitute(attribute_param)
    value = substitute(value_param)
    def attribute_does_not_contain_value(_: Remote) -> bool:
        found = find_attribute(by, by_value, attribute)
        return isinstance(found, str) and value not in found
    try:
        wait_until(attribute_does_not_contain_value)
    except TimeoutException:
        found_value = find_attribute(by, by_value, attribute, immediately=True)
        raise AssertionError(_err_msg(f"attribute {attribute} in element {by} = {by_value} contains {value} - found: {found_value}"))


@step("Assert <by> = <by_value> screenshot resembles <file> with SSIM more than <threshold>")
def assert_image_resembles(by: str, by_value: str, image_file_name_param: str, threshold_param: str) -> None:
    element = find_element(by, by_value)
    threshold = float(substitute(threshold_param))
    assert 0.0 <= threshold <= 1.0, "threshold must be between 0.0 and 1.0"
    pixel_ratio = _device_pixel_ratio()
    viewport_offset = _viewport_offset()
    image_file_name = substitute(image_file_name_param)
    ssim = get_structured_similarity_to_expected(image_file_name, element.location, element.size, pixel_ratio, viewport_offset)
    assert ssim >= threshold, \
        _err_msg(f"SSIM {ssim} is less than threshold {threshold}")


@step("Assert page screenshots resemble <file> with SSIM more than <threshold>")
def assert_whole_page_resembles(image_file_name_param: str, threshold_param: str) -> None:
    threshold = float(substitute(threshold_param))
    assert 0.0 <= threshold <= 1.0, "threshold must be between 0.0 and 1.0"
    image_file_name = substitute(image_file_name_param)
    if _is_firefox_page_screenshot_no_scrolling():
        failed_asserts = ssim_screenshot_noscrolling(image_file_name, threshold)
    else:
        failed_asserts = ssim_screenshot_scrolling(image_file_name, threshold)
    assert len(failed_asserts) == 0,\
            _err_msg("Assertions failed:\n\t{}".format("\n\t".join(failed_asserts)))


@step("Assert page screenshots resemble <file> with SSIM more than <threshold> for <pages> pages")
def assert_pages_resemble(image_file_name_param: str, threshold_param: str, pages_param: str) -> None:
    """This step exists in case the upper step does not work, f.i. due to framework restrictions"""
    threshold = float(substitute(threshold_param))
    assert 0.0 <= threshold <= 1.0, "threshold must be between 0.0 and 1.0"
    image_file_name = substitute(image_file_name_param)
    pages = int(substitute(pages_param))
    failed_asserts = []
    for page in range(1, pages + 1):
        actual_screenshot_full_path = create_actual_screenshot_file_path(image_file_name, page)
        expected_screenshot_full_path = create_expected_screenshot_file_path(image_file_name, page)
        page += 1
        send_keys("PAGE_DOWN")
        wait_time = config.get_scroll_wait_time()
        time.sleep(wait_time)
        if not os.path.isfile(expected_screenshot_full_path):
            failed_asserts.append("screenshot {} does not exist".format(expected_screenshot_full_path))
        else:
            append_structured_similarity(failed_asserts, expected_screenshot_full_path, actual_screenshot_full_path, threshold)
    assert len(failed_asserts) == 0,\
            _err_msg("Assertions failed:\n\t{}".format("\n\t".join(failed_asserts)))


@step("Fail <message>")
def fail(message_param: str) -> None:
    message = substitute(message_param)
    report().log(message)
    assert False

@step("Print message <message>")
def print_message(message_param: str) -> None:
    message = substitute(message_param)
    report().log(message)

# Context methods -------------------------------------------


def driver() -> Remote | AppiumRemote:
    app_ctx: AppContext = data_store.spec[app_context_key]
    return app_ctx.driver


def report() -> Report:
    app_ctx: AppContext = data_store.spec[app_context_key]
    return app_ctx.report


# Private methods -------------------------------------------

def _init_opened_page(page) -> None:
    for _ in range(max_attempts):
        # Browsers sometimes open the page in the middle, when visited before
        _page_ready()
        if "#" not in page:
            try:
                driver().execute_script("window.scrollTo(0, 0);")
                break
            except JavascriptException:
                # In case of a page redirect the window object can become invalid.
                pass


def _page_ready() -> None:
    if config.is_app_test():
        # cannot execute script in native apps
        return
    try:
        wait_until(lambda driver: "complete" == driver.execute_script("return document.readyState"))
    except TimeoutException:
        # Some dynamic pages will never be ready
        pass


def _ready_for_interaction(element: WebElement) -> None:
    try:
        wait_until(EC.element_to_be_clickable(element))
    except TimeoutException:
        # best chance. But false negatives possible.
        pass


def _device_pixel_ratio() -> int:
    return int(driver().execute_script("return window.devicePixelRatio"))


def _viewport_offset() -> int:
    return int(driver().execute_script("return window.pageYOffset"))

def _is_firefox_page_screenshot_no_scrolling() -> bool:
    return config.get_browser() == Browser.FIREFOX and config.is_whole_page_screenshot()


def _is_mobile_operating_system() -> bool:
    return config.get_operating_system().is_mobile()


def _focused_element() -> WebElement:
    return driver().switch_to.active_element


def _err_msg(default_msg: str) -> str:
    return str(data_store.scenario.get(error_message_key, default_msg))
