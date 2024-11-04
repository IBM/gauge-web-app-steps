#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import glob
import shutil
import unittest

from getgauge.python import data_store
from pathlib import Path
from unittest.mock import MagicMock, patch

from gauge_web_app_steps.web_app_steps import (
    suite_id_key,
    after_spec_hook, accept_alert, answer_in_prompt,
    assert_attribute_contains, assert_attribute_does_not_contain, assert_attribute_equals, assert_attribute_exists,
    assert_dialog_text, assert_element_exists, assert_element_does_not_exist,
    assert_element_is_selected, assert_element_is_not_selected, assert_selected_option,
    assert_text_contains, assert_text_does_not_contain, assert_text_does_not_equal, assert_text_equals,
    assert_title, assert_whole_page_resembles,
    before_spec_hook, check_element, click_element, double_click_element, driver,
    hover_over, move_into_view, move_out_of_view, mouse_down, mouse_up, open_page,
    save_placeholder_from_element, save_placeholder_from_element_attribute,
    select_option, switch_to_frame, switch_to_window,
    take_screenshots_of_whole_page, type_string, uncheck_element, wait_for

)
from gauge_web_app_steps.driver import Browser


@unittest.skipIf(os.environ.get("TEST_SKIP_IT", "0") == "1", "TEST_SKIP_IT env variable is set")
class TestWebAppStepsIT(unittest.TestCase):

    MAIN_PAGE: str = "https://the-internet.herokuapp.com"

    @classmethod
    def setUpClass(cls):
        data_store.suite.clear()
        data_store.suite[suite_id_key] = "suite-id"
        test_dir = os.path.abspath(os.path.dirname(__file__))
        cls.out = os.path.join(test_dir, "out")
        cls.browser = Browser.CHROME.value
        cls.env_patcher = patch.dict(os.environ, {
            "GAUGE_PROJECT_ROOT": cls.out,
            "driver_browser": cls.browser,
            "driver_platform_local_headless": "False",
            "driver_implicit_timeout": "7",
            "driver_manager_selenium4": "True"
        })
        cls.env_patcher.start()
        before_spec_hook(MagicMock())

    @classmethod
    def tearDownClass(cls):
        after_spec_hook()
        cls.env_patcher.stop()


    def setUp(self) -> None:
        self.screenshots_dir = os.path.join(TestWebAppStepsIT.out, "screenshots")

    def tearDown(self):
        if os.path.exists(self.screenshots_dir):
            shutil.rmtree(self.screenshots_dir)

    def _files(self):
        return glob.glob(self.screenshots_dir + f"{os.path.sep}*")

    def _open_page(self, page=MAIN_PAGE, sub_page=""):
        open_page(page + sub_page)
        wait_for("1")

    def test_assert_attribute(self):
        self._open_page()
        assert_attribute_contains("css selector", "#content", "class", "large-12")
        assert_attribute_equals("css selector", "#content", "class", "large-12 columns")
        assert_attribute_does_not_contain("css selector", "#content", "class", "large-13")

    def test_assert_attribute_exists(self):
        self._open_page(sub_page="/checkboxes")
        assert_attribute_exists("css selector", "#checkboxes input[checked]", "checked")

    def test_answer_in_prompt(self):
        self._open_page(sub_page="/javascript_alerts")
        click_element("xpath", "(//button)[3]")
        answer_in_prompt("foo")
        assert_text_equals("xpath", "//*[@id='result']", "You entered: foo")

    def test_assert_dialog_text(self):
        self._open_page(sub_page="/javascript_alerts")
        click_element("xpath", "(//button)[1]")
        assert_dialog_text("I am a JS Alert")
        accept_alert()

    def test_assert_dynamic_element_displayed(self):
        self._open_page(sub_page="/dynamic_loading/1")
        assert_element_does_not_exist("id", "finish")
        click_element("xpath", "//button")
        assert_element_exists("id", "finish")

    def test_assert_text(self):
        self._open_page()
        assert_text_contains("tag name", "h2", "Examples")
        assert_text_does_not_contain("tag name", "h2", "Shmexamples")

    def test_check(self):
        self._open_page(sub_page="/checkboxes")
        check_element("xpath", "(//input)[1]")
        uncheck_element("xpath", "(//input)[2]")
        assert_element_is_selected("xpath", "(//input)[1]")
        assert_element_is_not_selected("xpath", "(//input)[2]")

    def test_double_click(self):
        self._open_page(sub_page="/add_remove_elements/")
        double_click_element("xpath", "(//button)[1]")
        assert_text_equals("xpath", "(//button)[2]", "Delete")
        assert_text_does_not_equal("xpath", "(//button)[2]", "delete")
        assert_text_equals("xpath", "(//button)[3]", "Delete")

    def test_hover_over(self):
        self._open_page(sub_page="/hovers")
        hover_over("css selector", "div.figure:nth-child(3)")
        assert_element_exists("css selector", "div.figure:nth-child(3) > div.figcaption")

    def test_mouse_down_and_release(self):
        self._open_page(sub_page="/add_remove_elements/")
        mouse_down("xpath", "(//button)[1]")
        mouse_up("xpath", "(//button)[1]")
        assert_element_exists("xpath", "(//button)[2]")

    def test_move(self):
        self._open_page(sub_page="/hovers")
        move_into_view("css selector", "div.figure:nth-child(3)")
        assert_element_exists("css selector", "div.figure:nth-child(3) > div.figcaption")
        move_out_of_view()
        assert_element_does_not_exist("css selector", "div.figure:nth-child(3) > div.figcaption")

    def test_save_placeholder_from_element(self):
        self._open_page(sub_page="/inputs")
        click_element("xpath", "//input")
        type_string("5")
        save_placeholder_from_element("mynum", "tag name", "input")
        result = data_store.scenario.get("mynum")
        self.assertEqual("5", result)

    def test_save_placeholder_from_element_attribute(self):
        self._open_page()
        save_placeholder_from_element_attribute("myref", "href", "xpath", "//li[1]/a")
        result = data_store.scenario.get("myref")
        self.assertEqual("/abtest", result)

    def test_select_list_element(self):
        self._open_page(page="https://mdn.github.io/html-examples/custom-select/")
        select_option("id", "select", "index", "2")
        assert_selected_option("id", "select", "Beans")

    def test_switch_to_frame_by_name(self):
        self._open_page(sub_page="/nested_frames")
        switch_to_frame("frame-bottom")
        assert_text_equals("xpath", "/html/body", "BOTTOM")

    def test_switch_to_frame_by_index(self):
        self._open_page(sub_page="/nested_frames")
        switch_to_frame("1")
        assert_text_equals("xpath", "/html/body", "BOTTOM")

    def test_take_screenshots_of_whole_page_scrolling(self):
        os.environ["screenshot_whole_page_no_scroll"] = "False"
        self._open_page()
        take_screenshots_of_whole_page(self.__class__.__name__)
        self.assertGreater(len(self._files()), 1)

    #works only with Firefox => TODO: skip if not Firefox
    @unittest.SkipTest
    def test_take_screenshots_of_whole_page_no_scrolling(self):
        os.environ["screenshot_whole_page_no_scroll"] = "True"
        self._open_page()
        take_screenshots_of_whole_page(self.__class__.__name__)
        file = f"{TestWebAppStepsIT.browser}_{self.__class__.__name__}.png"
        src = os.path.join(self.screenshots_dir, file)
        dst_dir = os.path.join(self.out, "expected_screenshots")
        dst = os.path.join(dst_dir, file)
        Path(dst_dir).mkdir(exist_ok=True)
        shutil.copy(src, dst)
        assert_whole_page_resembles(self.__class__.__name__, "1.0")
        self.assertEqual(len(self._files()), 1)

    #the following tests should be executed at last because the switch windows
    def test_window_by_index(self):
        self._open_page()
        driver().switch_to.new_window('window')
        switch_to_window("0")
        assert_title("The Internet")

    def test_window_by_name(self):
        self._open_page()
        driver().switch_to.new_window('window')
        switch_to_window("The Internet")
        assert_title("The Internet")


if __name__ == '__main__':
    unittest.main()
