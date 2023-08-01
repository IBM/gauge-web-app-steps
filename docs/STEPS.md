# Gauge Steps

An overview of how to write Gauge specifications can be found [here](https://docs.gauge.org/writing-specifications.html?os=macos&language=python&ide=vscode).\
The following Gauge steps are implemented in this module:

## Overview

  - [Wait \<secs>](#wait-secs)
  - [Fullscreen](#fullscreen)
  - [Maximize](#maximize)
  - [Window size \<width>x\<height>](#window-size-widthxheight)
  - [Close current window](#close-current-window)
  - [Close other windows](#close-other-windows)
  - [Refresh](#refresh)
  - [Back](#back)
  - [Forward](#forward)
  - [Open \<page>](#open-page)
  - [Open \<page> for \<user>: \<password>](#open-page-for-user-password)
  - [Register authentication \<user>: \<password> for \<regexp>](#register-authentication-user-password-for-regexp)
  - [Remove authentication for \<regexp>](#remove-authentication-for-regexp)
  - [Print window handles](#print-window-handles)
  - [Switch to window \<window_param>](#switch-to-window-window_param)
  - [Switch to default content](#switch-to-default-content)
  - [Switch to frame \<frame_param>](#switch-to-frame-frame_param)
  - [Switch to frame \<by> = \<by_value>](#switch-to-frame-by--by_value)
  - [Dismiss alert](#dismiss-alert)
  - [Accept alert](#accept-alert)
  - [Take a screenshot](#take-a-screenshot)
  - [Take a screenshot of \<by> = \<by_value> \<file>](#take-a-screenshot-of-by--by_value-file)
  - [Take screenshots of whole page \<file>](#take-screenshots-of-whole-page-file)
  - [Click \<by> = \<by_value>](#click-by--by_value)
  - [Click \<by> = \<by_value> \<key_down>](#click-by--by_value-key_down)
  - [Check \<by> = \<by_value>](#check-by--by_value)
  - [Uncheck \<by> = \<by_value>](#uncheck-by--by_value)
  - [Select \<by> = \<by_value> option \<select_key> = \<select_value>](#select-by--by_value-option-select_key--select_value)
  - [Double click \<by> = \<by_value>](#double-click-by--by_value)
  - [Type \<string>](#type-string)
  - [Type \<key_down> \<string>](#type-key_down-string)
  - [Type \<by> = \<by_value> \<string>](#type-by--by_value-string)
  - [Type \<by> = \<by_value> \<key_down> \<string>](#type-by--by_value-key_down-string)
  - [Send keys \<keys>](#send-keys-keys)
  - [Send keys \<key_down> \<keys>](#send-keys-key_down-keys)
  - [Send \<by> = \<by_value> keys \<keys>](#send-by--by_value-keys-keys)
  - [Send \<by> = \<by_value> keys \<key_down> \<keys>](#send-by--by_value-keys-key_down-keys)
  - [Clear \<by> = \<by_value>](#clear-by--by_value)
  - [Mouse down \<by> = \<by_value>](#mouse-down-by--by_value)
  - [Mouse up \<by> = \<by_value>](#mouse-up-by--by_value)
  - [Move to \<by> = \<by_value>](#move-to-by--by_value)
  - [Move to and center \<by> = \<by_value>](#move-to-and-center-by--by_value)
  - [Move out](#move-out)
  - [Hover over \<by> = \<by_value>](#hover-over-by--by_value)
  - [Show message in an error case \<error_message>](#show-message-in-an-error-case-error_message)
  - [Scroll \<by> = \<by_value> into view](#scroll-by--by_value-into-view)
  - [Drag and drop \<by_source> = \<by\_value_source> into \<by_dest> = \<by\_value_dest>](#drag-and-drop-by_source--by_value_source-into-by_dest--by_value_dest)
  - [Upload file = \<file\_path> into \<by> = \<by_value>](#upload-file--file_path-into-by--by_value)
  - [Execute \<script>](#execute-script)
  - [Execute \<script> and save result in \<placeholder>](#execute-script-and-save-result-in-placeholder)
  - [Execute \<script> with \<by> = \<by_value> as \<elem>](#execute-script-with-by--by_value-as-elem)
  - [Execute \<script> with \<by> = \<by_value> as \<elem> and save result in \<placeholder>](#execute-script-with-by--by_value-as-elem-and-save-result-in-placeholder)
  - [Execute async \<script>](#execute-async-script)
  - [Execute async \<script> and save result in \<placeholder> with callback \<callback>](#execute-async-script-and-save-result-in-placeholder-with-callback-callback)
  - [Execute async \<script> with \<by> = \<by_value> as \<elem>](#execute-async-script-with-by--by_value-as-elem)
  - [Execute async \<script> with \<by> = \<by_value> as \<elem> and save result in \<placeholder> with callback \<callback>](#execute-async-script-with-by--by_value-as-elem-and-save-result-in-placeholder-with-callback-callback)
  - [Save placeholder \<placeholder> = \<value>](#save-placeholder-placeholder--value)
  - [Save placeholder \<placeholder> from \<by> = \<by_value>](#save-placeholder-placeholder-from-by--by_value)
  - [Save placeholder \<placeholder> from attribute \<attribute> of \<by> = \<by_value>](#save-placeholder-placeholder-from-attribute-attribute-of-by--by_value)
  - [Assert window handles is \<windows_num>](#assert-window-handles-is-windows_num)
  - [Assert title equals \<url>](#assert-title-equals-url)
  - [Assert dialog text equals \<url>](#assert-dialog-text-equals-url)
  - [Assert url equals \<url>](#assert-url-equals-url)
  - [Assert url starts with \<url>](#assert-url-starts-with-url)
  - [Assert url ends with \<url>](#assert-url-ends-with-url)
  - [Assert url contains \<url>](#assert-url-contains-url)
  - [Assert \<by> = \<by_value> exists](#assert-by--by_value-exists)
  - [Assert \<by> = \<by_value> is invisible](#assert-by--by_value-is-invisible)
  - [Assert \<by> = \<by_value> is enabled](#assert-by--by_value-is-enabled)
  - [Assert \<by> = \<by_value> is disabled](#assert-by--by_value-is-disabled)
  - [Assert \<by> = \<by_value> is selected](#assert-by--by_value-is-selected)
  - [Assert \<by> = \<by_value> has selected value \<value>](#assert-by--by_value-has-selected-value-value)
  - [Assert \<by> = \<by_value> is not selected](#assert-by--by_value-is-not-selected)
  - [Assert \<by> = \<by_value> equals \<string>](#assert-by--by_value-equals-string)
  - [Assert \<by> = \<by_value> does not equal \<string>](#assert-by--by_value-does-not-equal-string)
  - [Assert \<by> = \<by_value> regexp \<regexp>](#assert-by--by_value-regexp-regexp)
  - [Assert \<by> = \<by_value> contains \<string>](#assert-by--by_value-contains-string)
  - [Assert \<by> = \<by_value> does not contain \<string>](#assert-by--by_value-does-not-contain-string)
  - [Assert \<by> = \<by_value> css \<css_property_name> is \<css_expected_value>](#assert-by--by_value-css-css_property_name-is-css_expected_value)
  - [Assert \<by> = \<by_value> is focused](#assert-by--by_value-is-focused)
  - [Assert \<by> = \<by_value> attribute \<attribute> exists](#assert-by--by_value-attribute-attribute-exists)
  - [Assert \<by> = \<by_value> attribute \<attribute> contains \<value>](#assert-by--by_value-attribute-attribute-contains-value)
  - [Assert \<by> = \<by_value> attribute \<attribute> equals \<value>](#assert-by--by_value-attribute-attribute-equals-value)
  - [Assert \<by> = \<by_value> attribute \<attribute> does not contain \<value>](#assert-by--by_value-attribute-attribute-does-not-contain-value)
  - [Assert \<by> = \<by_value> screenshot resembles \<file> with SSIM more than \<threshold>](#assert-by--by_value-screenshot-resembles-file-with-ssim-more-than-threshold)
  - [Assert page screenshots resemble \<file> with SSIM more than \<threshold>](#assert-page-screenshots-resemble-file-with-ssim-more-than-threshold)
  - [Assert page screenshots resemble \<file> with SSIM more than \<threshold> for \<pages>](#assert-page-screenshots-resemble-file-with-ssim-more-than-threshold-for-pages)
  - [Fail \<message>](#fail-message)


## Wait \<secs>

> \* Wait "2"

> \* Wait "0.3"

> \* Wait "\${secs}"

Waits for the specified time in seconds. This can be used for debugging purposes. It should not be necessary very often in final tests, because there is an implicit wait time set for Selenium. See the [configuration properties](./CONFIG.md).

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |


## Fullscreen

> \* Fullscreen

Go fullscreen with the currently open test browser window.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Maximize

> \* Maximize

Maximize the currently open test browser window.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Window size \<width>x\<height>

> \* Window size "800"x"600"

> \* Window size "\${width}"x"\${height}"

Sets the page size of the currently open test browser window to the specified dimensions.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Close current window

> \* Close current window

Closes the currently open window and switches to the last opened window.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Close other windows

> \* Close other windows

Closes all other windows but the current one.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Refresh

>\* Refresh

Refresh the currently open page, as if you click the ↻ "refresh" button.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Back

> \* Back

Navigate back one page in the browsing history, as if you click the ← "back" button.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Forward

>\* Forward

Navigate forward one page in the browsing history, as if you click the → "forward" button.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Open \<page>

> \* Open "https://my-app.net/"

> \* Open "\${homepage_url}"

Opens the specified url. Make sure to specify the whole URL including, f.i., any _https://_ prefix.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Open \<page> for \<user>: \<password>

> \* Open "https://my-app.net/" for "mike": "passw@rd1"

> \* Open "\${homepage_url}" for "\${user}": "\${password}"

**ATTENTION - this step will write the credentials into the final URL. This might pose a security risk!**\
**Use placeholders and a credentials manager, so that credentials are not stored as plain text in your project.**\
Opens the specified url with the specified credentials in HTTP Basic Authentication mode. Make sure to specify the whole URL including, f.i., any _https://_ prefix.
You do not need to worry about url encoding of special password characters, the step will handle that.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ?        |     ?      |

## Register authentication \<user>: \<password> for \<regexp>

> \* Register authentication "\${user}": "\${password} for "https://.*\\.herokuapp\\.com/basic_auth"

Open pages, that match the given `regexp` in the same specification with the given credentials.
That means that subsequent steps like `* Open "https://the-internet.herokuapp.com/basic_auth"` will use those credentials automatically. This functionality is not yet supported by all browsers and might fail when the driver tries to open the page.
**Use placeholders and a credentials manager, so that credentials are not stored as plain text in your project.**

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|Chrome |       ?        |     x      |

## Remove authentication for \<regexp>

> \* Remove authentication for "https://.*\\.herokuapp\\.com/basic_auth"

If any credentials have been registered for the given URL regexp, then remove it. subsequent `Open` -steps will not use the credentials anymore.

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Print window handles

> \* Print window handles

Prints all window handles into the console and the report.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Switch to window \<window_param>

> \* Switch to window "Name"

> \* Switch to window "0"

Switch to the specified window handle. The parameter can either be the name of the window or the index. 
The latest opened window has the highest index. Index starts with 0.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Switch to default content

> \* Switch to default content

Switch the Selenium driver mode back (to the main frame of the page). Element selections in Selenium work per frame. If an element resides outside of the main page, you first have to switch there.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Switch to frame \<frame_param>

> \* Switch to frame "myIframeName"

> \* Switch to frame "0"

Switch to the specified frame/iFrame by "name"-tag or index. When using an index, the first frame in the DOM tree has the index 0, the second the index 1 and so on. Element selections in Selenium work per frame. If an element resides outside of the main page, you first have to switch there.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Switch to frame \<by> = \<by_value>

> \* Switch to frame "id" = "element-identifier"

> \* Switch to frame "xpath" = "//div/iframe"

> \* Switch to frame "name" = "frameName"

> \* Switch to frame "tag name" = "iframe"

> \* Switch to frame "class name" = "frameClass"

> \* Switch to frame "css selector" = "p>iframe.frameClass"

Switch to the specified iFrame by specified selector. Element selections in Selenium work per frame. If an element resides outside of the main page, you first have to switch there.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Dismiss alert

> \* Dismiss alert

Dismiss the alert of the current page.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |            |

## Accept alert

> \* Accept alert

Accept the alert of the current page.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |            |

## Take a screenshot

> \* Take a screenshot "my\_screenshot"

Takes a screenshot of the current screen and saves it into the directory defined in the property 'screenshot\_dir'. The filename of the image can be defined with a pattern in the property 'filename\_pattern'. If the filename shall contain the current time, then also set the property 'time\_pattern'.
See the tests.properties file in your gauge project.

### ___filename\_pattern___ property

available substitutes:
* **%{browser}** - the browser, with which the test is running
* **%{time}** - the current time, it will be formatted according to the 'time\_pattern' property
* **%{name}** - your custom name
* **%{ext}** - file extension. This is always 'png' for now. Do not forget the '.' before the extension.

### ___time\_pattern___ property

see http://strftime.org/ for possible formats

### Examples

> screenshot_dir = screenshots \
> time_pattern = %Y-%m-%d\_%H-%M-%S-%f \
> filename_pattern = %{browser}\_%{time}\_%{name}.%{ext}

Taken the example step with the example properties above, it would produce a file like this: **firefox\_2019-05-31\_15-13-50-265593\_my\_screenshot.png**

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Take a screenshot of \<by> = \<by_value> \<file>

> \* Take a screenshot of "id" = "element-identifier" "my\_screenshot\_of\_element"

> \* Take a screenshot of "xpath" = "//div/a" "my\_screenshot\_of\_element"

> \* Take a screenshot of "link text" = "Click this link" "my\_screenshot\_of\_element"

> \* Take a screenshot of "partial link text" = "Click this" "my\_screenshot\_of\_element"

> \* Take a screenshot of "name" = "nameAttributeName" "my\_screenshot\_of\_element"

> \* Take a screenshot of "tag name" = "a" "my\_screenshot\_of\_element"

> \* Take a screenshot of "class name" = "cssClassName" "my\_screenshot\_of\_element"

> \* Take a screenshot of "css selector" = "p>a.redlink" "my\_screenshot\_of\_element"

See the step above for a comprehensive explanation. The only difference here is, that the screenshot will not contain the whole current screen, but only the selected element.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Take screenshots of whole page \<file>

> \* Take screenshots of whole page "my\_screenshots"

Takes multiple screenshots of the page while scrolling down. Screenshots are postfixed starting from "\_1".
After every screenshot the page scrolls down by the height of the window.
See step "Take a screenshot" for a basic description of configurations around taking screenshots.

## Click \<by> = \<by_value>

> \* Click "id" = "element-identifier"

> \* Click "xpath" = "//div/a"

> \* Click "link text" = "Click this link"

> \* Click "partial link text" = "Click this"

> \* Click "name" = "nameAttributeName"

> \* Click "tag name" = "nameTagName"

> \* Click "class name" = "cssClassName"

> \* Click "css selector" = "p>a.redlink"

Click on the specified element of the open page. Choose one of the "By" selectors, that suits best in the situation.
See https://www.w3schools.com/xml/xpath_syntax.asp for a handy XPath reference.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Click \<by> = \<by_value> \<key_down>

> \* Click "link text" = "Click this link" "COMMAND"

> \* Click "link text" = "Click this link" "\${cmdOrCtr}"

Like the above Step, but during the click the specified key is held down. See "Send Keys \<keys>" step for available keys.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Check \<by> = \<by_value>

> \* Check "id" = "element-identifier"

> \* Check "xpath" = "//input[1]"

> \* Check "link text" = "Check this element"

> \* Check "partial link text" = "Check this"

> \* Check "name" = "nameAttributeName"

> \* Check "tag name" = "nameTagName"

> \* Check "class name" = "cssClassName"

> \* Check "css selector" = "p>a.redlink"

Check an element, if not yet checked.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Uncheck \<by> = \<by_value>

Opposite of the Check step with same selectors. It will remove the checked flag from an element which is selected.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Select \<by> = \<by_value> option \<select_key> = \<select_value>

> \* Select "id" = "element-identifier" option "id" = "1"

> \* Select "xpath" = "//element-identifier" option "value" = "Carrots"

> \* Select "tag name" = "element-identifier" option "visible text" = "Carrots"

Selects an option from a select element. The available selectors for \<by> are the same as for the Click step.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Double click \<by> = \<by_value>

> \* Double click "id" = "element-identifier"

> \* Double click "xpath" = "//div/a"

> \* Double click "link text" = "Click this link"

> \* Double click "partial link text" = "Click this"

> \* Double click "name" = "nameAttributeName"

> \* Double click "tag name" = "nameTagName"

> \* Double click "class name" = "cssClassName"

> \* Double click "css selector" = "p>a.redlink"

Double click on the specified element of the open page.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Type \<string>

> \* Type "amalfi lemon"

> \* Type "\${type}"

Types the specified text. No element is clicked on before. This can be used, f.i. if an input field should be pre-selected after you opened a page.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Type \<key_down> \<string>

> \* Type "SHIFT" "amalfi lemon"

> \* Type "\${shift}" "amalfi lemon"

Like the above step, but with the specified key held down during typing. See [Send Keys \<keys>](#send-keys-keys) for available keys.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Type \<by> = \<by_value> \<string>

> \* Type "id" = "search-field" "amalfi lemon"

> \* Type "id" = "search-field" "\${type}"

> \* Type "xpath" = "//input[@type='text']" "amalfi lemon"

> \* Type "link text" = "search link" "amalfi lemon"

> \* Type "partial link text" = "search" "amalfi lemon"

> \* Type "name" = "search-field-name" "amalfi lemon"

> \* Type "tag name" = "input" "amalfi lemon"

> \* Type "class name" = "search-class" "amalfi lemon"

> \* Type "css selector" = "input.searchclass" "amalfi lemon"

Type the specified text into the specified element. As for the "Click" step, multiple "By" selectors can be used.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Type \<by> = \<by_value> \<key_down> \<string>

> \* Type "id" = "search-field" "SHIFT" "amalfi lemon"

> \* Type "id" = "search-field" "\${shift}" "amalfi lemon"

Like the above step, but holds the specified key down during typing. See [Send keys \<keys>](#send-keys-keys) step for available keys.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Send keys \<keys>

> \* Send keys "SHIFT TAB"

Send keys, separate multiple keys by whitespace and/or comma.
Valid keys are: ['NULL', 'CANCEL', 'HELP', 'BACKSPACE', 'BACK_SPACE', 'TAB', 'CLEAR', 'RETURN', 'ENTER', 'SHIFT', 'LEFT_SHIFT', 'CONTROL', 'LEFT_CONTROL', 'ALT', 'LEFT_ALT', 'PAUSE', 'ESCAPE', 'SPACE', 'PAGE_UP', 'PAGE_DOWN', 'END', 'HOME', 'LEFT', 'ARROW_LEFT', 'UP', 'ARROW_UP', 'RIGHT', 'ARROW_RIGHT', 'DOWN', 'ARROW_DOWN', 'INSERT', 'DELETE', 'SEMICOLON', 'EQUALS', 'NUMPAD0', 'NUMPAD1', 'NUMPAD2', 'NUMPAD3', 'NUMPAD4', 'NUMPAD5', 'NUMPAD6', 'NUMPAD7', 'NUMPAD8', 'NUMPAD9', 'MULTIPLY', 'ADD', 'SEPARATOR', 'SUBTRACT', 'DECIMAL', 'DIVIDE', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'META', 'COMMAND']

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |            |

## Send keys \<key_down> \<keys>

> \* Send keys "SHIFT" "TAB"

> \* Send keys "\${shift}" "\${tab}"

Like the above step, but holds the specified key down during typing. See [Send Keys \<keys>](#send-keys-keys) step for available keys.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |


## Send \<by> = \<by_value> keys \<keys>

> \* Send "id" = "search-field" "amalfi lemon" keys "SHIFT TAB"

> \* Send "xpath" = "//input[@type='text']" "amalfi lemon" keys "SHIFT TAB"

> \* Send "link text" = "search link" "amalfi lemon" keys "SHIFT TAB"

> \* Send "partial link text" = "search" "amalfi lemon" keys "SHIFT TAB"

> \* Send "name" = "search-field-name" "amalfi lemon" keys "SHIFT TAB"

> \* Send "tag name" = "input" "amalfi lemon" keys "SHIFT TAB"

> \* Send "class name" = "search-class" "amalfi lemon" keys "SHIFT TAB"

> \* Send "css selector" = "input.searchclass" "amalfi lemon" keys "SHIFT TAB"

Send keys to the specified element. See [Send keys \<keys>](#send-keys-keys) for details.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |            |

## Send \<by> = \<by_value> keys \<key_down> \<keys>

> \* Send "id" = "search-field" "amalfi lemon" keys "SHIFT" "TAB"

> \* Send "id" = "search-field" "amalfi lemon" keys "\${shift}" "\${tab}"

Like the step above, but holds down the specified key during sending the other keys. See [Send keys \<keys>](#send-keys-keys) step for available keys.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Clear \<by> = \<by_value>

> \* Clear "id" = "search-field"

Clears any input text from the specified element.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Mouse down \<by> = \<by_value>

> \* Mouse down "id" = "search-field"

> \* Mouse down "xpath" = "//input[@type='text']"

> \* Mouse down "link text" = "search link"

> \* Mouse down "partial link text" = "search"

> \* Mouse down "name" = "search-field-name"

> \* Mouse down "tag name" = "input"

> \* Mouse down "class name" = "search-class"

> \* Mouse down "css selector" = "input.searchclass"

Mouse down on a selected element.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Mouse up \<by> = \<by_value>

> \* Mouse up "id" = "search-field"

> \* Mouse up "xpath" = "//input[@type='text']"

> \* Mouse up "link text" = "search link"

> \* Mouse up "partial link text" = "search"

> \* Mouse up "name" = "search-field-name"

> \* Mouse up "tag name" = "input"

> \* Mouse up "class name" = "search-class"

> \* Mouse up "css selector" = "input.searchclass"

Mouse up or release from a selected element.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Move to \<by> = \<by_value>

> \* Move to "id" = "search-field"

> \* Move to "xpath" = "//input[@type='text']"

> \* Move to "link text" = "search link"

> \* Move to "partial link text" = "search"

> \* Move to "name" = "search-field-name"

> \* Move to "tag name" = "input"

> \* Move to "class name" = "search-class"

> \* Move to "css selector" = "input.searchclass"

Scroll the specified element into view, and place the mouse coursor over it.
This can be helpful, when elements are not currently visible on the page.
Other steps like "Click" or "Type" would usually fail if the element is not visible on the page.
Some elements also need the mouse to hover over them to become fully visible, in which case this step can be used as well.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Move to and center \<by> = \<by_value>

> \* Move to and center "id" = "search-field"

> \* Move to and center "xpath" = "//input[@type='text']"

> \* Move to and center "link text" = "search link"

> \* Move to and center "partial link text" = "search"

> \* Move to and center "name" = "search-field-name"

> \* Move to and center "tag name" = "input"

> \* Move to and center "class name" = "search-class"

> \* Move to and center "css selector" = "input.searchclass"

It moves the element into the view like [Move to \<by> = \<by_value>](#move-to-by--by_value), but then also tries to center it vertically,
so that it is less likely, that header elements overlap the targeted element.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Move out

Opposite of the [Move to \<by> = \<by_value>](#move-to-by--by_value) step. It will move the cursor out of a focused element to the body of the page.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Hover over \<by> = \<by_value>

> \* Hover over "id" = "search-field"

> \* Hover over "xpath" = "//input[@type='text']"

> \* Hover over "link text" = "search link"

> \* Hover over "partial link text" = "search"

> \* Hover over "name" = "search-field-name"

> \* Hover over "tag name" = "input"

> \* Hover over "class name" = "search-class"

> \* Hover over "css selector" = "input.searchclass"

Hover over the specified element.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ?        |     ?      |

## Show message in an error case \<error_message>

> \* Show message in an error case "Error in test case xyz"

In case of a failed assert use the predefined error message, instead of the default.

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Scroll \<by> = \<by_value> into view

> \* Scroll "id" = "lemon" into view

> \* Scroll "xpath" = "//div/p" into view

> \* Scroll "link text" = "click me" into view

> \* Scroll "partial link text" = "click" into view

> \* Scroll "name" = "amalfi" into view

> \* Scroll "tag name" = "p" into view

> \* Scroll "class name" = "lemon" into view

> \* Scroll "css selector" = "div>p" into view

Scroll an element into the viewport.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |

## Drag and drop \<by_source> = \<by\_value_source> into \<by_dest> = \<by\_value_dest>

> \* Drag and drop "id" = "source" into "id" = "dest"

> \* Drag and drop "xpath" = "//div[1]/div" into "xpath" = "//div[2]"

> \* Drag and drop "link text" = "source" into "link text" = "dest"

> \* Drag and drop "partial link text" = "source" into "partial link text" = "dest"

> \* Drag and drop "name" = "source" into "name" = "dest"

> \* Drag and drop "tag name" = "p" into "tag name" = "div"

> \* Drag and drop "class name" = "source" into "class name" = "dest"

> \* Drag and drop "css selector" = "source" into "css selector" = "dest"

Drag and drop an element.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |

## Upload file = \<file\_path> into \<by> = \<by_value>

> \* Upload file = "path/to/filename" into "id" = "uploader"

> \* Upload file = "path/to/filename" into "xpath" = "//input[@type='file']"

> \* Upload file = "path/to/filename" into "name" = "uploader"

> \* Upload file = "path/to/filename" into "tag name" = "input"

> \* Upload file = "path/to/filename" into "class name" = "cssClassName"

> \* Upload file = "path/to/filename" into "css selector" = "div>input.uploader"

Upload a file over a form.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |

## Execute \<script>

> \* Execute "document.body.style.backgroundColor = 'yellow'"

Execute a snippet of self written JavaScript.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Execute \<script> and save result in \<placeholder>

> \* Execute "return 1 + 2;" and save result in "result"

Execute a snippet of self written JavaScript.
The result of the execution will be saved in a placeholder and can be used in later steps.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Execute \<script> with \<by> = \<by_value> as \<elem>

> \* Execute script "mybutton.click()" with "id" = "button" as "mybutton"

> \* Execute script "mybutton.click()" with "xpath" = "//button" as "mybutton"

> \* Execute script "mybutton.click()" with "link text" = "Click Me" as "mybutton"

> \* Execute script "mybutton.click()" with "partial link text" = "Click" as "mybutton"

> \* Execute script "mybutton.click()" with "name" = "button" as "mybutton"

> \* Execute script "mybutton.click()" with "tag name" = "button" as "mybutton"

> \* Execute script "mybutton.click()" with "class name" = "create-button" as "mybutton"

> \* Execute script "mybutton.click()" with "css selector" = "button.create-button" as "mybutton"

Execute a snippet of self written JavaScript on a defined element.
The element will be given the provided name, so it can be used in the JavaScript with that variable name.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Execute \<script> with \<by> = \<by_value> as \<elem> and save result in \<placeholder>

> \* Execute script "return numberelem.innerText + ${addend}" with "id" = "nummy" as "numberelem" and save result in "sum"

> \* Execute script "return numberelem.innerText + ${addend}" with "xpath" = "//[@id='nummy']" as "numberelem" and save result in "sum"

> \* Execute script "return numberelem.innerText + ${addend}" with "link text" = "5" as "numberelem" and save result in "sum"

> \* Execute script "return numberelem.innerText + ${addend}" with "partial link text" = "5" as "numberelem" and save result in "sum"

> \* Execute script "return numberelem.innerText + ${addend}" with "name" = "button" as "numberelem" and save result in "sum"

> \* Execute script "return numberelem.innerText + ${addend}" with "tag name" = "div" as "numberelem" and save result in "sum"

> \* Execute script "return numberelem.innerText + ${addend}" with "class name" = "nummy" as "numberelem" and save result in "sum"

> \* Execute script "return numberelem.innerText + ${addend}" with "css selector" = "div.nummy" as "numberelem" and save result in "sum"

Execute a snippet of self written JavaScript on a defined element.
The element will be given the provided name, so it can be used in the JavaScript with that variable name.
The result of the execution will be saved in a placeholder and can be used in later steps.


Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Execute async \<script>

> \* Execute async "setTimeout(function() {alert('tada');}, 100);"

Execute a snippet of self written JavaScript asynchronously.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Execute async \<script> and save result in \<placeholder> with callback \<callback>

> \* Execute async "var result = \`${placeholder}!`; setTimeout(function() {myCallback(result);}, 100);" and save result in "result" with callback "myCallback"

Execute a snippet of self written JavaScript asynchronously.
The result of the execution can be saved in a placeholder and can be used in later steps.
The script has to invoke a callback with a freely selectable name in order to return the result.


Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Execute async \<script> with \<by> = \<by_value> as \<elem>

> \* Execute async script "mybutton.click()" with "id" = "button" as "mybutton"

> \* Execute async script "mybutton.click()" with "xpath" = "//button" as "mybutton"

> \* Execute async script "mybutton.click()" with "link text" = "Click Me" as "mybutton"

> \* Execute async script "mybutton.click()" with "partial link text" = "Click" as "mybutton"

> \* Execute async script "mybutton.click()" with "name" = "button" as "mybutton"

> \* Execute async script "mybutton.click()" with "tag name" = "button" as "mybutton"

> \* Execute async script "mybutton.click()" with "class name" = "create-button" as "mybutton"

> \* Execute async script "mybutton.click()" with "css selector" = "button.create-button" as "mybutton"

Execute a snippet of self written JavaScript asynchronously on a defined element.
The element will be given the provided name, so it can be used in the JavaScript with that variable name.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Execute async \<script> with \<by> = \<by_value> as \<elem> and save result in \<placeholder> with callback \<callback>

> \* Execute async script "myCallback(myelement.innerText)" with "id" = "txtelem" as "myelement" and save result in "myplaceholder" with callback "myCallback"

> \* Execute async script "myCallback(myelement.innerText)" with "xpath" = "//div/p" as "myelement" and save result in "myplaceholder" with callback "myCallback"

> \* Execute async script "myCallback(myelement.innerText)" with "link text" = "Click Me" as "myelement" and save result in "myplaceholder" with callback "myCallback"

> \* Execute async script "myCallback(myelement.innerText)" with "partial link text" = "Click" as "myelement" and save result in "myplaceholder" with callback "myCallback"

> \* Execute async script "myCallback(myelement.innerText)" with "name" = "button" as "myelement" and save result in "myplaceholder" with callback "myCallback"

> \* Execute async script "myCallback(myelement.innerText)" with "tag name" = "p" as "myelement" and save result in "myplaceholder" with callback "myCallback"

> \* Execute async script "myCallback(myelement.innerText)" with "class name" = "txtelem" as "myelement" and save result in "myplaceholder" with callback "myCallback"

> \* Execute async script "myCallback(myelement.innerText)" with "css selector" = "p.txtelem" as "myelement" and save result in "myplaceholder" with callback "myCallback"

Execute a snippet of self written JavaScript asynchronously on a defined element.
The element will be given the provided name, so it can be used in the JavaScript with that variable name.
The result of the execution can be saved in a placeholder and can be used in later steps.
The script has to invoke a callback with a freely selectable name in order to return the result.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Save placeholder \<placeholder> = \<value>

> \* Save placeholder "class" = "greenFrame"

> \* Save placeholder "class" = \<value>

Saves the placeholder name/value pair into the scenario data store. This way, it can be used as a placeholder in later steps. This can be especially useful in combination with concepts (2nd example). See the [Gauge documentation on concepts](https://docs.gauge.org/writing-specifications.html?os=macos&language=python&ide=vscode#concept).

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |        ✔       |      ✔     |

## Save placeholder \<placeholder> from \<by> = \<by_value>

> \* Save placeholder "costs" from "id" = "costSlider"

> \* Save placeholder "costs" from "xpath" = "//input"

> \* Save placeholder "costs" from "link text" = "Click Me"

> \* Save placeholder "costs" from "partial link text" = "Click"

> \* Save placeholder "costs" from "name" = "costy"

> \* Save placeholder "costs" from "tag name" = "input"

> \* Save placeholder "costs" from "class name" = "costSlider"

> \* Save placeholder "costs" from "css selector" = "input.costSlider"

Saves the placeholder with the defined key into the scenario data store. The value of the placeholder is the text inside the specified element. This way, it can be used as a placeholder in later steps.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |        ✔       |      ✔     |

## Save placeholder \<placeholder> from attribute \<attribute> of \<by> = \<by_value>

> \* Save placeholder "costs" from attribute "value" of "id" = "costSlider"

> \* Save placeholder "costs" from attribute "value" of "xpath" = "//input"

> \* Save placeholder "costs" from attribute "value" of "link text" = "Click Me"

> \* Save placeholder "costs" from attribute "value" of "partial link text" = "Click"

> \* Save placeholder "costs" from attribute "value" of "name" = "costy"

> \* Save placeholder "costs" from attribute "value" of "tag name" = "input"

> \* Save placeholder "costs" from attribute "value" of "class name" = "costSlider"

> \* Save placeholder "costs" from attribute "value" of "css selector" = "input.costSlider"

Saves the placeholder with the defined key into the scenario data store. The value of the placeholder is the text of the specified element's attribute. This way, it can be used as a placeholder in later steps.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |        ✔       |      ✔     |

## Assert window handles is \<windows_num>

> \* Assert window handles is "2"

Assert, that the current number of window handles equals the specified parameter.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Assert title equals \<url>

> \* Assert title equals "The Internet"

> \* Assert title equals "\${title}"

Assert that the title of the web page equals exactly "The Internet".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert dialog text equals \<url>

> \* Assert dialog text equals "I am a dialog"

> \* Assert dialog text equals "\${text}"

Assert that the text of a Javascript dialog equals exactly "I am a dialog".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert url equals \<url>

> \* Assert url equals "http://localhost/home/"

> \* Assert url equals "\${homepage_url}"

Assert that the current url equals exactly "http://localhost/home/".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert url starts with \<url>

> \* Assert url starts with "http://localhost"

> \* Assert url starts with "\${homepage_url}"

Assert that the current url starts with the specified text.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert url ends with \<url>

> \* Assert url ends with "/some/path/"

> \* Assert url ends with "\${homepage_url}"

Assert that the current url ends with the specified text. This can be useful to assert a certain path regardless of the domain.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert url contains \<url>

> \* Assert url contains "/some/path"

> \* Assert url contains "\${homepage_url}"

Assert that the current url contains the specified text. The text can occur anywhere in the url, so it can be useful to check if a certain path segmant is present regardless of the domain, the preceding path, or parameters.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> exists

> \* Assert "id" = "elem-id" exists

> \* Assert "xpath" = "//div/a" exists

> \* Assert "link text" = "Click here" exists

> \* Assert "partial link text" = "Click" exists

> \* Assert "name" = "field-name" exists

> \* Assert "tag name" = "ul" exists

> \* Assert "class name" = "resultlist-class" exists

> \* Assert "css selector" = "ul.resultlist-class" exists

Assert that the specified element exists on screen.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ?        |     ?      |

## Assert \<by> = \<by_value> is invisible

> \* Assert "id" = "elem-id" is invisible

> \* Assert "xpath" = "//div/a" is visible

> \* Assert "link text" = "Click here" is invisible

> \* Assert "partial link text" = "Click" is invisible

> \* Assert "name" = "field-name" is invisible

> \* Assert "tag name" = "ul" is invisible

> \* Assert "class name" = "resultlist-class" is invisible

> \* Assert "css selector" = "ul.resultlist-class" is invisible

Assert that the specified element does not exist or is not displayed on screen.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ?        |     ?      |

## Assert \<by> = \<by_value> is enabled

> \* Assert "id" = "elem-id" is enabled

> \* Assert "xpath" = "//div/a" is enabled

> \* Assert "link text" = "Click here" is enabled

> \* Assert "partial link text" = "Click" is enabled

> \* Assert "name" = "field-name" is enabled

> \* Assert "tag name" = "ul" is enabled

> \* Assert "class name" = "resultlist-class" is enabled

> \* Assert "css selector" = "ul.resultlist-class" is enabled

Assert that the specified element is enabled. This is useful for input elements like buttons and text fields.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> is disabled

> \* Assert "id" = "elem-id" is disabled

> \* Assert "xpath" = "//div/a" is disabled

> \* Assert "link text" = "Click here" is disabled

> \* Assert "partial link text" = "Click" is disabled

> \* Assert "name" = "field-name" is disabled

> \* Assert "tag name" = "ul" is disabled

> \* Assert "class name" = "resultlist-class" is disabled

> \* Assert "css selector" = "ul.resultlist-class" is disabled

Assert that the specified element is disabled. This is useful for input elements like buttons and text fields.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> is selected

> \* Assert "id" = "elem-id" is selected

> \* Assert "xpath" = "//input[@type='checkbox']" is selected

> \* Assert "link text" = "Click here" is selected

> \* Assert "partial link text" = "Click" is selected

> \* Assert "name" = "field-name" is selected

> \* Assert "tag name" = "ul" is selected

> \* Assert "class name" = "resultlist-class" is selected

> \* Assert "css selector" = "ul.resultlist-class" is selected

Assert that the specified element is selected. This is useful for input elements like checkboxes or radio buttons.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> has selected value \<value>

> \* Assert "id" = "elem-id" has selected value "Carrots"

> \* Assert "xpath" = "//input[@type='checkbox']" has selected value "Carrots"

> \* Assert "link text" = "Click here" has selected value "Carrots"

> \* Assert "partial link text" = "Click" has selected value "Carrots"

> \* Assert "name" = "field-name" has selected value "Carrots"

> \* Assert "tag name" = "ul" has selected value "Carrots"

> \* Assert "class name" = "resultlist-class" has selected value "Carrots"

> \* Assert "css selector" = "ul.resultlist-class" has selected value "Carrots"

Assert that the specified select element has the value selected.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> is not selected

> \* Assert "id" = "elem-id" is not selected

> \* Assert "xpath" = "//input[@type='checkbox']" is not selected

> \* Assert "link text" = "Click here" is not selected

> \* Assert "partial link text" = "Click" is not selected

> \* Assert "name" = "field-name" is not selected

> \* Assert "tag name" = "ul" is not selected

> \* Assert "class name" = "resultlist-class" is not selected

> \* Assert "css selector" = "ul.resultlist-class" is not selected

Assert that the specified element is not selected. This is useful for input elements like checkboxes or radio buttons.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> equals \<string>

> \* Assert "id" = "elem-id" equals "Lorem Ipsum"

> \* Assert "id" = "elem-id" equals "\${text}"

> \* Assert "xpath" = "//div/a" equals "Lorem Ipsum"

> \* Assert "link text" = "Click here" equals "Lorem Ipsum"

> \* Assert "partial link text" = "Click" equals "Lorem Ipsum"

> \* Assert "name" = "field-name" equals "Lorem Ipsum"

> \* Assert "tag name" = "ul" equals "Lorem Ipsum"

> \* Assert "class name" = "resultlist-class" equals "Lorem Ipsum"

> \* Assert "css selector" = "ul.resultlist-class" equals "Lorem Ipsum"

Assert that the specified element has the exact text value "Lorem Ipsum".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> does not equal \<string>

Similar to the previous assert but checks that a string is not equal to a value.

## Assert \<by> = \<by_value> regexp \<regexp>

> \* Assert "id" = "elem-id" regexp "Lorem[\s]*Ipsum"

> \* Assert "xpath" = "//div/p" regexp "Lorem[\s]*Ipsum"

> \* Assert "link text" = "Click here" regexp "Lorem[\s]*Ipsum"

> \* Assert "partial link text" = "Click" regexp "Lorem[\s]*Ipsum"

> \* Assert "name" = "field-name" regexp "Lorem[\s]*Ipsum"

> \* Assert "tag name" = "ul" regexp "Lorem[\s]*Ipsum"

> \* Assert "class name" = "resultlist-class" regexp "Lorem[\s]*Ipsum"

> \* Assert "css selector" = "ul.resultlist-class" regexp "Lorem[\s]*Ipsum"

Assert that the specified element has a text value that matches the regular expression "Lorem[\s]*Ipsum".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> contains \<string>

> \* Assert "id" = "elem-id" contains "Ipsum"

> \* Assert "xpath" = "//div/p" contains "Ipsum"

> \* Assert "link text" = "Click here" contains "Ipsum"

> \* Assert "partial link text" = "Click" contains "Ipsum"

> \* Assert "name" = "field-name" contains "Ipsum"

> \* Assert "tag name" = "ul" contains "Ipsum"

> \* Assert "class name" = "resultlist-class" contains "Ipsum"

> \* Assert "css selector" = "ul.resultlist-class" contains "Ipsum"

Assert that the specified element contains the text value "Ipsum".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> does not contain \<string>

> \* Assert "id" = "elem-id" does not contain "Shmipsum"

> \* Assert "xpath" = "//div/p" does not contain "Shmipsum"

> \* Assert "link text" = "Click here" does not contain "Shmipsum"

> \* Assert "partial link text" = "Click" does not contain "Shmipsum"

> \* Assert "name" = "field-name" does not contain "Shmipsum"

> \* Assert "tag name" = "ul" does not contain "Shmipsum"

> \* Assert "class name" = "resultlist-class" does not contain "Shmipsum"

> \* Assert "css selector" = "ul.resultlist-class" does not contain "Shmipsum"

Assert that the specified element does not contain the text value "Shmipsum".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> css \<css_property_name> is \<css_expected_value>

> \* Assert "id" = "elem-id" css "width" is "800px"

> \* Assert "xpath" = "//div/a" css "width" is "800px"

> \* Assert "link text" = "Click here" css "width" is "800px"

> \* Assert "partial link text" = "Click" css "width" is "800px"

> \* Assert "name" = "field-name" css "width" is "800px"

> \* Assert "tag name" = "ul" css "width" is "800px"

> \* Assert "class name" = "resultlist-class" css "width" is "800px"

> \* Assert "css selector" = "ul.resultlist-class" css "width" is "800px"

Assert that the specified element has a CSS property with the specified value.\
ATTENTION: the browser might not return the same value, that is specified in the page source, e.g. for a key-value pair like "color: red" it might return a value like "rgb(255,0,0)"

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |

## Assert \<by> = \<by_value> is focused

> \* Assert "id" = "input-id" is focused

> \* Assert "xpath" = "//div/input" is focused

> \* Assert "link text" = "Click here" is focused

> \* Assert "partial link text" = "Click" is focused

> \* Assert "name" = "field-name" is focused

> \* Assert "tag name" = "ul" is focused

> \* Assert "class name" = "resultlist-class" is focused

> \* Assert "css selector" = "ul.resultlist-class" is focused

Assert that the specified element is focused. This is done by comparing the specified element with the element, that is returned by Selenium as currently active element: `driver.switch_to.active_element`.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |


## Assert \<by> = \<by_value> attribute \<attribute> exists

> \* Assert "id" = "input-id" attribute "checked" exists

> \* Assert "xpath" = "//div/input" attribute "checked" exists

> \* Assert "link text" = "Click here" attribute "checked" exists

> \* Assert "partial link text" = "Click" attribute "checked" exists

> \* Assert "name" = "field-name" attribute "checked" exists

> \* Assert "tag name" = "input" attribute "checked" exists

> \* Assert "class name" = "checkbox-class" attribute "checked" exists

> \* Assert "css selector" = "input[type=checkbox]" attribute "checked" exists

Assert that the specified element has an attribute with the given name.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |


## Assert \<by> = \<by_value> attribute \<attribute> contains \<value>

> \* Assert "id" = "input-id" attribute "href" contains "issues/59"

> \* Assert "xpath" = "//div/a" attribute "href" contains "issues/59"

> \* Assert "link text" = "Click here" attribute "href" contains "issues/59"

> \* Assert "partial link text" = "Click" attribute "href" contains "issues/59"

> \* Assert "name" = "field-name" attribute "href" contains "issues/59"

> \* Assert "tag name" = "a" attribute "href" contains "issues/59"

> \* Assert "class name" = "link-class" attribute "href" contains "issues/59"

> \* Assert "css selector" = "a.link-class" attribute "href" contains "issues/59"

Assert that the specified element has an attribute with the given name, that contains a certain value.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |


## Assert \<by> = \<by_value> attribute \<attribute> equals \<value>

> \* Assert "id" = "input-id" attribute "href" equals "../issues/59"

> \* Assert "xpath" = "//div/a" attribute "href" equals "../issues/59"

> \* Assert "link text" = "Click here" attribute "href" equals "../issues/59"

> \* Assert "partial link text" = "Click" attribute "href" equals "../issues/59"

> \* Assert "name" = "field-name" attribute "href" equals "../issues/59"

> \* Assert "tag name" = "a" attribute "href" equals "../issues/59"

> \* Assert "class name" = "link-class" attribute "href" equals "../issues/59"

> \* Assert "css selector" = "a.link-class" attribute "href" equals "../issues/59"

Assert that the specified element has an attribute with the given name, that equals a certain value.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |


## Assert \<by> = \<by_value> attribute \<attribute> does not contain \<value>

> \* Assert "id" = "input-id" attribute "href" does not contain "imnothere"

> \* Assert "xpath" = "//div/a" attribute "href" does not contain "imnothere"

> \* Assert "link text" = "Click here" attribute "href" does not contain "imnothere"

> \* Assert "partial link text" = "Click" attribute "href" does not contain "imnothere"

> \* Assert "name" = "field-name" attribute "href" does not contain "imnothere"

> \* Assert "tag name" = "a" attribute "href" does not contain "imnothere"

> \* Assert "class name" = "link-class" attribute "href" does not contain "imnothere"

> \* Assert "css selector" = "a.link-class" attribute "href" does not contain "imnothere"

Assert that the specified element either has no attribute with the given name, or it does not contain a certain value.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |      ?         |     ?      |


## Assert \<by> = \<by_value> screenshot resembles \<file> with SSIM more than \<threshold>

> \* Assert "id" = "elem-id" screenshot resembles "example.png" with SSIM more than "0.95"

> \* Assert "xpath" = "//div/img" screenshot resembles "example.png" with SSIM more than "0.95"

> \* Assert "link text" = "Click here" screenshot resembles "example.png" with SSIM more than "0.95"

> \* Assert "partial link text" = "Click" = "div" screenshot resembles "example.png" with SSIM more than "0.95"

> \* Assert "name" = "field-name" screenshot resembles "example.png" with SSIM more than "0.95"

> \* Assert "tag name" = "div" screenshot resembles "example.png" with SSIM more than "0.95"

> \* Assert "class name" = "resultlist-class" screenshot resembles "example.png" with SSIM more than "0.95"

> \* Assert "css selector" = "ul.resultlist-class" screenshot resembles "example.png" with SSIM more than "0.95"

Assert that the specified element looks like the specified image file.
The browser will take a screenshot of the element to compare the image against the reference.
Beware the environment variables `actual_screenshot_dir`, and `expected_screenshot_dir`, that are used for saving the images.
The computed SSIM must not be less than the specified threshold.
The SSIM value must be between 0.0 (no similarity) and 1.0 (same picture).
For a more comprehensive explanation of SSIM, see

* https://en.wikipedia.org/wiki/Structural_similarity
* https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |            |

## Assert page screenshots resemble \<file> with SSIM more than \<threshold>

> \* Assert page screenshots resemble "example.png" with SSIM more than "0.95"

Scrolls and takes screenshots of the whole page, while comparing them to existing files.\
In principle, this works just as the step above, but for the whole page and with multiple picture files, that are postfixed, starting from "_1".

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Assert page screenshots resemble \<file> with SSIM more than \<threshold> for \<pages>

> \* Assert page screenshots resemble "example.png" with SSIM more than "0.95" for "5" pages

Scrolls and takes screenshots for the specified number of times, while comparing them to existing files.
This works similar to the step above, but internally the PAGE\_DOWN key is pressed and no automatical break condition is used.
This step can be used for front-end frameworks which do not support scrolling by Javascript.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |                |            |

## Fail \<message>

> \* Fail "Please finish this scenario"

This step will always fail and leave the specified message in the report.
The intention is to provide an early exit, especially for scenarios, that are 'in progress'. Working this way ensures that a half done scenario will not be forgotten to be finished.

Support

|Desktop|Android (Chrome)|iOS (Safari)|
|:-----:|:--------------:|:----------:|
|   ✔   |       ✔        |     ✔      |
