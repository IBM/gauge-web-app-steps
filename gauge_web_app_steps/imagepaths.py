#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import errno

from datetime import datetime
from string import Template

from .config import common_config as config


class ImagePath(object):

    def __init__(self, browser: str, headless: bool):
        self.browser_name = browser
        self.headless = headless

    def create_failure_screenshot_file_path(self) -> str:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S-%f")

        failure_screenshot_dir = self._create_screenshot_dir(config.get_failure_screenshot_dir())
        screenshot_file = "fail_{}.png".format(date_str)
        screenshot_file_path = os.path.join(failure_screenshot_dir, screenshot_file)
        return screenshot_file_path

    def create_screenshot_file_path(self, image_file_name: str) -> str:
        """
        Creates a new file name in the screenshot directory.
        The directory will be created if it does not exist yet.
        """
        file_name = image_file_name if image_file_name.endswith(".png") else "{}.png".format(image_file_name)
        return "/".join((self._screenshot_dir(), self._filename(file_name),))

    def create_actual_screenshot_file_path(self, image_file_name: str, running_number=None) -> str:
        """
        Creates a new file name in the actual_screenshot directory.
        The directory will be created if it does not exist yet.
        """
        actual_screenshot_dir = self._actual_screenshot_dir()
        actual_screenshot_full_path = self._create_screenshot_file_path(actual_screenshot_dir, image_file_name, running_number)
        return actual_screenshot_full_path

    def create_expected_screenshot_file_path(self, image_file_name: str, running_number=None) -> str:
        """
        Creates a new file name in the expected_screenshot directory.
        The directory will be created if it does not exist yet.
        """
        expected_screenshot_dir = self._expected_screenshot_dir()
        expected_screenshot_full_path = self._create_screenshot_file_path(expected_screenshot_dir, image_file_name, running_number)
        return expected_screenshot_full_path

    def _create_screenshot_file_path(self, screenshot_dir: str, image_file_name: str, running_number=None) -> str:
        filename_without_ext = image_file_name if not image_file_name.endswith(".png") else image_file_name[:-len(".png")]
        if running_number is None:
            file_name_parts = [self.browser_name, "_", filename_without_ext, ".png"]
        else:
            file_name_parts = [self.browser_name, "_", filename_without_ext, "_", str(running_number), ".png"]
        if self.headless:
            file_name_parts.insert(0, "headless_")
        file_name = "".join(file_name_parts)
        screenshot_full_path = os.path.join(screenshot_dir, file_name)
        return screenshot_full_path

    def _time_str(self) -> str:
        time_pattern = config.get_time_pattern()
        now = datetime.now()
        date_str = now.strftime(time_pattern)
        return date_str

    def _filename(self, name) -> str:
        pattern = config.get_file_name_pattern()
        class FileTemplate(Template):
            delimiter = "%"
        template = FileTemplate(pattern)
        subs = template.safe_substitute({
                "name"    : name if not name.endswith(".png") else name[:-len(".png")],
                "ext"     : "png",
                "browser" : self.browser_name,
                "time"    : self._time_str(),
        })
        return subs if subs.endswith(".png") else "{}.png".format(subs)

    def _screenshot_dir(self) -> str:
        return self._create_screenshot_dir(config.get_screenshot_dir())

    def _actual_screenshot_dir(self) -> str:
        return self._create_screenshot_dir(config.get_actual_screenshot_dir())

    def _expected_screenshot_dir(self) -> str:
        return self._create_screenshot_dir(config.get_expected_screenshot_dir())

    def _create_screenshot_dir(self, screenshot_dir) -> str:
        if not os.path.isabs(screenshot_dir):
            project_root = os.environ.get("GAUGE_PROJECT_ROOT")
            screenshot_dir = os.path.join(project_root, screenshot_dir)
        screenshot_dir = os.path.abspath(screenshot_dir)
        return self._create_dir(screenshot_dir)

    def _create_dir(self, dir_) -> str:
        try:
            os.makedirs(dir_)
        except OSError as e:
            # the directory might already exist. If not it is created.
            if e.errno != errno.EEXIST:
                raise
            pass
        return dir_
