from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time


def login(driver: WebDriver, url, id_selector, pw_selector, btn_selector, account, text):
    print(f"{text} 파트너센터 로그인 중..", end=' ', flush=True)
    _id, _pw = account.values()
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, id_selector).send_keys(_id)
    driver.find_element(By.CSS_SELECTOR, pw_selector).send_keys(_pw)
    driver.find_element(By.CSS_SELECTOR, btn_selector).click()
    time.sleep(0.5)
    print("[완료]")
