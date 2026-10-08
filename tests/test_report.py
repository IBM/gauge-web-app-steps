#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import pathlib
import unittest
from unittest.mock import patch

from getgauge.python import ExecutionContext, Specification

from gauge_web_app_steps.report import Report


class TestReport(unittest.TestCase):

    def test_spec_html_report_dir(self):
        this_directory = str(pathlib.Path.cwd())
        spec = Specification("Test Spec", os.path.join(this_directory, "resources", "test_file.spec"), False, "")
        context = ExecutionContext(spec, None, None)
        self.report = Report(context=context)
        with patch.dict(os.environ, {
            "GAUGE_PROJECT_ROOT": this_directory,
            "gauge_reports_dir": "reports"
        }):
            result = self.report._spec_html_report_dir()
            self.assertIn(os.path.join("reports", "html-report", "resources"), result)


if __name__ == '__main__':
    unittest.main()
