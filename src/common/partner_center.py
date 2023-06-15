import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from util.color import Color


class PartnerCenter:
    def __init__(self, driver: WebDriver, res_list, start, end, account):
        self.driver = driver
        self.res_list = res_list
        self.start = start
        self.end = end
        self.account = account
        self.login_url = ""
        self.reg_date = ""
        time.sleep(0.5)

    def run(self):
        pass

    def collect_data(self):
        pass

    def login(self, url, id_selector, pw_selector, btn_selector, text):
        print(f"{Color.CYAN}{text}{Color.END} 파트너센터 로그인 중..", end=' ', flush=True)
        _id, _pw = self.account.values()
        self.driver.get(url)
        self.driver.find_element(By.CSS_SELECTOR, id_selector).send_keys(_id)
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, pw_selector).send_keys(_pw)
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, btn_selector).click()
        time.sleep(1)
        if self.driver.current_url == url:
            print(f"{Color.RED}[에러]{Color.END}")
            raise Exception(f"{Color.RED}* 업데이트 필요 *{Color.END}\n"
                            f"아이디 또는 비밀번호가 일치하지 않습니다.\n")
        else:
            print("[완료]")
