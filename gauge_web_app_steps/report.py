#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os

from collections.abc import Iterable
from getgauge.python import Messages, ExecutionContext


class Report(object):
    """
    Here you find methods related to writing to gauge reports.
    """

    def __init__(self, context: ExecutionContext = None, debug=False) -> None:
        self.context = context
        self.debug = debug

    def _spec_html_report_dir(self) -> str:
        gauge_project_dir = os.environ.get("GAUGE_PROJECT_ROOT")
        spec_file = self.context.specification.file_name
        spec_dir = os.path.dirname(spec_file)
        spec_dir_rel = spec_dir[len(gauge_project_dir)+1:]
        gauge_reports_dir = os.environ.get("gauge_reports_dir", "reports")
        html_report_dir = os.path.join(gauge_reports_dir, "html-report")
        if not os.path.isabs(html_report_dir):
            html_report_dir = os.path.join(gauge_project_dir, html_report_dir)
        spec_report_dir = os.path.join(html_report_dir, spec_dir_rel)
        return spec_report_dir

    def log(self, message="") -> None:
        """
        Log to terminal and write into the gauge report the given string
        """
        print(message)  # > terminal
        Messages.write_message(message)  # > html report

    def log_debug(self, message="") -> None:
        if not self.debug:
            return
        self.log(message)

    def log_image(self, image_file_path, label="") -> None:
        """
        Include an image into the gauge report.
        The relative path from the report to the image will be used in the created html.
        """
        spec_report_dir = self._spec_html_report_dir()
        rel_path_report_to_image = os.path.relpath(image_file_path, spec_report_dir)
        html_rel_path = rel_path_report_to_image.replace('\\', '/')
        Messages.write_message(
            "<a href='{0}'><img src='{0}' height='165'/></a><label>{1}</label>".format(html_rel_path, label))

    def log_image_info(self, name, image) -> None:
        """
        Include information about the given image into the gauge report.
        The image parameter is expected to be a multidimensional array,
        just as the skimage library works with.
        """
        if not self.debug:
            return
        self.log()
        self.log("Image Info: %s" % (name,))
        self.log("Size: %sx%s" % (len(image[0]), len(image),))
        depth = 1
        channel = image
        while isinstance(channel, Iterable):
            self.log("Channel %s length: %s" % (depth, len(channel),))
            if not isinstance(channel[0], Iterable):
                self.log("Last channel values excerpt: [%s]" % (", ".join([str(i) for i in channel]),))
            channel = channel[0]
            depth += 1
        self.log("Channels: %s" % (depth,))
        self.log()
