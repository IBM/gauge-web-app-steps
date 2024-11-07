#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import numpy as np
import os
import shutil
import unittest
from numpy import uint8
from skimage import img_as_ubyte, io
from unittest.mock import MagicMock
from parameterized import parameterized

from gauge_web_app_steps.images import Images
from tests import TEST_RESOURCES_DIR, TEST_OUT_DIR


class TestImages(unittest.TestCase):

    def setUp(self) -> None:
        self.test_instance = Images(MagicMock())
        self.actual_image = os.path.join(TEST_OUT_DIR, "actual_screenshots", "actual_rgba.png")
        self.actual_image_rgb = os.path.join(TEST_OUT_DIR, "actual_screenshots", "actual_rgb.png")
        self.expected_image = os.path.join(TEST_RESOURCES_DIR, "expected_rgba.png")
        self.expected_image_rgb = os.path.join(TEST_RESOURCES_DIR, "expected_rgb.png")
        self.diffs_dir = os.path.join(TEST_OUT_DIR, "diffs")
        self.crop_dir = os.path.join(TEST_OUT_DIR, "crop")
        os.makedirs(os.path.join(TEST_OUT_DIR, "actual_screenshots"), exist_ok=True)
        os.makedirs(self.diffs_dir, exist_ok=True)
        os.makedirs(self.crop_dir, exist_ok=True)
        # the actual image file might be altered during the test, so the test runs on a copy
        shutil.copy(os.path.join(TEST_RESOURCES_DIR, "actual_rgb.png"), self.actual_image_rgb)
        shutil.copy(os.path.join(TEST_RESOURCES_DIR, "actual_rgba.png"), self.actual_image)

    @parameterized.expand(["full", "gradient", "red", "color:fuchsia"])
    def test_adapt_and_compare_images(self, diff_format:str):
        mergefile = os.path.join(self.diffs_dir, "actual_rgba_merged.png")
        self._remove_image_if_it_exists(mergefile)
        expected_diff_file = os.path.join(self.diffs_dir, f"actual_rgba_{diff_format.removeprefix('color:')}.png")
        self._remove_image_if_it_exists(expected_diff_file)
        ssim = self.test_instance.adapt_and_compare_images(
            expected_screenshot_full_path=self.expected_image,
            actual_screenshot_full_path=self.actual_image,
            output_path=self.diffs_dir,
            diff_formats=diff_format)
        self.assertGreater(ssim, 0.9)
        self.assertLess(ssim, 1)
        self.assertFalse(os.path.exists(mergefile))
        self.assertTrue(os.path.exists(expected_diff_file), f"{expected_diff_file} does not exist")

    def test__align_alpha_channel_of_actual_image__no_change(self):
        img_expected = io.imread(self.expected_image)
        img_actual = io.imread(self.actual_image)
        result = self.test_instance._align_alpha_channel_of_actual_image(img_expected, img_actual)
        self.assertTrue(img_actual is result)

    def test__align_alpha_channel_of_actual_image__add_alpha(self):
        img_expected = io.imread(self.expected_image)
        img_actual = io.imread(self.actual_image_rgb)
        result = self.test_instance._align_alpha_channel_of_actual_image(img_expected, img_actual)
        before_color_depth = img_actual.shape[2]
        result_color_depth = result.shape[2]
        self.assertEqual(3, before_color_depth)
        self.assertEqual(4, result_color_depth)

    def test__align_alpha_channel_of_actual_image__remove_alpha(self):
        img_expected = io.imread(self.expected_image_rgb)
        img_actual = io.imread(self.actual_image)
        result = self.test_instance._align_alpha_channel_of_actual_image(img_expected, img_actual)
        before_color_depth = img_actual.shape[2]
        result_color_depth = result.shape[2]
        self.assertEqual(4, before_color_depth)
        self.assertEqual(3, result_color_depth)

    def test_adapt_and_compare_images_merged(self):
        mergefile = os.path.join(self.diffs_dir, "actual_rgba_merged.png")
        self._remove_image_if_it_exists(mergefile)
        ssim = self.test_instance.adapt_and_compare_images(
            expected_screenshot_full_path=self.expected_image,
            actual_screenshot_full_path=self.actual_image,
            output_path=self.diffs_dir,
            diff_formats="color:green",
            append_images=True)
        self.assertGreater(ssim, 0.9)
        self.assertLess(ssim, 1)
        self.assertTrue(os.path.exists(mergefile))
        diff_file = os.path.join(self.diffs_dir, "actual_rgba_green.png")
        self.assertFalse(os.path.exists(diff_file))

    def test_crop_image_file(self):
        file = self._prepare_crop_image()
        self.test_instance.crop_image_file(file,
            location={"x": 10, "y": 10},
            size={"width": 20, "height": 20},
            pixel_ratio=2, viewport_offset=10)
        img = io.imread(file)
        self.assertEqual((40, 40, 4), img.shape)

    def test__pad_images__pad_actual(self):
        img_actual = self._create_img(3, 3)
        img_expected = self._create_img(4, 4)
        img_actual_padded, img_expected_padded = self.test_instance._pad_images(img_actual, img_expected)
        self.assertTrue(img_expected is img_expected_padded)
        self.assertTupleEqual((4, 4, 4), img_actual_padded.shape)
        padded_color = img_actual_padded[3][3]
        expected_color = [255, 0, 0, 255]
        self.assertListEqual(expected_color, padded_color.tolist())

    def test__pad_images__pad_expected(self):
        img_actual = self._create_img(4, 4)
        img_expected = self._create_img(3, 3)
        img_actual_padded, img_expected_padded = self.test_instance._pad_images(img_actual, img_expected)
        self.assertTrue(img_actual is img_actual_padded)
        self.assertTupleEqual((4, 4, 4), img_expected_padded.shape)
        padded_color = img_expected_padded[3][3]
        expected_color = [255, 0, 0, 255]
        self.assertListEqual(expected_color, padded_color.tolist())

    def _create_img(self, width: int, height: int) -> np.ndarray:
        color = [215, 215, 215, 255]
        width = [color for _ in range(width)]
        img = np.array([width for _ in range(height)], dtype=uint8)
        return img_as_ubyte(img)

    def _prepare_crop_image(self):
        # copy a test resource there for further operations
        target = os.path.join(self.crop_dir, "crop.png")
        shutil.copy(self.actual_image, target)
        return target

    def _remove_image_if_it_exists(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
