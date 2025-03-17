import os
import platform
import json
import sys
from colorama import Fore, Style
from enum import Enum
from typing import Optional

from exit_cursor import ExitCursor
import go_cursor_help
import patch_cursor_get_machine_id
from reset_machine import MachineIDResetter
from language import language, get_translation

os.environ["PYTHONVERBOSE"] = "0"
os.environ["PYINSTALLER_VERBOSE"] = "0"

import time
import random
from cursor_auth_manager import CursorAuthManager
import os
from logger import logging
from browser_utils import BrowserManager
from get_email_code import EmailVerificationHandler
from logo import print_logo
from config import Config
from datetime import datetime

# Define EMOJI dictionary
EMOJI = {"ERROR": get_translation("error"), "WARNING": get_translation("warning"), "INFO": get_translation("info")}


class VerificationStatus(Enum):
    """Verification status enum"""

    PASSWORD_PAGE = "@name=password"
    CAPTCHA_PAGE = "@data-index=0"
    ACCOUNT_SETTINGS = "Account Settings"


class TurnstileError(Exception):
    """Turnstile verification related exception"""

    pass


def save_screenshot(tab, stage: str, timestamp: bool = True) -> None:
    """
    Save a screenshot of the page

    Args:
        tab: Browser tab object
        stage: Stage identifier for the screenshot
        timestamp: Whether to add a timestamp
    """
    try:
        # Create screenshots directory
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # Generate filename
        if timestamp:
            filename = f"turnstile_{stage}_{int(time.time())}.png"
        else:
            filename = f"turnstile_{stage}.png"

        filepath = os.path.join(screenshot_dir, filename)

        # Save screenshot
        tab.get_screenshot(filepath)
        logging.debug(f"Screenshot saved: {filepath}")
    except Exception as e:
        logging.warning(f"Failed to save screenshot: {str(e)}")


def check_verification_success(tab) -> Optional[VerificationStatus]:
    """
    Check if verification was successful

    Returns:
        VerificationStatus: The corresponding status if successful, None if failed
    """
    for status in VerificationStatus:
        if tab.ele(status.value):
            logging.info(get_translation("verification_success", status=status.name))
            return status
    return None


def handle_turnstile(tab, max_retries: int = 2, retry_interval: tuple = (1, 2)) -> bool:
    """
    Handle Turnstile verification

    Args:
        tab: Browser tab object
        max_retries: Maximum number of retries
        retry_interval: Retry interval range (min, max)

    Returns:
        bool: Whether verification was successful

    Raises:
        TurnstileError: Exception during verification process
    """
    logging.info(get_translation("detecting_turnstile"))
    save_screenshot(tab, "start")

    retry_count = 0

    try:
        while retry_count < max_retries:
            retry_count += 1
            logging.debug(get_translation("retry_verification", count=retry_count))

            try:
                # Locate verification frame element
                challenge_check = (
                    tab.ele("@id=cf-turnstile", timeout=2)
                    .child()
                    .shadow_root.ele("tag:iframe")
                    .ele("tag:body")
                    .sr("tag:input")
                )

                if challenge_check:
                    logging.info(get_translation("detected_turnstile"))
                    # Random delay before clicking verification
                    time.sleep(random.uniform(1, 3))
                    challenge_check.click()
                    time.sleep(2)

                    # Save screenshot after verification
                    save_screenshot(tab, "clicked")

                    # Check verification result
                    if check_verification_success(tab):
                        logging.info(get_translation("turnstile_verification_passed"))
                        save_screenshot(tab, "success")
                        return True

            except Exception as e:
                logging.debug(f"Current attempt unsuccessful: {str(e)}")

            # Check if already verified
            if check_verification_success(tab):
                return True

            # Random delay before next attempt
            time.sleep(random.uniform(*retry_interval))

        # Exceeded maximum retries
        logging.error(get_translation("verification_failed_max_retries", max_retries=max_retries))
        logging.error(
            "Please visit the open source project for more information: https://github.com/chengazhen/cursor-auto-free"
        )
        save_screenshot(tab, "failed")
        return False

    except Exception as e:
        error_msg = get_translation("turnstile_exception", error=str(e))
        logging.error(error_msg)
        save_screenshot(tab, "error")
        raise TurnstileError(error_msg)


def get_cursor_session_token(tab, max_attempts=3, retry_interval=2):
    """
    Get Cursor session token with retry mechanism
    :param tab: Browser tab
    :param max_attempts: Maximum number of attempts
    :param retry_interval: Retry interval (seconds)
    :return: Session token or None
    """
    logging.info(get_translation("getting_cookie"))
    attempts = 0

    while attempts < max_attempts:
        try:
            cookies = tab.cookies()
            for cookie in cookies:
                if cookie.get("name") == "WorkosCursorSessionToken":
                    return cookie["value"].split("%3A%3A")[1]

            attempts += 1
            if attempts < max_attempts:
                logging.warning(
                    get_translation("cookie_attempt_failed", attempts=attempts, retry_interval=retry_interval)
                )
                time.sleep(retry_interval)
            else:
                logging.error(
                    get_translation("cookie_max_attempts", max_attempts=max_attempts)
                )

        except Exception as e:
            logging.error(get_translation("cookie_failure", error=str(e)))
            attempts += 1
            if attempts < max_attempts:
                logging.info(get_translation("retry_in_seconds", seconds=retry_interval))
                time.sleep(retry_interval)

    return None


def update_cursor_auth(email=None, access_token=None, refresh_token=None):
    """
    Update Cursor authentication information
    """
    auth_manager = CursorAuthManager()
    return auth_manager.update_auth(email, access_token, refresh_token)


def sign_up_account(browser, tab):
    logging.info(get_translation("start_account_registration"))
    logging.info(get_translation("visiting_registration_page", url=sign_up_url))
    tab.get(sign_up_url)

    try:
        if tab.ele("@name=first_name"):
            logging.info(get_translation("filling_personal_info"))
            tab.actions.click("@name=first_name").input(first_name)
            logging.info(get_translation("input_first_name", name=first_name))
            time.sleep(random.uniform(1, 3))

            tab.actions.click("@name=last_name").input(last_name)
            logging.info(get_translation("input_last_name", name=last_name))
            time.sleep(random.uniform(1, 3))

            tab.actions.click("@name=email").input(account)
            logging.info(get_translation("input_email", email=account))
            time.sleep(random.uniform(1, 3))

            logging.info(get_translation("submitting_personal_info"))
            tab.actions.click("@type=submit")

    except Exception as e:
        logging.error(get_translation("registration_page_access_failed", error=str(e)))
        return False

    handle_turnstile(tab)

    try:
        if tab.ele("@name=password"):
            logging.info(get_translation("setting_password"))
            tab.ele("@name=password").input(password)
            time.sleep(random.uniform(1, 3))

            logging.info(get_translation("submitting_password"))
            tab.ele("@type=submit").click()
            logging.info(get_translation("password_setup_complete"))

    except Exception as e:
        logging.error(get_translation("password_setup_failed", error=str(e)))
        return False

    if tab.ele("This email is not available."):
        logging.error(get_translation("registration_failed_email_used"))
        return False

    handle_turnstile(tab)

    while True:
        try:
            if tab.ele("Account Settings"):
                logging.info(get_translation("registration_success"))
                break
            if tab.ele("@data-index=0"):
                logging.info(get_translation("getting_email_verification"))
                code = email_handler.get_verification_code()
                if not code:
                    logging.error(get_translation("verification_code_failure"))
                    return False

                logging.info(get_translation("verification_code_success", code=code))
                logging.info(get_translation("inputting_verification_code"))
                i = 0
                for digit in code:
                    tab.ele(f"@data-index={i}").input(digit)
                    time.sleep(random.uniform(0.1, 0.3))
                    i += 1
                logging.info(get_translation("verification_code_input_complete"))
                break
        except Exception as e:
            logging.error(get_translation("verification_code_process_error", error=str(e)))

    handle_turnstile(tab)
    wait_time = random.randint(3, 6)
    for i in range(wait_time):
        logging.info(get_translation("waiting_system_processing", seconds=wait_time-i))
        time.sleep(1)

    logging.info(get_translation("getting_account_info"))
    tab.get(settings_url)
    try:
        usage_selector = (
            "css:div.col-span-2 > div > div > div > div > "
            "div:nth-child(1) > div.flex.items-center.justify-between.gap-2 > "
            "span.font-mono.text-sm\\/\\[0\\.875rem\\]"
        )
        usage_ele = tab.ele(usage_selector)
        if usage_ele:
            usage_info = usage_ele.text
            total_usage = usage_info.split("/")[-1].strip()
            logging.info(get_translation("account_usage_limit", limit=total_usage))
            logging.info(
                "Please visit the open source project for more information: https://github.com/chengazhen/cursor-auto-free"
            )
    except Exception as e:
        logging.error(get_translation("account_usage_info_failure", error=str(e)))

    logging.info(get_translation("registration_complete"))
    account_info = get_translation("cursor_account_info", email=account, password=password)
    logging.info(account_info)
    time.sleep(5)
    return True


class EmailGenerator:
    def __init__(
        self,
        password="".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*",
                k=12,
            )
        ),
    ):
        configInstance = Config()
        configInstance.print_config()
        self.domain = configInstance.get_domain()
        self.names = self.load_names()
        self.default_password = password
        self.default_first_name = self.generate_random_name()
        self.default_last_name = self.generate_random_name()

    def load_names(self):
        try:
            with open("names-dataset.txt", "r") as file:
                return file.read().split()
        except FileNotFoundError:
            logging.warning(get_translation("names_file_not_found"))
            # Fallback to a small set of default names if the file is not found
            return ["John", "Jane", "Alex", "Emma", "Michael", "Olivia", "William", "Sophia", 
                    "James", "Isabella", "Robert", "Mia", "David", "Charlotte", "Joseph", "Amelia"]

    def generate_random_name(self):
        """Generate a random username"""
        return random.choice(self.names)

    def generate_email(self, length=4):
        """Generate a random email address"""
        length = random.randint(0, length)  # Generate a random int between 0 and length
        timestamp = str(int(time.time()))[-length:]  # Use the last length digits of timestamp
        return f"{self.default_first_name}{timestamp}@{self.domain}"

    def get_account_info(self):
        """Get complete account information"""
        return {
            "email": self.generate_email(),
            "password": self.default_password,
            "first_name": self.default_first_name,
            "last_name": self.default_last_name,
        }


def get_user_agent():
    """Get user_agent"""
    try:
        # Use JavaScript to get user agent
        browser_manager = BrowserManager()
        browser = browser_manager.init_browser()
        user_agent = browser.latest_tab.run_js("return navigator.userAgent")
        browser_manager.quit()
        return user_agent
    except Exception as e:
        logging.error(f"Failed to get user agent: {str(e)}")
        return None


def check_cursor_version():
    """Check cursor version"""
    pkg_path, main_path = patch_cursor_get_machine_id.get_cursor_paths()
    with open(pkg_path, "r", encoding="utf-8") as f:
        version = json.load(f)["version"]
    return patch_cursor_get_machine_id.version_check(version, min_version="0.45.0")


def reset_machine_id(greater_than_0_45):
    if greater_than_0_45:
        # Prompt to manually execute script https://github.com/chengazhen/cursor-auto-free/blob/main/patch_cursor_get_machine_id.py
        go_cursor_help.go_cursor_help()
    else:
        MachineIDResetter().reset_machine_ids()


def print_end_message():
    logging.info("\n\n\n\n\n")
    logging.info("=" * 30)
    logging.info(get_translation("all_operations_completed"))
    logging.info("\n=== Get More Information ===")
    logging.info("📺 Bilibili UP: 想回家的前端")
    logging.info("🔥 WeChat Official Account: code 未来")
    logging.info("=" * 30)
    logging.info(
        "Please visit the open source project for more information: https://github.com/chengazhen/cursor-auto-free"
    )


if __name__ == "__main__":
    print_logo()
    
    # Add language selection
    print("\n")
    language.select_language_prompt()
    
    greater_than_0_45 = check_cursor_version()
    browser_manager = None
    try:
        logging.info(get_translation("initializing_program"))
        ExitCursor()

        # Prompt user to select operation mode
        print(get_translation("select_operation_mode"))
        print(get_translation("reset_machine_code_only"))
        print(get_translation("complete_registration"))

        while True:
            try:
                choice = int(input(get_translation("enter_option")).strip())
                if choice in [1, 2]:
                    break
                else:
                    print(get_translation("invalid_option"))
            except ValueError:
                print(get_translation("enter_valid_number"))

        if choice == 1:
            # Only reset machine code
            reset_machine_id(greater_than_0_45)
            logging.info(get_translation("machine_code_reset_complete"))
            print_end_message()
            sys.exit(0)

        logging.info(get_translation("initializing_browser"))

        # Get user_agent
        user_agent = get_user_agent()
        if not user_agent:
            logging.error(get_translation("get_user_agent_failed"))
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        # Remove "HeadlessChrome" from user_agent
        user_agent = user_agent.replace("HeadlessChrome", "Chrome")

        browser_manager = BrowserManager()
        browser = browser_manager.init_browser(user_agent)

        # Get and print browser's user-agent
        user_agent = browser.latest_tab.run_js("return navigator.userAgent")

        logging.info(
            "Please visit the open source project for more information: https://github.com/chengazhen/cursor-auto-free"
        )
        logging.info(get_translation("configuration_info"))
        login_url = "https://authenticator.cursor.sh"
        sign_up_url = "https://authenticator.cursor.sh/sign-up"
        settings_url = "https://www.cursor.com/settings"
        mail_url = "https://tempmail.plus"

        logging.info(get_translation("generating_random_account"))

        email_generator = EmailGenerator()
        first_name = email_generator.default_first_name
        last_name = email_generator.default_last_name
        account = email_generator.generate_email()
        password = email_generator.default_password

        logging.info(get_translation("generated_email_account", email=account))

        logging.info(get_translation("initializing_email_verification"))
        email_handler = EmailVerificationHandler(account)

        auto_update_cursor_auth = True

        tab = browser.latest_tab

        tab.run_js("try { turnstile.reset() } catch(e) { }")

        logging.info(get_translation("starting_registration"))
        logging.info(get_translation("visiting_login_page", url=login_url))
        tab.get(login_url)

        if sign_up_account(browser, tab):
            logging.info(get_translation("getting_session_token"))
            token = get_cursor_session_token(tab)
            if token:
                logging.info(get_translation("updating_auth_info"))
                update_cursor_auth(
                    email=account, access_token=token, refresh_token=token
                )
                logging.info(
                    "Please visit the open source project for more information: https://github.com/chengazhen/cursor-auto-free"
                )
                logging.info(get_translation("resetting_machine_code"))
                reset_machine_id(greater_than_0_45)
                logging.info(get_translation("all_operations_completed"))
                print_end_message()
            else:
                logging.error(get_translation("session_token_failed"))

    except Exception as e:
        logging.error(get_translation("program_error", error=str(e)))
    finally:
        if browser_manager:
            browser_manager.quit()
        input(get_translation("program_exit_message"))
