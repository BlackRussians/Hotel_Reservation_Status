import re
import time
import datetime
from common.partner_center import PartnerCenter
from selenium.webdriver.common.by import By
from selenium.common import JavascriptException
from util.check_rooms import check_rooms


class CoolStay(PartnerCenter):
    def __init__(self, driver, res_list, start, end, account):
        super().__init__(driver, res_list, start, end, account)
        self.login_url = "https://partner.coolstay.co.kr/login"
        self.reg_date = re.compile(r"(\d{1,4}\.\d{1,2}\.\d{1,2})+")
        self.run()

    def run(self):
        self.login(self.login_url, "#userId", "#userPassword", ".MuiButton-root", "꿀스테이")
        time.sleep(0.5)

        self.driver.get(
            f"https://partner.coolstay.co.kr/reservation?&page=1&searchType=ST602,ST607&searchExtra={self.start.strftime('%Y%m%d')}|{self.end.strftime('%Y%m%d')},010102&sort=BOOK_DESC&tabState=1&selectSort=0&selectDateRange=customInput")
        print("데이터 불러 오는 중..", end=" ", flush=True)

        try:
            # 팝업 발생 시 에러 방지
            self.driver.execute_script("document.querySelector('.MuiDialog-root').style.visibility = 'hidden';")
            self.driver.execute_script("document.querySelector('.logout').style.overflow = 'auto';")
        except JavascriptException:
            pass

        pages = len(self.driver.find_elements(By.CSS_SELECTOR, ".MuiTablePagination-root > div > button")) - 4
        time.sleep(0.5)

        if pages > 1:
            for i in range(1, pages + 1):
                self.driver.get(
                    f"https://partner.coolstay.co.kr/reservation?&page={i}&searchType=ST602,ST607&searchExtra={self.start.strftime('%Y%m%d')}|{self.end.strftime('%Y%m%d')},010102&sort=BOOK_DESC&tabState=1&selectSort=0&selectDateRange=customInput")
                time.sleep(2)
                self.collect_data()
        else:
            self.collect_data()
        print("[완료]")

    def collect_data(self):
        time_table_rows = self.driver.find_elements(By.CSS_SELECTOR, ".sc-dIUggk > div")
        time.sleep(1)
        for tr in time_table_rows:
            if "예약취소" not in tr.find_element(By.CSS_SELECTOR, "div:nth-child(1)").text:
                room_dec = tr.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text
                room_date = re.compile(self.reg_date).findall(room_dec)
                t1 = datetime.datetime.strptime(room_date[0].replace(".", ""), "%Y%m%d")
                t2 = datetime.datetime.strptime(room_date[1].replace(".", ""), "%Y%m%d")
                for i in range((t2 - t1).days):
                    check_in = t1 + datetime.timedelta(days=i)
                    check_rooms(str(check_in.date()), room_dec, self.res_list)
