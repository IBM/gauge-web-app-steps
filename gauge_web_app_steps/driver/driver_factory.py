#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

from __future__ import annotations
import shutil
import tempfile
import os
from abc import ABC, abstractmethod
from appium.webdriver.webdriver import WebDriver as MobileRemote
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.ie.service import Service as IeService
from selenium.webdriver.ie.webdriver import WebDriver as Ie
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.safari.webdriver import WebDriver as Safari
from webdriver_manager.chrome import ChromeDriverManager as ChromeManager
from webdriver_manager.core.driver_cache import DriverCacheManager as DriverCache
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.firefox import GeckoDriverManager as GeckoManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeManager
from webdriver_manager.microsoft import IEDriverManager as IeManager
from webdriver_manager.opera import OperaDriverManager as OperaManager

from ..config import common_config as config
from ..config import local_config
from ..config import saucelabs_config
from .browsers import Browser
from .operating_system import OperatingSystem, SaucelabsOperatingSystem


class DriverFactory(ABC):

    """
    Abstract parent factory for all driver factories.
    """

    @staticmethod
    def create_driver_factory(spec_name: str) -> DriverFactory:
        if config.get_platform().is_remote():
            return SaucelabsDriverFactory(spec_name)
        elif config.get_platform().is_local():
            return LocalDriverFactory()
        else:
            raise RuntimeError("Given driver options are not supported")

    @abstractmethod
    def create_driver(self) -> Remote:
        pass

    def _create_browser_options(self, browser: Browser) -> ArgOptions:
        return {
            Browser.CHROME: ChromeOptions,
            Browser.EDGE: EdgeOptions,
            Browser.FIREFOX: FirefoxOptions,
            Browser.INTERNET_EXPLORER: IeOptions,
            Browser.OPERA: ChromeOptions,
            Browser.SAFARI: SafariOptions,
        }[browser]()


class LocalDriverFactory(DriverFactory):

    """
    This factory creates drivers for a browser which is installed on the machine of the user.
    """

    def create_driver(self) -> Remote:
        """Creates and returns a driver for local environment."""
        if config.get_operating_system().is_desktop():
            return self._create_desktop_driver()
        elif config.get_operating_system().is_mobile():
            return self._create_mobile_driver()
        else:
            raise RuntimeError(f"Operating system {config.get_operating_system()} is not supported")

    def _create_desktop_driver(self) -> Remote:
        browser = config.get_browser()
        operating_system = config.get_operating_system()
        assert browser.is_supported(operating_system), f"Browser {browser} not supported by {operating_system}."
        browser_options = self._create_options()
        if config.is_selenium4_driver_manager():
            executable_path = None
        else:
            cache = DriverCache(valid_range=config.get_driver_cache_days())
            manager: DriverManager = {
                Browser.CHROME: lambda: ChromeManager(cache_manager=cache),
                Browser.EDGE: lambda: EdgeManager(cache_manager=cache),
                Browser.FIREFOX: lambda: GeckoManager(cache_manager=cache),
                Browser.INTERNET_EXPLORER: lambda: IeManager(cache_manager=cache),
                Browser.OPERA: lambda: OperaManager(cache_manager=cache),
                Browser.SAFARI: lambda: None
            }[browser]()
            if manager is not None:
                driver_path=manager.install()
                executable_path = driver_path
                if config.is_driver_binary_copy():
                    driver_name = os.path.basename(f"{driver_path}_")
                    tmp_file = tempfile.NamedTemporaryFile(prefix=driver_name) # auto-deletes after program exit
                    executable_path = tmp_file.name
                    shutil.copy(driver_path, executable_path)
        service = {
            Browser.CHROME: lambda: ChromeService(executable_path=executable_path),
            Browser.EDGE: lambda: EdgeService(executable_path=executable_path),
            Browser.FIREFOX: lambda: FirefoxService(executable_path=executable_path, log_output=self._firefox_log_path()),
            Browser.INTERNET_EXPLORER: lambda: IeService(executable_path=executable_path),
            Browser.OPERA: lambda: ChromeService(executable_path=executable_path),
            Browser.SAFARI: lambda: SafariService() # Driver executable for Mac/Safari comes pre-installed
        }[browser]()
        driver: Remote = None
        driver = {
            Browser.CHROME: lambda: Chrome(service=service, options=browser_options),
            Browser.EDGE: lambda: Edge(service=service, options=browser_options),
            Browser.FIREFOX: lambda: Firefox(service=service, options=browser_options),
            Browser.INTERNET_EXPLORER: lambda: Ie(service=service, options=browser_options),
            Browser.OPERA: lambda: Chrome(service=service, options=browser_options),
            Browser.SAFARI: lambda: Safari(service=service, options=browser_options)
        }[browser]()
        driver.implicitly_wait(config.get_implicit_timeout())
        driver.set_page_load_timeout(config.get_page_load_timeout())
        return driver

    def _create_mobile_driver(self) -> MobileRemote:
        operating_system = config.get_operating_system()
        browser = config.get_browser()
        assert browser.is_supported(operating_system), f"Browser {browser} not supported by {operating_system}."
        capabilities = {
            OperatingSystem.IOS: self._create_ios_capabilities,
            OperatingSystem.ANDROID: self._create_android_capabilities,
        }[operating_system]()
        driver = MobileRemote(local_config.get_mobile_appium_server_url(), desired_capabilities=capabilities)
        driver.implicitly_wait(config.get_implicit_timeout())
        driver.set_page_load_timeout(config.get_page_load_timeout())
        return driver

    def _create_options(self) -> ArgOptions:
        browser = config.get_browser()
        options: ArgOptions = None
        if browser == Browser.CHROME:
            options = self._create_chrome_options()
        elif browser == Browser.FIREFOX:
            options = self._create_firefox_options()
        elif browser == Browser.OPERA:
            options = self._create_chrome_options()
            # following is needed for Opera to run
            options.add_experimental_option('w3c', True)
        else:
            options = self._create_browser_options(browser)
        for arg in config.get_custom_args():
            options.add_argument(arg)
        return options

    def _create_firefox_options(self) -> FirefoxOptions:
        options = FirefoxOptions()
        if config.is_headless():
            options.add_argument('-headless')
        return options

    def _create_chrome_options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--disable-extensions')
        if config.is_headless():
            # to run chrome headless in a docker container without any GUI environment
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
        return options

    def _firefox_log_path(self) -> str:
        project_root = os.environ.get("GAUGE_PROJECT_ROOT")
        return os.path.join(project_root, "logs", "geckodriver.log")

    def _create_android_capabilities(self) -> dict:
        desired_capabilities = {
            "deviceName": local_config.get_mobile_device_name(),
            "platformName": OperatingSystem.ANDROID.value,
            "platformVersion": config.get_operating_system_version(),
            "browserName": config.get_browser().value,
            "nativeWebScreenshot": "true",
            "chromeOptions": {
                "w3c": True,
                "extensions": []
            }
        }
        if local_config.get_mobile_real_device():
            # a real device needs a UDID instead of a name
            desired_capabilities["udid"] = local_config.get_mobile_device_udid()
        custom_args = config.get_custom_args()
        if custom_args:
            # see https://sites.google.com/a/chromium.org/chromedriver/capabilities#TOC-ChromeOptions-object
            # TODO: needs rewriting with browser's specific options classes.
            desired_capabilities['chromeOptions']['args'] = custom_args
        return desired_capabilities

    def _create_ios_capabilities(self) -> dict:
        desired_capabilities = {
            "automationName": "XCUITest",
            "deviceName": local_config.get_mobile_device_name(),
            "platformName": OperatingSystem.IOS.value,
            "platformVersion": config.get_operating_system_version(),
            "browserName": Browser.SAFARI.value
        }
        custom_args = config.get_custom_args()
        if custom_args:
            # not sure, if this works with safari. Documentation is scarce
            # TODO: needs rewriting and consolidation with android's browser capabilities.
            desired_capabilities['safariOptions'] = {}
            desired_capabilities['safariOptions']['args'] = custom_args
        return desired_capabilities


class RemoteDriverFactory(DriverFactory):

    """
    This factory creates remote drivers for browsers. It is not bound to any specific proved of an environment.
    """

    def create_driver(self) -> Remote:
        options = self._create_options()
        return Remote(command_executor=local_config.get_mobile_appium_server_url(), options=options)

    def _create_options(self) -> ArgOptions:
        browser = config.get_browser()
        headless = config.is_headless()
        options = self._create_browser_options(browser)
        if browser == Browser.CHROME or browser == Browser.OPERA:
            options.add_argument('--no-sandbox')
            options.add_argument('--hide-scrollbars')
            options.add_argument('--disable-extensions')
            if headless:
                # to run chrome headless in a docker container without any GUI environment
                options.add_argument('--headless')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--start-maximized')
            if browser == Browser.OPERA:
                options.add_experimental_option('w3c', True)
        elif browser == Browser.EDGE and headless:
            options.add_argument('--headless')
        elif browser == Browser.FIREFOX and headless:
            options.add_argument('-headless')
        return options


class SaucelabsDriverFactory(DriverFactory):
    """
    This factory creates drivers for the remote Saucelabs environment.
    """

    def __init__(self, spec_name: str) -> None:
        self.spec_name = spec_name

    def create_driver(self) -> Remote:
        """Creates and returns a driver for https://saucelabs.com/"""
        operating_system = config.get_operating_system()
        if operating_system.is_desktop():
            return self._create_desktop_driver()
        elif operating_system.is_mobile():
            return self._create_mobile_driver()
        else:
            raise RuntimeError(f"Operating system {operating_system} is not supported")

    def _create_desktop_driver(self) -> Remote:
        operating_system = config.get_operating_system()
        browser = config.get_browser()
        assert browser.is_supported(operating_system), f"Browser {browser} not supported by {operating_system}."
        browser_options = self._create_browser_options(browser)
        browser_options.platform_name = self._get_platform_name(operating_system, config.get_operating_system_version())
        if operating_system.is_desktop():
            browser_options.browser_version = saucelabs_config.get_browser_version()
        sauce_options = self._get_sauce_options()
        browser_options.set_capability("sauce:options", sauce_options)
        for arg in config.get_custom_args():
            browser_options.add_argument(arg)
        driver = Remote(saucelabs_config.get_executor(), options=browser_options)
        driver.implicitly_wait(config.get_implicit_timeout())
        driver.set_page_load_timeout(config.get_page_load_timeout())
        return driver

    def _create_mobile_driver(self) -> MobileRemote:
        operating_system = config.get_operating_system()
        browser = config.get_browser()
        desired_capabilities = {
            'platformName': operating_system.value,
            'browserName': browser.value,
            'appium:deviceName': saucelabs_config.get_device_name(),
            'appium:platformVersion': config.get_operating_system_version(),
            'tunnelIdentifier': saucelabs_config.get_tunnel_name(),
            'sauce:options': self._get_sauce_options()
        }
        if operating_system == OperatingSystem.ANDROID:
            desired_capabilities["chromeOptions"] = {
                'w3c': True,
                'extensions': []
            }
        elif operating_system == OperatingSystem.IOS:
            desired_capabilities["appium:automationName"] = "XCUITest"
        driver = MobileRemote(saucelabs_config.get_executor(), desired_capabilities)
        driver.implicitly_wait(config.get_implicit_timeout())
        driver.set_page_load_timeout(config.get_page_load_timeout())
        return driver

    def _get_platform_name(self, operating_system: OperatingSystem, operating_system_version: str) -> str:
        if operating_system == OperatingSystem.WINDOWS:
            return self._get_windows_platform_name(operating_system_version)
        elif operating_system == OperatingSystem.MACOS:
            return self._get_macos_platform_name(operating_system_version)
        else:
            raise RuntimeError(f"Cannot determine platform name for {operating_system}")

    def _get_windows_platform_name(self, operating_system_version: str) -> str:
        version = {
            "11": SaucelabsOperatingSystem.WINDOWS_11,
            "10": SaucelabsOperatingSystem.WINDOWS_10,
            "8.1": SaucelabsOperatingSystem.WINDOWS_8_1,
            "8": SaucelabsOperatingSystem.WINDOWS_8,
            "7": SaucelabsOperatingSystem.WINDOWS_7,
        }
        return version.get(operating_system_version, SaucelabsOperatingSystem.WINDOWS_DEFAULT).value

    def _get_macos_platform_name(self, operating_system_version: str) -> str:
        if operating_system_version is None:
            return SaucelabsOperatingSystem.MACOS_DEFAULT.value
        operating_system_version = operating_system_version.lower()
        versions = {
            "12": SaucelabsOperatingSystem.MACOS_12,
            "monterey": SaucelabsOperatingSystem.MACOS_12,
            "11": SaucelabsOperatingSystem.MACOS_11,
            "big sur": SaucelabsOperatingSystem.MACOS_11,
            "big_sur": SaucelabsOperatingSystem.MACOS_11,
            "big-sur": SaucelabsOperatingSystem.MACOS_11,
            "10.15": SaucelabsOperatingSystem.MACOS_10_15,
            "10": SaucelabsOperatingSystem.MACOS_10_15,
            "catalina": SaucelabsOperatingSystem.MACOS_10_15,
            "10.14": SaucelabsOperatingSystem.MACOS_10_14,
            "mojave": SaucelabsOperatingSystem.MACOS_10_14,
            "10.13": SaucelabsOperatingSystem.MACOS_10_13,
            "high sierra": SaucelabsOperatingSystem.MACOS_10_13,
            "high_sierra": SaucelabsOperatingSystem.MACOS_10_13,
            "high-sierra": SaucelabsOperatingSystem.MACOS_10_13,
            "10.12": SaucelabsOperatingSystem.MACOS_10_12,
            "sierra": SaucelabsOperatingSystem.MACOS_10_12,
            "10.11": SaucelabsOperatingSystem.MACOS_10_11,
            "el capitan": SaucelabsOperatingSystem.MACOS_10_11,
            "el_capitan": SaucelabsOperatingSystem.MACOS_10_11,
            "el-capitan": SaucelabsOperatingSystem.MACOS_10_11,
            "10.10": SaucelabsOperatingSystem.MACOS_10_10,
            "yosemite": SaucelabsOperatingSystem.MACOS_10_10,
        }
        return versions.get(operating_system_version, SaucelabsOperatingSystem.MACOS_DEFAULT).value

    def _get_sauce_options(self) -> dict:
        sauce_options = {}
        operating_system = config.get_operating_system()
        appium_version = saucelabs_config.get_appium_version()
        if operating_system and operating_system.is_mobile() and appium_version:
            sauce_options["appiumVersion"] = appium_version
        tunnel_name = saucelabs_config.get_tunnel_name()
        if tunnel_name:
            sauce_options["tunnelIdentifier"] = tunnel_name
        custom_test_title = saucelabs_config.get_test_title()
        spec_name = self.spec_name
        sauce_options["name"] = f"{spec_name} - {custom_test_title}" if custom_test_title else spec_name
        build = saucelabs_config.get_build()
        if build:
            sauce_options["build"] = build
        return sauce_options
