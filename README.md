# SeleBrute & PlayBrute

`SeleBrute` (Selenium) and `PlayBrute` (Playwright) are WebDriver-based tools designed for brute-forcing and password spraying form-based web authentication.

### Overview

Traditional command-line tools like Hydra and Medusa excel in many authentication scenarios but often struggle with modern web applications that rely on dynamic, session-based tokens.

SeleBrute and PlayBrute address this challenge by simulating real user interactions within a full browser instance. This approach automatically handles any dynamic elements the page requires, such as JavaScript-generated values or CSRF tokens, ensuring each login attempt is valid.

### The Trade-Off

This browser-based approach involves a significant trade-off in speed. In headless "fast mode," the tools achieve an average rate of only about **2 password attempts per second**.

> Still looking for that free lunch.

![selebrute](https://github.com/user-attachments/assets/7ff0632a-22d3-4d35-94b1-7bb7b3d77727)

### Key Features

- **Two Flavors:** Choose between Selenium (`SeleBrute.py`) or Playwright (`PlayBrute.py`).
- **Two Attack Modes:**
    - **Brute Force:** One username, many passwords.
    - **Password Spray:** Many usernames, one password.
- **User Simulation:** An optional `--simulate-user` flag enables stealthy, human-like behavior to evade basic bot detection. This includes:
    - Dynamic, realistic user agents on each run.
    - Human-like typing speed.
    - Randomised delays and mouse movements.
- **Flexible Targeting:** Specify form fields and buttons using ID, Name, or XPath locators.
- **Headless Support:** Run silently in the background for cleaner execution.

---

### Setup 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fake-useragent
pip install selenium
pip install playwright
playwright install
```

**For Selenium:** Download the appropriate WebDriver for your browser and either place it in your PATH or specify its location with the `--driver-path` argument.
    - [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)
    - [GeckoDriver (Firefox)](https://github.com/mozilla/geckodriver/releases)

---

### Usage

Both scripts share the same command-line interface (see [CommandUsage](https://github.com/tpazz/SeleBrute/blob/main/CommandUsage.md) for full list).

#### **Brute Force (Fast Mode)**

```bash
python3 PlayBrute.py \
  --browser "chromium" \
  --url "https://example.com/login" \
  --username "admin" \
  --passwords-file "/path/to/passwords.txt" \
  --username-locator-strategy "id" \
  --username-locator-value "user-id" \
  --password-locator-strategy "id" \
  --password-locator-value "pass-id" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button[@type='submit']" \
  --headless
```
#### **Password Spray (User Simulation Mode)**

```bash
python3 SeleBrute.py \
  --driver-path "/path/to/geckodriver" \
  --browser "firefox" \
  --url "https://example.com/login" \
  --usernames-file "/path/to/users.txt" \
  --password "Spring2024!" \
  --username-locator-strategy "name" \
  --username-locator-value "username" \
  --password-locator-strategy "name" \
  --password-locator-value "password" \
  --loginbutton-locator-strategy "id" \
  --loginbutton-locator-value "login-btn" \
  --simulate-user \
  --headless
```  

---

### Command-Line Arguments

| Argument                      | Description                                                               |
| ----------------------------- | ------------------------------------------------------------------------- |
| **Attack Mode**               |                                                                           |
| `--url`                       | **Required.** URL of the login page.                                      |
| `--username`                  | [Brute Force] A single username to attack.                                |
| `--passwords-file`            | [Brute Force] Path to the password list.                                  |
| `--usernames-file`            | [Password Spray] Path to the username list.                               |
| `--password`                  | [Password Spray] A single password to spray.                              |
| **General Options**           |                                                                           |
| `--browser`                   | Browser to use. `chrome`/`firefox` (Sele) or `chromium`/`firefox`/`webkit` (Play). |
| `--driver-path`               | [Selenium Only] Path to the `chromedriver` or `geckodriver` executable.   |
| `--max-attempts`              | Maximum number of login attempts before stopping.                         |
| `--headless`                  | Run the browser in headless mode (no GUI).                                |
| `--simulate-user`             | Enables slower, human-like interaction to evade bot detection.            |
| **Locators**                  |                                                                           |
| `--username-locator-strategy` | `id`, `name`, `xpath`, or `css` (Playwright) for the username field.        |
| `--username-locator-value`    | The value of the locator (e.g., "user-id", "//input").                  |
| `--password-locator-strategy` | Locator strategy for the password field.                                  |
| `--password-locator-value`    | The value of the password field locator.                                  |
| `--loginbutton-locator-strategy`| Locator strategy for the login button.                                    |
| `--loginbutton-locator-value` | The value of the login button locator.                                    |

### Ethical Disclaimer

These tools are intended for legitimate security testing and research on systems for which you have **explicit, written permission** to test. Unauthorised use of this software to access systems you do not own is illegal and unethical. The authors are not responsible for misuse or damage caused by this software.
