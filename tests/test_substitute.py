#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import unittest
import os
import re
import time

from datetime import datetime
from getgauge.python import data_store

from gauge_web_app_steps.substitute import substitute
import pytest


class TestSubstitute(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print(f"{t:.3f}s")

    def test_substitute_replace(self):
        tableflip = "(ノಠ益ಠ)ノ彡┻━┻"
        os.environ["placeholder"] = tableflip
        result = substitute("${placeholder}")
        assert tableflip == result

    def test_substitute_with_full_math_expression(self):
        result = substitute("#{1 + 1}")
        assert "2" == result

    def test_substitute_with_inner_math_expression(self):
        result = substitute("\(^#{0 + 0}^)/")
        assert "\(^0^)/" == result

    def test_substitute_with_two_math_expressions(self):
        result = substitute("#{0 + 0}#{1 + 1}")
        assert "02" == result

    def test_substitute_complex(self):
        os.environ["a"] = "1"
        result = substitute("(${a} + 1) ** 2 = #{($a + 1) ** 2}")
        assert "(1 + 1) ** 2 = 4" == result

    def test_substitute_fails(self):
        result = substitute("}#{1 + 1")
        assert "}#{1 + 1" == result

    def test_substitute_with_bracket_diversions(self):
        result = substitute("}#{0 + 0}#{")
        assert "}0#{" == result

    def test_substitute_without_pipe_operator(self):
        placeholder1 = "lala"
        placeholder2 = "baba"
        os.environ["placeholder1"] = placeholder1
        data_store.scenario["placeholder2"] = placeholder2
        result = substitute("This is ${placeholder1}/url and ${placeholder2}")
        assert "This is lala/url and baba" == result

    def test_substitute_with_uuid_expression(self):
        result = substitute("!{uuid}")
        assert re.search("^[0-9a-f]{8}.[0-9a-f]{4}.[0-9a-f]{4}.[0-9a-f]{4}.[0-9a-f]{12}$", result)

    def test_substitute_with_time_expression(self):
        result = substitute("!{time}")
        assert self._datetime_valid(result)

    def test_substitute_with_time_and_format_expression(self):
        result = substitute("!{time:%Y}")
        assert re.fullmatch("[0-9]{4}", result) is not None

    def test_substitute_raises_with_invalid_time(self):
        with pytest.raises(ValueError):
            substitute("!{time-ly}")

    def test_substitute_raises_with_invalid_expression(self):
        with pytest.raises(ValueError):
            substitute("!{nonexistent}")


    def _datetime_valid(self, dt_str: str) -> bool:
        try:
            datetime.fromisoformat(dt_str)
        except ValueError:
            return False
        return True

if __name__ == '__main__':
    unittest.main()
