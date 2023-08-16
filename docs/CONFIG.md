# Configuration

The Configuration follows the [Gauge configuration](https://docs.gauge.org/configuration.html?os=linux&language=python&ide=vscode) approach.
The following properties are supported:

## Categories

  - [General](#general)
  - [Appium](#appium)
  - [Saucelabs](#saucelabs)
  - [Deprecated](#deprecated)

## General

| Property | Type | Default | Description |
|--|--|--|--|
| `driver_cache_days` | int | 365 | number of days, before the driver manager will invalidate the cache and make a renewal request. |
| `debug_log` | boolean | `false`| Logs more information. |
| `diff_formats` | `gradient` \| `full` \| `color:xyz` | `full` | For screenshot comparisons. `xyz`: any CSS3 color name. |
| `screenshot_whole_page_no_scroll` | boolean | `false` | Firefox offers to take a screenshot of the whole page, even if the page is wider and higher than the current viewport. This is not standard behaviour. |
| `time_pattern` | string | `%Y-%m-%d_%H-%M-%S` | Supported date format codes can be taken from the [Python docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). |
| `filename_pattern` | string | `%{browser}_%{name}.%{ext}` | Screenshot files will be named according to this pattern. Available placeholders are `%{browser}`, `%{name}`, `%{ext}`, `%{time}`. `%{time}` is defined by the property `%{time_pattern}`. |
| `screenshot_dir` | string | `screenshots` | Determines the directory, in which screenshots should be saved. |
| `actual_screenshot_dir` | string | `actual_screenshots` | Determines the directory, in which the screenshots of the current test run should be stored, which will be compared to expected screenshots. |
| `expected_screenshot_dir` | string | `expected_screenshots` | Determines the directory, in which the expected screenshots will be found, which are the source for comparisons. |
| `failure_screenshot_dir` | string | `reports/html-report/images` | Determines the directory, in which screenshots will be stored, that are taken when an error happens. |
| `driver_browser` | `chrome` \| `firefox` \| `safari` \| `edge` \| `internet explorer` \| `opera` | `firefox` | The browser, in which tests should run. |
| `driver_implicit_timeout` | int | `5` | Seconds to wait for any web elements to appear, disappear, or transform into an expected state. |
| `driver_operating_system` | `win` \| `macos` \| `linux` \| `android` \| `ios` | `macos` | Determines on which OS the tests should run. |
| `driver_operating_system_version` | string | `None` \| `Windows 11` \| `macOS 13` | Some drivers need the OS version, but it is not needed for local tests. |
| `driver_page_load_timeout` | int | `30` | Timeout in seconds to wait until a web page has been loaded. |
| `driver_platform` | `local` \| `saucelabs` | `local` | Whether the driver should connect to a remote device cloud provider. At the moment, [SauceLabs](https://saucelabs.com/) is the only supported service provider. |
| `driver_platform_local_headless`| boolean | `false` | When `driver_platform` = `local`, then tests can be run in headless mode. |
| `driver_custom_args` | string | `None` | Optional custom arguments, that are appended to the browser options, f.i. `incognito` for chrome browsers. Multiple arguments can be comma-separated. |

## Appium

The following properties define a connection to an [Appium server](https://appium.io/docs/en/2.0/).
With Appium, mobile browsers can be used for testing.

| Property | Type | Default | Description |
|--|--|--|--|
| `driver_platform_local_mobile_appium_server_url` | string | `None` | This is the URL of the appium command executor. For local tests, this typically is `http://127.0.0.1:4444/wd/hub`. |
| `driver_platform_local_mobile_device_name` | string | `None` | The device name of the Appium test device. |
| `driver_platform_local_mobile_device_udid` | string | `None` | The UID of the Appium test device. |
| `driver_platform_local_mobile_real_device` | boolean | `false` | Whether the test device is a simulator or a real device. |

## Saucelabs

The following properties define a connection to the [SauceLabs](https://saucelabs.com/) device cloud provider.

| Property | Type | Default | Description |
|--|--|--|--|
| `driver_platform_saucelabs_mobile_appium_version` | string | `None` | When not specified, a default will be picked by SauceLabs. |
| `driver_platform_saucelabs_desktop_browser_version` | string | `latest` | The release version of the chosen browser. |
| `driver_platform_saucelabs_mobile_device_name` | string | `None` | The name of the test device. Regular expressions are supported: `Samsung.*`, `iPhone [6-7]`. The [Platform Configurator](https://app.saucelabs.com/platform-configurator) can be used to pick a device. |
| `driver_platform_saucelabs_executor` | string | `None` | The executor URL of SauceLabs. This URL can be found in the [Platform Configurator](https://app.saucelabs.com/platform-configurator). |
| `driver_platform_saucelabs_tunnel_name` | string | `None` | If the SauceConnect tunnel is used, the name can be placed here. The Name can be found on the SauceLabs [Tunnel Proxies](https://app.saucelabs.com/tunnels) page. |
| `driver_platform_saucelabs_test_title` | string | `None` | Test runs can be given a title, so they can be found more easily in the [Test Results](https://app.saucelabs.com/dashboard/tests) or [Builds](https://app.saucelabs.com/dashboard/builds/vdc). |
| `driver_platform_saucelabs_build` | string | `None` | Test runs can be given a build ID, so they can be found more easily in the [Test Results](https://app.saucelabs.com/dashboard/tests) or [Builds](https://app.saucelabs.com/dashboard/builds/vdc). |

The following properties should be set as system variables, rather than Gauge properties:

| Property | Type | Default | Description |
|--|--|--|--|
| `SAUCE_STATUS_ADDRESS` | string | `None` | The standard address of the SauceConnect tunnel API, when run locally is `127.0.0.1:8080`, without `http://`. |
| `SAUCE_TUNNEL_ACTIVE` | boolean | `false` | Whether the SauceConnect tunnel should be started before test execution. |
| `SAUCE_TUNNEL_POOLING` | boolean | `false` | Parallel executions will need the SauceConnect tunnel to run in pool mode. |
| `SAUCE_HOST` | `macos` \| `windows` \| `linux` | `None` | The OS type, from which the Gauge test has been started. This property should be auto-discovered in a future release. |
| `SAUCE_PATH` | string | `sc` | Path to the sauce connector binary. |
| `SAUCE_USERNAME` | string | `None` | SauceLabs user name |
| `SAUCE_ACCESS_KEY` | string | `None` | SauceLabs access key. It can be found in the user settings. |
| `SAUCE_REGION` | string | `None` | Possible regions as of now: `eu-central`, `us-west` |
| `SAUCE_DNS` | string | `None` | DNS of the VPN connection (seems necessary on Windows hosts). This will be passed to the `--dns` [parameter](https://docs.saucelabs.com/dev/cli/sauce-connect-proxy/#--dns) of the tunnel command. |
| `SAUCE_NO_SSL_BUMP_DOMAINS` | string | `None` | This will be passed to the `--no-ssl-bump-domains` [parameter](https://docs.saucelabs.com/dev/cli/sauce-connect-proxy/#--no-ssl-bump-domains) of the tunnel command. Can be: `all` \| any domains. This property is needed for some real devices. |
| `SAUCE_LOG_FILE` | string | `$GAUGE_PROJECT_ROOT/logs/sc.log` | The log file path of the tunnel output. |

## Deprecated

* `driver_headless`: use `driver_platform_local_headless` instead
