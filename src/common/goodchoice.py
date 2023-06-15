import re
import time
import datetime
from common.partner_center import PartnerCenter
from selenium.webdriver.common.by import By
from util.check_rooms import check_rooms


class GoodChoice(PartnerCenter):
    def __init__(self, driver, res_list, start, end, account):
        super().__init__(driver, res_list, start, end, account)
        self.login_url = "https://ad.goodchoice.kr/login"
        self.reg_date = re.compile(r"(\d{1,4}-\d{1,2}-\d{1,2})+")
        self.run()

    def run(self):
        self.login(self.login_url, "div.input-wrapper > input:nth-child(1)", "div.input-wrapper > input:nth-child(2)",
                   "div.login-wrapper > form:nth-child(3) > button", "여기어때")
        time.sleep(0.5)

        print("데이터 불러 오는 중..", end=" ", flush=True)
        self.driver.get(
            f"https://ad.goodchoice.kr/reservation/history/stay?start_date={self.start}&end_date={self.end}&q=&armgno=&sort=checkin&page=1&checked_in=&status=")
        pages = self.num_pages()

        if pages > 1:
            for i in range(1, pages + 1):
                self.driver.get(
                    f"https://ad.goodchoice.kr/reservation/history/stay?start_date={self.start}&end_date={self.end}&q=&armgno=&sort=checkin&page={i}&checked_in=&status=")
                self.collect_data()
        else:
            self.collect_data()
        print("[완료]")

    def collect_data(self):
        time.sleep(0.5)
        time_table_rows = self.driver.find_elements(By.CSS_SELECTOR, "div.common-component--table > table > tbody > tr")
        time.sleep(0.5)
        test_list = 0
        for tr in time_table_rows:
            # status_dec = tr.find_element(By.CSS_SELECTOR, ".is-first").text
            room_dec = tr.find_element(By.CSS_SELECTOR, ".detail-info").text
            room_date = re.compile(self.reg_date).findall(room_dec)
            if "예약취소" not in tr.find_element(By.CSS_SELECTOR, ".is-first").text:
                # print(status_dec, room_dec, room_date)
                t1 = datetime.datetime.strptime(room_date[0].replace("-", ""), "%Y%m%d")
                t2 = datetime.datetime.strptime(room_date[1].replace("-", ""), "%Y%m%d")
                for i in range((t2 - t1).days):
                    test_list += 1
                    check_in = t1 + datetime.timedelta(days=i)
                    check_rooms(str(check_in.date()), room_dec, self.res_list)
        #     else:
        #         print(status_dec, room_dec, room_date)
        # print("총 예약수:", test_list)

    def num_pages(self):
        time.sleep(0.5)
        page_items = self.driver.find_elements(By.CSS_SELECTOR, "div.contents-component > ul > li")
        page_items[len(page_items) - 1].click()
        page_items = self.driver.find_elements(By.CSS_SELECTOR, "div.contents-component > ul > li")

        return int(page_items[len(page_items) - 3].text)
