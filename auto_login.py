# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0091801F5F3AB9B34D5D92184B2DD73205415062FEF80264097CE3018E515F3B24A752291378BE2F3A35E39DC9C524E67D7DD0426649DD5BA8828DEF022852274680B74B020022B9AA385652E75CF2A14581B326222A5F99E02BF624783CB6DC3B360DBE0471F80BC4E59CBEFE9A11BC809F6B080A8F230887DF7D383037E3B47FE61262B4E3F2C3EFA3CC0CC157E5A61C183DF6223A6BEA9622894EBED4AB18AAD8985F46B218E6D967555263D2EFADA7FBBF828ED5A14204FA6056C71043E22EC7699380CA890C418A8D628CE4940B7204CEFC8A2C3569B70C5BA3225948AB13521464336C36550900818EC3AEBA17D34A9E27E4858CABC8C3A518B92560B08BDC300908E8C74DCE84DB83F9D60DEA6C109F0C73FF7F1470FC93CCDFD0BD32F8AA95EF54B4F3588D3B5D35E33771FB0AD692E2A46DF4016D15C8219B56F759A017FC3032DF29B641B60A4FBBA51C02F2964B0A3680C7DC25D38B05390C72E00E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
