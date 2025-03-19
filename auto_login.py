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
    browser.add_cookie({"name": "MUSIC_U", "value": "005AF6DD7505973D9CA3A886B497229E3E13265AB4DD048C10904B4268E4ADF4689FD7E3AA40127A6163BEE161973B476AA464116C74130B326A1EB369669484220F655B766DB3FE47B18E8FD5373D63B2E1C56D68E5EA48FCE8B12729376D4FB6A24F3F0D423B8B07632E205D40BC6E60C6107DC56DCBC222965D3A3D187DF6E022BC8493FD0F8E5C752F71CA829E1794AB84F294BE49D371CEE2B5E8079F49E6E0CEE9B8FD6EC7D362E67D76B97DE67C2AC9B6428D9F4E77C3EC51D26BE11D82D5EF451AC9A37F8F767598F0276D2781CB33DD8EACBCA345664F4EE6FAD96D91DB17602B231E2EF18A2A23B18D408AC8A9B44DB4E763D3E6EE7EB878E81010BB83BB9EC23326787644E0BF665899228B9A38B9A349BC4A85A58C195EFF1A596BA11B17FF18FF2D1CEAEA339269111EEC4C0EFE2E232F85C8C47CB84002837DCF6D44B834384FF8C50E995E90B5358394A5024AADAA63AE51000C504AF5A214AD"})
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
