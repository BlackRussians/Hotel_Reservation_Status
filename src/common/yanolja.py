import re
import time
import datetime
from common.partner_center import PartnerCenter
from selenium.webdriver.common.by import By
from util.check_rooms import check_rooms
from selenium.common.exceptions import NoSuchElementException


class Yanolja(PartnerCenter):
    def __init__(self, driver, res_list, start, end, account, accom_type):
        super().__init__(driver, res_list, start, end, account)
        self.accom_type = accom_type
        self.display_size = 300
        self.login_url = "https://account.yanolja.biz/?serviceType=PC&redirectURL=%2F&returnURL=https%3A%2F%2Fpartner.yanolja.com%2Fauth%2Flogin"
        self.reg_date = re.compile(r"^\d{1,4}\.\d{1,2}\.\d{1,2}")
        self.run()

    def run(self):
        self.login(self.login_url, "input[name='id']", "input[name='password']", ".v-btn__content",
                   f"야놀자[{self.accom_type}]")
        time.sleep(0.5)
        self.check_accom_type(self.accom_type)  # 숙소타입 검사(모텔/호텔)

        print("데이터 불러 오는 중..", end=" ", flush=True)
        self.driver.get(
            f"https://partner.yanolja.com/reservation/search?dateType=STAY_DATE&startDate={self.start}&endDate="f"{self.end}&reservationStatus=COMPLETE&keywordType=VISITOR_NAME&page=1&size={self.display_size}&sort=checkInDate,asc&propertyCategory=MOTEL&selectedDate={self.start}&searchType=detail&useTypeDetail=STAY&useTypeCheckIn=ALL")
        self.collect_data()
        print("[완료]")
        self.driver.get("https://partner.yanolja.com/auth/logout")  # 로그아웃

    def collect_data(self):
        time_table_rows = self.driver.find_elements(By.CSS_SELECTOR,
                                                    ".ReservationSearchList__list > div > table > tbody > tr")
        time.sleep(0.5)
        for tr in time_table_rows:
            room_dec = tr.find_element(By.CSS_SELECTOR, ".body-2 > div").text
            room_date = tr.find_elements(By.CSS_SELECTOR, "td.ReservationSearchListItem__date > span")
            # print(f"Date {room_date[0].text} ~ {room_date[1].text} - {room_dec}")
            t1 = datetime.datetime.strptime(self.reg_date.search(room_date[0].text).group().replace(".", ""), "%Y%m%d")
            t2 = datetime.datetime.strptime(self.reg_date.search(room_date[1].text).group().replace(".", ""), "%Y%m%d")
            for i in range((t2 - t1).days):
                check_in = t1 + datetime.timedelta(days=i)
                check_rooms(str(check_in.date()), room_dec, self.res_list)

    def check_accom_type(self, val):
        accom_type = self.driver.find_element(By.CSS_SELECTOR,
                                              "button.ya-ml-16 > .v-btn__content > span.body-4.ya-mr-4 > .v-chip__content").text
        if accom_type != val:
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, "button.ya-ml-16").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, "div.v-select__slot").click()
            time.sleep(0.5)
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#app > div:nth-child(4) > div > div > div").click()
                time.sleep(1)
            except NoSuchElementException:
                self.driver.find_element(By.CSS_SELECTOR, "#app > div:nth-child(3) > div > div > div").click()
                time.sleep(1)
