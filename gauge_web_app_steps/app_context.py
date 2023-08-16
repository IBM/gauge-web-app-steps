#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from getgauge.python import ExecutionContext, Specification
from selenium.webdriver import Remote

from .driver import Browser, DriverFactory
from .imagepaths import ImagePath
from .images import Images
from .report import Report
from .config import common_config as config
from .config import local_config, saucelabs_config


class AppContext:
    """
    Context objects are created and kept here.
    """

    def __init__(self, ctx: ExecutionContext = None) -> None:
        """Initiates objects used in the basic steps."""
        if ctx is None:
            # getgauge's loading mechanism might try to instantiate the class before the lib is ready.
            return
        self.report = Report(ctx, config.is_debug_log())
        self._report_driver_options()
        spec : Specification = ctx.specification
        self.driver = self._create_driver(spec.name)
        self.image_path = ImagePath(config.get_browser().value, config.is_headless())
        self.images = Images(self.report)
        self.diff_formats = config.get_diff_formats()
        self.mobile = config.get_operating_system().is_mobile()
        self.firefox_page_screenshot_no_scrolling = config.get_browser() == Browser.FIREFOX and config.is_whole_page_screenshot()

    def _create_driver(self, spec_name: str) -> Remote:
        driver_factory = DriverFactory.create_driver_factory(spec_name)
        return driver_factory.create_driver()

    def _report_driver_options(self) -> None:
        operating_system = config.get_operating_system()
        self.report.log(f"platform: {config.get_platform().value}")
        self.report.log(f"operating system: {operating_system}")
        self.report.log(f"operating system version: {config.get_operating_system_version()}")
        self.report.log(f"browser: {config.get_browser()}")
        self.report.log(f"page load timeout: {config.get_page_load_timeout()}")
        self.report.log(f"implicit timeout: {config.get_implicit_timeout()}")
        if config.get_platform().is_local():
            self.report.log(f"headless: {config.is_headless()}")
            if operating_system.is_mobile():
                self.report.log(f"device name: {local_config.get_mobile_device_name()}")
                self.report.log(f"real device: {local_config.get_mobile_real_device()}")
                self.report.log(f"device udid: {local_config.get_mobile_device_udid()}")
                self.report.log(f"appium server url: {local_config.get_mobile_appium_server_url()}")
        elif config.get_platform().is_remote():
            if operating_system.is_desktop():
                self.report.log(f"browser version: {saucelabs_config.get_browser_version()}")
            elif operating_system.is_mobile():
                self.report.log(f"device name: {saucelabs_config.get_device_name()}")
                self.report.log(f"appium version: {saucelabs_config.get_appium_version()}")
