from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger
import time
import os

def setup_chromium():
    options = ChromiumOptions()
    options.set_paths('/usr/bin/google-chrome')
    arguments = [
        "--no-first-run",
        "--force-color-profile=srgb",
        "--metrics-recording-only",
        "--password-store=basic",
        "--use-mock-keychain",
        "--export-tagged-pdf",
        "--no-default-browser-check",
        "--disable-background-mode",
        "--enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
        "--disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
        "--deny-permission-prompts",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-web-security",
        "--disable-save-password-bubble",
        "--disable-infobars",
        "--test-type"
    ]
    for argument in arguments:
        options.set_argument(argument)
    return ChromiumPage(options)

def login(driver, email, password):
    driver.get('https://account.microsoft.com/billing/redeem')
    time.sleep(1)
    driver.ele("xpath:/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]").input(email)
    time.sleep(1)
    driver.ele("xpath:/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div[2]/input").click()
    time.sleep(1)
    driver.ele("xpath:/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/form/div[3]/div/div/input").input(password)
    time.sleep(1)
    driver.ele("xpath:/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/form/div[5]/div/div/div/div/button").click()
    time.sleep(1)
    driver.ele("xpath:/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/form/div[3]/div[2]/div/div[2]/button").click()
    time.sleep(3)
    logger.success(f"Successfully logged in ({email}).")
    logger.debug("Waiting 60 seconds...")
    time.sleep(60)

def redeem_code(driver, code):
    driver.get("https://account.microsoft.com/billing/redeem?refd=account.microsoft.com")
    logger.debug(f"Trying gift card {code}...")
    driver.ele("xpath:/html/body/main/div/div/div/div/div[1]/input").input(code)
    time.sleep(2)
    error_message = driver.ele("xpath:/html/body/main/div/div/div/div/div[1]/div[2]/p")
    if not error_message:
        redeem_button = driver.ele("xpath:/html/body/main/div/div/div/div/div[2]/button[2]")
        if redeem_button:
            redeem_button.click()
            time.sleep(5)
            result_text = driver.ele("xpath:/html/body/main/div/div/div/div/div[1]/div[2]/h3")
            if result_text:
                try:
                    value_of_gift_card = result_text.text.split("TRY ")[1].split(" ")[0].split(".")[0]
                except IndexError:
                    value_of_gift_card = result_text.text.split("₺")[1].split(" ")[0].split(",")[0]
                logger.success(f"Gift card test successful. [{code}] ({value_of_gift_card}TL)")
                with open(f"{value_of_gift_card}TL.txt", "a") as f:
                    f.write(f"{code}\n")
                return True
    else:
        logger.error(f"Gift card redemption failed. ({code})")
    return False

def load_accounts():
    with open("accounts.txt", "r") as f:
        return [line.strip().split(":") for line in f]

def load_codes():
    with open("codes.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

def save_progress(account_index, code_index):
    with open("progress.txt", "w") as f:
        f.write(f"{account_index},{code_index}")

def load_progress():
    if os.path.exists("progress.txt"):
        with open("progress.txt", "r") as f:
            account_index, code_index = map(int, f.read().split(","))
        return account_index, code_index
    return 0, 0

if __name__ == '__main__':
    driver = setup_chromium()
    driver.clear_cache()
    accounts = load_accounts()
    codes = load_codes()
    account_index, code_index = load_progress()
    while account_index < len(accounts) and code_index < len(codes):
        email, password = accounts[account_index]
        login(driver, email, password)
        for _ in range(20):
            if code_index >= len(codes):
                break
            if redeem_code(driver, codes[code_index]):
                time.sleep(5)
            code_index += 1
            save_progress(account_index, code_index)
        account_index += 1
        save_progress(account_index, code_index)
        driver.clear_cache()
    driver.quit()
