#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest
import os

from getgauge.python import data_store
from unittest.mock import Mock, call

from gauge_web_app_steps.web_app_steps import (
    app_context_key, assert_element_exists, assert_element_does_not_exist,
    execute_async_script, execute_async_script_on_element, execute_async_script_on_element_save_result, execute_async_script_save_result,
    execute_script, execute_script_on_element, execute_script_on_element_save_result, execute_script_save_result,
    save_placeholder, switch_to_frame,
    _substitute
)


class TestWebAppSteps(unittest.TestCase):

    def setUp(self):
        data_store.scenario.clear()
        self.app_context = Mock()
        self.app_context.driver = Mock()
        data_store.spec[app_context_key] = self.app_context

    def test_assert_element_exists(self):
        self.assertRaises(AssertionError, lambda: assert_element_exists("id", "foo"))
        self.app_context.driver.find_element.assert_called()

    def test_assert_element_does_not_exist(self):
        self.assertRaises(AssertionError, lambda: assert_element_does_not_exist("id", "foo"))
        self.app_context.driver.find_element.assert_called()

    def test_save_placeholder(self):
        save_placeholder("placeholder-key", "placeholder_value")
        result = data_store.scenario.get("placeholder-key")
        self.assertEqual("placeholder_value", result)

    def test_substitute_replace(self):
        tableflip = "(ノಠ益ಠ)ノ彡┻━┻"
        os.environ["placeholder"] = tableflip
        result = _substitute("${placeholder}")
        self.assertEqual(tableflip, result)

    def test_substitute_with_full_math_expression(self):
        result = _substitute("#{1 + 1}")
        self.assertEqual("2", result)

    def test_substitute_with_inner_math_expression(self):
        result = _substitute("\(^#{0 + 0}^)/")
        self.assertEqual("\(^0^)/", result)

    def test_substitute_with_two_math_expressions(self):
        result = _substitute("#{0 + 0}#{1 + 1}")
        self.assertEqual("02", result)

    def test_substitute_complex(self):
        os.environ["a"] = "1"
        result = _substitute("(${a} + 1) ** 2 = #{($a + 1) ** 2}")
        self.assertEqual("(1 + 1) ** 2 = 4", result)

    def test_substitute_fails(self):
        result = _substitute("}#{1 + 1")
        self.assertEqual("}#{1 + 1", result)

    def test_substitute_with_bracket_diversions(self):
        result = _substitute("}#{0 + 0}#{")
        self.assertEqual("}0#{", result)

    def test_substitute_without_pipe_operator(self):
        placeholder1 = "lala"
        placeholder2 = "baba"
        os.environ["placeholder1"] = placeholder1
        data_store.scenario["placeholder2"] = placeholder2
        result = _substitute("This is ${placeholder1}/url and ${placeholder2}")
        self.assertEqual("This is lala/url and baba", result)

    def test_switch_to_frame_by_index(self):
        self.app_context.driver.find_elements = Mock(return_value=[])
        self.assertRaises(AssertionError, lambda: switch_to_frame("1"))
        self.app_context.driver.assert_has_calls([call.find_elements('tag name', 'frame'), call.find_elements('tag name', 'iframe')])

    def test_execute_script(self):
        execute_script("script")
        self.app_context.driver.assert_has_calls([call.execute_script("script")])

    def test_execute_script_save_result(self):
        self.app_context.driver.execute_script = Mock(return_value="result")
        execute_script_save_result("script", "placeholder")
        self.app_context.driver.assert_has_calls([call.execute_script("script")])
        self.assertEqual("result", data_store.scenario.get("placeholder"))

    def test_execute_script_on_element(self):
        elem = "web element"
        self.app_context.driver.find_element = Mock(return_value=elem)
        execute_script_on_element("script(elem)", "tag name", "p", "elem")
        self.app_context.driver.assert_has_calls([
            call.find_element("tag name", "p"),
            call.execute_script("var elem=arguments[0]; script(elem)", elem)
        ])

    def test_execute_script_on_element_save_result(self):
        elem = "web element"
        self.app_context.driver.find_element = Mock(return_value=elem)
        self.app_context.driver.execute_script = Mock(return_value="result")
        execute_script_on_element_save_result("script(elem)", "tag name", "p", "elem", "placeholder")
        self.app_context.driver.assert_has_calls([
            call.find_element("tag name", "p"),
            call.execute_script("var elem=arguments[0]; script(elem)", elem)
        ])
        self.assertEqual("result", data_store.scenario.get("placeholder"))

    def test_execute_async_script(self):
        execute_async_script("script")
        self.app_context.driver.assert_has_calls([call.execute_async_script("script")])

    def test_execute_async_script_save_result(self):
        self.app_context.driver.execute_async_script = Mock(return_value="result")
        execute_async_script_save_result("callback(result)", "placeholder", "callback")
        self.app_context.driver.assert_has_calls([call.execute_async_script("var callback=arguments[arguments.length-1]; callback(result)")])
        self.assertEqual("result", data_store.scenario.get("placeholder"))

    def test_execute_async_script_on_element(self):
        elem = "web element"
        self.app_context.driver.find_element = Mock(return_value=elem)
        execute_async_script_on_element("script(elem)", "tag name", "p", "elem")
        self.app_context.driver.assert_has_calls([
            call.find_element("tag name", "p"),
            call.execute_async_script("var elem=arguments[0]; script(elem)", elem)
        ])

    def test_execute_async_script_on_element_save_result(self):
        elem = "web element"
        self.app_context.driver.find_element = Mock(return_value=elem)
        self.app_context.driver.execute_async_script = Mock(return_value="result")
        execute_async_script_on_element_save_result("callback(elem.innerText)", "tag name", "p", "elem", "placeholder", "callback")
        self.app_context.driver.assert_has_calls([
            call.find_element("tag name", "p"),
            call.execute_async_script("var elem=arguments[0]; var callback=arguments[arguments.length-1]; callback(elem.innerText)", elem)
        ])
        self.assertEqual("result", data_store.scenario.get("placeholder"))


if __name__ == '__main__':
    unittest.main()
