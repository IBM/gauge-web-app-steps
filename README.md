# gauge-web-app-steps

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENCE)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-31012/)
[![Selenium](https://img.shields.io/badge/-Selenium-blue?logo=selenium&logoColor=white)](https://github.com/SeleniumHQ)
[![Appium](https://img.shields.io/badge/-Appium-blue)](https://github.com/appium)
[![Gauge](https://img.shields.io/badge/Framework-Gauge-blue)](https://github.com/getgauge)
[![SauceLabs](https://img.shields.io/badge/Cloud-SauceLabs-blue)](https://saucelabs.com)

A Python module, that provides re-usable steps for testing web applications with the [Gauge](https://gauge.org/) framework.

## Description

This is an extensible and flexible test-automation library for [Gauge](https://gauge.org). It enables users with and without programming knowledge to create end-to-end test scenarios in [Markdown](https://www.markdownguide.org/) syntax. Developers can still easily extend their test scenarios with custom code. Selenium and Appium are used to simulate user interaction with the browser. A wide range of platforms and browsers are supported. Tests can also be executed on devices and emulators in the [SauceLabs](https://saucelabs.com) cloud.

## Gauge Step Overview

Find the documentation on all Gauge steps of this project in the overview:

[Gauge Step Overview](./docs/STEPS.md)

## Quick Start

This is a library for the Gauge framework, so Gauge+Python must be installed first.

* Install Python >= 3.10 on your platform and make it available in the \$PATH
* Install [Gauge](https://docs.gauge.org/getting_started/installing-gauge.html?language=python&ide=vscode) and [create a test project with Python](https://docs.gauge.org/getting_started/create-test-project.html?os=macos&language=python&ide=vscode)

It is useful to understand the basic workings of Gauge first. The [documentation](https://docs.gauge.org/?os=macos&language=python&ide=vscode) is excellent.

* Install [this module](#installation)
* Find out the path to this module after installation:
  ```shell
  echo $( python -m site --user-site )/gauge_web_app_steps
  ```
* Add that path to the property `STEP_IMPL_DIR` inside the test project file `env/default/python.properties`. Paths to multiple modules are comma separated.\
  Example on a Mac:
  ```
  STEP_IMPL_DIR = /Users/<user>/Library/Python/3.10/lib/python/site-packages/gauge_web_app_steps, step_impl
  ```
* Reload Visual Studio Code
* Write a new scenario in `specs/example.spec`. VSC offers **auto-completion**

## Installation

This module can be installed from source:

```shell
cd path/to/gauge-web-app-steps
pip install --user .
```

Or the latest package can be downloaded and installed from [PyPi](https://pypi.org/project/gauge-web-app-steps/):

```shell
pip install gauge-web-app-steps --user --upgrade
```

## Development

When coding on this project, unit tests can be executed like this:

```shell

TEST_SKIP_IT=1 python -m unittest discover -v -s tests/ -p 'test_*.py'
```

[Contributions are welcome](./docs/CONTRIBUTING.md).

## Troubleshooting

Some known inter-operability issues can be found on the [troubleshooting](./docs/TROUBLESHOOTING.md) page. If things don't work immediately, a solution might already be documented there.

## Configuration

The Configuration follows the [Gauge configuration](https://docs.gauge.org/configuration.html?os=linux&language=python&ide=vscode) approach.
A lot of behaviour, including the browsers and devices to use for the tests, can be determined with properties.

[Configuration Overview](./docs/CONFIG.md)

## Placeholders and Mathematical Expressions

Step parameters allow the use of placeholders, that can be defined in the Gauge environment properties files. Some steps also allow to set a placeholder value manually. Property keys act as placeholders, they are defined like "\${key}" and they will be replaced by its value if such a property key/value pair exists in any _env/\*/\*.properties_ file or within the execution scope.

Mathematical expressions can also be evaluated. For example: "#{5 + 5 * 5}" will be evaluated as "30".

It is possible to combine the two features. Placeholder substitution takes place before mathematical expression evaluation. Note that the first starts with a \$dollar sign, and the second with a \#hash sign.

Examples:

> \* Open "\${homepage_url}/home"

> \* Assert "id" = "sum" equals "#{5 + 6}"

> \* Assert "id" = "sum" equals "#{$addend + 5 * 5}"

The property "homepage_url" can be defined in _env/default/test.properties_ like this:

> homepage_url = https://my-app.net

It is also possible to define a property in a step:

\* Save placeholder "addend" = "5"

## Maintainers

[Maintainers](./docs/MAINTAINERS.md)
