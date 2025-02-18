#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import re
import numpy as np
import webcolors

from webcolors import HTML4
from warnings import warn
from skimage import img_as_ubyte
from skimage import color as skimg_color
from skimage import exposure as skimg_exposure
from skimage import io as skimg_io
from skimage import transform as skimg_transform
from skimage import util as skimg_util
from skimage.metrics import structural_similarity as compare_ssim

from .report import Report


class Images(object):
    """
    Functionality around image processing and comparison.
    """

    def __init__(self, report_: Report):
        self.report = report_

    def crop_image_file(
            self,
            screenshot_file_path: str,
            location: dict,
            size: dict,
            pixel_ratio: int,
            viewport_offset: int
    ):
        """
        Crop the specified image by the given dimensions.
        Parameters
        ----------
        screenshot_file_path : str
        location: Dict: {"x": int, "y": int}
            the upper left corner of the rectangle to be cropped out of the image
        size: Dict: {"width": int, "height": int}
            the size of the cropping
        pixel_ratio:
            for Retina displays this is usually 2, else 1
        viewport_offset:
            the offset of the browser's viewport
        """
        img = skimg_io.imread(screenshot_file_path)
        img = self._crop_image(img, location, size, pixel_ratio, viewport_offset)
        skimg_io.imsave(screenshot_file_path, img, check_contrast=False)
        self.report.log_image_info("screenshot {}".format(screenshot_file_path), img)

    def _crop_image(
            self,
            image,
            location,
            size,
            pixel_ratio: int,
            viewport_offset
    ):
        if pixel_ratio != 1:
            self.report.log("pixel ratio is %s" % (pixel_ratio,))
        start_x = int(location["x"]) * pixel_ratio
        start_y = int(location["y"]) * pixel_ratio - viewport_offset
        end_x = start_x + int(size["width"]) * pixel_ratio
        end_y = start_y + int(size["height"]) * pixel_ratio
        self.report.log("cropping image to element dimensions {}x{}".format((end_x - start_x), (end_y - start_y)))
        cropped_image = image[start_y: end_y, start_x: end_x]
        return cropped_image

    def adapt_and_compare_images(
            self,
            expected_screenshot_full_path: str,
            actual_screenshot_full_path: str,
            diff_formats="full",
            append_images=False,
            output_path=""
    ) -> float:
        """
        Calculates the SSIM between 2 images. Does rescaling and padding of the actual image, if necessary.
        Also prints a diff image to the report in different possible formats.
        Parameters
        ----------
        expected_screenshot_full_path : str
        actual_screenshot_full_path : str
        diff_formats : str
            One or more of the following in the same string: gradient, full, (color:red|color:green|color:fuchsia|...).
            The name of the color should a valid HTML color name: https://www.w3.org/TR/html401/types.html#h-6.5.
        append_images: if true, the diff image will be append to the expected screenshot
        output_path : optional path for the diff image, if not set it is equal to the path of the actual screenshot
        """
        img_expected = skimg_io.imread(expected_screenshot_full_path)
        img_actual_raw = skimg_io.imread(actual_screenshot_full_path)
        img_actual = self._align_alpha_channel_of_actual_image(img_expected, img_actual_raw)
        channel_axis = self._channel_axis(img_actual)
        self.report.log_debug(f"actual channel_axis: {channel_axis}")
        self.report.log_debug(f"expected channel_axis: {self._channel_axis(img_expected)}")
        img_actual = self._rescale_image(img_actual, img_expected, channel_axis)
        img_actual, img_expected = self._pad_images(img_actual, img_expected)
        if img_actual is not img_actual_raw:
            self.report.log_debug("Overwriting actual image after rescaling and padding")
            skimg_io.imsave(actual_screenshot_full_path, img_actual, check_contrast=False)
        self.report.log_image_info("actual", img_actual)
        self.report.log_image_info("expected", img_expected)
        img_list = []
        if append_images:
            img_list.append(img_expected)
        ssim, diff_images = self._compute_ssim_and_diff(img_actual, img_expected, diff_formats, channel_axis=channel_axis)
        if ssim < 1.0:
            self._save_diff_image(expected_screenshot_full_path, actual_screenshot_full_path, output_path,
                                  diff_images, img_list)
        self.report.log_debug("SSIM: {}\n".format(ssim))
        return ssim

    def _align_alpha_channel_of_actual_image(self, img_expected: np.ndarray, img_actual: np.ndarray) -> np.ndarray:
        expected_has_alpha = self._img_has_alpha(img_expected)
        actual_has_alpha = self._img_has_alpha(img_actual)
        if expected_has_alpha and not actual_has_alpha:
            self.report.log_debug("Adding alpha channel to actual image")
            rgba = np.insert(
                    img_actual,
                    3, # index in the color array [r,g,b,a]. index 3 -> a.
                    255, # value to insert at the index above: 255 is fully opaque
                    axis=2, # 0: height, 1: width, 2: color
            )
            return rgba
        elif not expected_has_alpha and actual_has_alpha:
            self.report.log_debug("Removing alpha channel from actual image")
            img_rgb = skimg_color.rgba2rgb(img_actual)
            return img_as_ubyte(img_rgb)
        else:
            return img_actual

    def _img_has_alpha(self, img: np.ndarray):
        height, width, color = img.shape
        # 4 bytes of color information indicates RGBa, 3 would be without.
        return color == 4

    def _channel_axis(self, img: np.ndarray):
        channel_axis = img.ndim - 1
        return channel_axis  # 2 dimensions: b/w, 3: color

    def _rescale_image(
            self,
            img,
            img_reference,
            channel_axis
    ):
        rescale_ratio = self._compute_rescale_ratio(img, img_reference)
        if rescale_ratio == 1.0:
            return img
        self.report.log("rescaling image by ratio {} to fit expected image size".format(rescale_ratio))
        img_rescaled = skimg_transform.rescale(
            img,
            rescale_ratio,
            channel_axis=channel_axis,
            anti_aliasing=True
        )
        # skimage uses different internal representations for an image.
        # https://scikit-image.org/docs/dev/user_guide/data_types.html
        # The rescale function returns an image with a different data type, so we convert it back.
        return img_as_ubyte(img_rescaled)

    def _compute_rescale_ratio(
            self,
            img,
            img_reference
    ):
        actual_height = len(img)
        reference_height = len(img_reference)
        if actual_height == reference_height:
            return 1.0
        actual_width = len(img[0])
        reference_width = len(img_reference[0])
        if actual_width == reference_width:
            return 1.0
        height_ratio = 1.0 * reference_height / actual_height
        width_ratio = 1.0 * reference_width / actual_width
        return height_ratio if height_ratio < width_ratio else width_ratio

    def _pad_images(
            self,
            img,
            img_ref
    ) -> tuple[np.ndarray, np.ndarray]:
        pad_bottom = len(img_ref) - len(img)
        pad_right = len(img_ref[0]) - len(img[0])
        if pad_bottom == pad_right == 0:
            return img, img_ref
        padded_ref_image = img_ref
        padded_image = img
        if pad_bottom < 0 or pad_right < 0:
            ref_pad_bottom = -min(pad_bottom, 0)
            ref_pad_right = -min(pad_right, 0)
            self.report.log(f"reference screenshot needs padding to match actual image size. padding bottom: {ref_pad_bottom}, padding right: {ref_pad_right}")
            padded_ref_image = self._pad_image(img_ref, ref_pad_bottom, ref_pad_right)
        if pad_bottom > 0 or pad_right > 0:
            act_pad_bottom = max(pad_bottom, 0)
            act_pad_right = max(pad_right, 0)
            self.report.log(f"screenshot needs padding to match expected image size. padding bottom: {act_pad_bottom}, padding right: {act_pad_right}")
            padded_image = self._pad_image(img, act_pad_bottom, act_pad_right)
        return padded_image, padded_ref_image

    def _pad_image(self, img: np.ndarray, pad_bottom: int, pad_right: int) -> np.ndarray:
        height, width, color = img.shape
        red = [255, 0, 0, 255] if self._img_has_alpha(img) else [255, 0, 0]
        red = np.array(red, dtype=np.uint8)
        right_pad_img = np.zeros((height, pad_right, color), dtype=np.uint8) + red
        padded = np.concatenate((img, right_pad_img), axis=1, dtype=np.uint8)
        bottom_pad_img = np.zeros((pad_bottom, width + pad_right, color), dtype=np.uint8) + red
        padded = np.concatenate((padded, bottom_pad_img), axis=0, dtype=np.uint8)
        return padded

    def _compute_ssim_and_diff(
            self,
            img_expected,
            img_actual,
            diff_formats,
            channel_axis
    ):
        ssim = None
        self.report.log_debug(f"using {diff_formats} to compare images")
        diff_images = {}
        if "gradient" in diff_formats and "full" in diff_formats:
            ssim, gradient, full = compare_ssim(img_actual, img_expected, channel_axis=channel_axis, gradient=True, full=True, data_range=255)
            diff_images["gradient"] = self._ssim_img_to_ubyte(gradient)
            diff_images["full"] = self._ssim_img_to_ubyte(full)
        elif "gradient" in diff_formats:
            ssim, gradient = compare_ssim(img_actual, img_expected, channel_axis=channel_axis, gradient=True, data_range=255)
            diff_images["gradient"] = self._ssim_img_to_ubyte(gradient)
        elif "full" in diff_formats:
            ssim, full = compare_ssim(img_actual, img_expected, channel_axis=channel_axis, full=True, data_range=255)
            diff_images["full"] = self._ssim_img_to_ubyte(full)
        if ssim is None:
            ssim = compare_ssim(img_actual, img_expected, channel_axis=channel_axis, data_range=255)
        if ssim < 1.0 and "red" in diff_formats:
            warn("The diff_format 'red' is deprecated. please use a key value pair: 'color=red'", DeprecationWarning)
            red = self._diff_images_color(img_expected, img_actual, "red")
            diff_images["red"] = red
        if ssim < 1.0 and "color:" in diff_formats:
            color_name = re.search("color:([a-z]*)", diff_formats).group(1)
            colored = self._diff_images_color(img_expected, img_actual, color_name)
            diff_images[color_name] = colored
        return ssim, diff_images

    def _ssim_img_to_ubyte(self, img: np.ndarray) -> np.ndarray:
        """ the returned image of *compare_ssim* has a weird format and must be converted back to uint8. """
        img = img * 0.5
        img = img.clip(min=-1.0, max=1.0)
        return img_as_ubyte(img)

    def _diff_images_color(
            self,
            img_expected,
            img_actual,
            color_name
    ):
        """
        Creates a diff image between two images.
        The diff will show any color differences by highlighting with the given color and reducing other colors.
        The name of the color should be HTML compliant.
        """
        color = list(webcolors.name_to_rgb(color_name, HTML4))
        self.report.log_debug("Expected: tranform to RGB float")
        img_expected_rgb = self._transform_to_rgb_float(img_expected)
        self.report.log_debug("Actual: tranform to RGB float")
        img_actual_rgb = self._transform_to_rgb_float(img_actual)
        img_diff = skimg_color.deltaE_cie76(img_expected_rgb, img_actual_rgb)  # Euclidean delta
        img_diff = skimg_color.gray2rgb(img_diff)
        img_diff = img_diff * color
        img_diff = img_expected_rgb + img_diff
        # Normalize the max pixel value, simultaneously graying out the parts of the original image.
        # then transform to 8bit colors
        img_diff = skimg_exposure.rescale_intensity(img_diff, in_range=(0., 2.), out_range=(0, 255))
        return img_diff.astype(np.uint8)

    def _transform_to_rgb_float(self, img):
        """
        Cut the alpha channel from an image, if present, and transform the data representation to float.
        Each channel will range between 0.0 and 1.0.
        """
        black = [0, 0, 0]
        if self._img_has_alpha(img):
            self.report.log_debug("Image has Alpha")
            return skimg_color.rgba2rgb(img, background=black)
        else:
            self.report.log_debug("Image has no Alpha")
            return skimg_util.img_as_float(img)

    def _save_diff_image(
            self,
            expected_screenshot_full_path,
            actual_screenshot_full_path,
            output_path,
            diff_images,
            img_list
    ):
        path = self._determine_target_path(actual_screenshot_full_path, output_path)
        for diff_format, diff_img in diff_images.items():
            if len(img_list) > 0:
                # append the images to the list to create a big one for visual comparing
                img_list.append(diff_img)
            else:
                # save diff images immediately
                diff_path = self._create_target_filename(path, diff_format)
                skimg_io.imsave(diff_path, diff_img, check_contrast=False)
                self.report.log_image(diff_path, f"Created {diff_format} diff for {expected_screenshot_full_path}")
        self._create_horizontal_aligned_diff(expected_screenshot_full_path, path, img_list)

    def _create_horizontal_aligned_diff(
            self,
            expected_screenshot_full_path,
            path,
            img_list
    ):
        """
        Creates a horizontally stacked image from expected image and diffs.
        """
        if len(img_list) > 1:
            diff_path = self._create_target_filename(path, "merged")
            reshaped = [self._transform_to_rgb_float(i) for i in img_list]
            merged = np.concatenate(reshaped, axis=1)
            merged = img_as_ubyte(merged)
            skimg_io.imsave(diff_path, merged, check_contrast=False)
            self.report.log_image(diff_path, f"Created merged diff for {expected_screenshot_full_path}")

    def _determine_target_path(
            self,
            actual_screenshot_full_path,
            output_path
    ):
        if not output_path or output_path.isspace():
            # output_path is None, empty or contains only whitespaces
            return actual_screenshot_full_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        filename = os.path.basename(actual_screenshot_full_path)
        return os.path.join(output_path, filename)

    def _create_target_filename(
            self,
            path,
            suffix
    ):
        return "{}_{}.png".format(path[:-len(".png")], suffix)
