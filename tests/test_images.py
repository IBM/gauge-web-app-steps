#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import shutil
import inspect
import unittest
from unittest.mock import MagicMock
from pathlib import Path
from parameterized import parameterized

from skimage import io

from gauge_web_app_steps.images import Images


class TestImages(unittest.TestCase):

    def setUp(self) -> None:
        self.test_instance = Images(MagicMock())
        # absolute path to this test class as a reference
        path = Path(inspect.getfile(self.__class__))
        absolute_path = path.parent.absolute()
        self.resource = os.path.join(absolute_path, "resources")
        self.out = os.path.join(absolute_path, "out")
        self.actual_path = os.path.join(self.resource, "card1.png")
        self.expected_path = os.path.join(self.resource, "card2.png")

    @parameterized.expand(["full", "gradient", "red", "color:fuchsia"])
    def test_adapt_and_compare_images(self, diff_format):
        merge = "card1_merged.png"
        self._remove_output_image_if_exists(merge)
        ssim = self.test_instance.adapt_and_compare_images(
            expected_screenshot_full_path=self.expected_path,
            actual_screenshot_full_path=self.actual_path,
            output_path=self.out,
            diff_formats=diff_format)
        self.assertGreater(ssim, 0.9)
        self.assertLess(ssim, 1)
        self.assertFalse(self._exists_output_image(merge))

    def test_adapt_and_compare_images_merged(self):
        merge = "card1_merged.png"
        self._remove_output_image_if_exists(merge)
        ssim = self.test_instance.adapt_and_compare_images(
            expected_screenshot_full_path=self.expected_path,
            actual_screenshot_full_path=self.actual_path,
            output_path=self.out,
            diff_formats="color:green",
            append_images=True)
        self.assertGreater(ssim, 0.9)
        self.assertLess(ssim, 1)
        self.assertTrue(self._exists_output_image(merge))
        self.assertFalse(self._exists_output_image("card1_green.png"))

    def test_crop_image_file(self):
        file = self._prepare_test_image()
        self.test_instance.crop_image_file(file,
            location={"x": 10, "y": 10},
            size={"width": 20, "height": 20},
            pixel_ratio=2, viewport_offset=10)
        img = io.imread(file)
        self.assertEqual((40, 40, 4), img.shape)

    def _prepare_test_image(self):
        # ensure that output folder exists
        if not os.path.exists(self.out):
            os.makedirs(self.out)
        # copy a test resource there for further operations
        shutil.copy(self.actual_path, self.out)
        return os.path.join(self.out, "card1.png")

    def _remove_output_image_if_exists(self, file_name):
        if self._exists_output_image(file_name):
            os.remove(os.path.join(self.out, file_name))

    def _exists_output_image(self, file_name):
        path = os.path.join(self.out, file_name)
        return os.path.exists(path)


if __name__ == '__main__':
    unittest.main()
