import re
import time
import datetime
from common.partner_center import PartnerCenter
from selenium.webdriver.common.by import By
from util.check_rooms import check_rooms


class HotelTime(PartnerCenter):
    def __init__(self, driver, res_list, start, end, account):
        super().__init__(driver, res_list, start, end, account)
        self.login_url = "https://hotel.gcpartner.kr/login"
        self.reg_date = re.compile(r"^\d{1,4}\.\d{1,2}\.\d{1,2}")
        self.run()

    def run(self):
        self.login(self.login_url, "#loginForm_uid", "#loginForm_upw", ".login-button-box", "호텔타임")
        time.sleep(0.5)

        print("데이터 불러 오는 중..", end=" ", flush=True)
        self.driver.get("https://hotel.gcpartner.kr/reservations/reservation-list")
        time.sleep(0.5)

        self.select_filters()  # 필터 설정
        self.click_calender()  # 날짜 선택
        time.sleep(1)

        page_items = self.driver.find_elements(By.CSS_SELECTOR, ".ant-spin-container > ul > li")
        len_pages = int(page_items[len(page_items) - 2].text)  # 총 페이지 수

        if len_pages > 1:
            for i in range(1, len_pages + 1):
                page_items = self.driver.find_elements(By.CSS_SELECTOR,
                                                       ".ant-spin-container > ul > li")  # page_items 업데이트
                for idx in range(1, len(page_items) - 1):
                    if int(page_items[idx].text) == i:
                        page_items[idx].click()
                        self.collect_data()
        else:
            self.collect_data()
        print("[완료]")

    def collect_data(self):
        time.sleep(3)  # 예약 상태 fetch 대기 시간
        time_table_rows_1 = self.driver.find_elements(By.CSS_SELECTOR,
                                                      "div.ant-table-fixed-left > div > div > table > tbody > tr")  # 예약 상태가 있는 테이블
        time.sleep(0.5)
        time_table_rows_2 = self.driver.find_elements(By.CSS_SELECTOR,
                                                      "div.ant-table-scroll > div > table > tbody > tr")  # 체크인, 체크아웃, 룸타입 등이 있는 테이블
        time.sleep(0.5)
        cancel_rows = []
        # nl = "\n"

        # 예약취소 index 찾아서 cancel_rows list에 append 하기
        for i, tr in enumerate(time_table_rows_1):
            status = tr.find_elements(By.CSS_SELECTOR, "td")
            if "취소" in status[0].text:
                cancel_rows.append(i)

        # 예약취소 row index를 제외한 데이터 취합하기
        for i, tr in enumerate(time_table_rows_2):
            # status_dec = time_table_rows_1[i].find_elements(By.CSS_SELECTOR, "td")
            room_dec = tr.find_elements(By.CSS_SELECTOR, "td")
            if i not in cancel_rows:
                # print(f"{status_dec[0].text.replace(nl, '')} {status_dec[3].text.split(nl)[0]}({status_dec[3].text.split(nl)[1]}), {room_dec[4].text}, {room_dec[5].text}, {room_dec[7].text}")
                t1 = datetime.datetime.strptime(self.reg_date.search(room_dec[4].text).group().replace(".", ""),
                                                "%Y%m%d")
                t2 = datetime.datetime.strptime(self.reg_date.search(room_dec[5].text).group().replace(".", ""),
                                                "%Y%m%d")
                for idx in range((t2 - t1).days):
                    check_in = t1 + datetime.timedelta(days=idx)
                    check_rooms(str(check_in.date()), room_dec[7].text, self.res_list)
            # else:
            #     print(f"{status_dec[0].text.replace(nl, '')}, {status_dec[3].text.split(nl)[0]}({status_dec[3].text.split(nl)[1]}), {room_dec[4].text}, {room_dec[5].text}, {room_dec[7].text}")

    def click_calender(self):
        self.driver.find_element(By.CSS_SELECTOR, ".ant-calendar-picker-input").click()  # 캘린더 클릭
        time.sleep(0.5)
        data = self.driver.find_elements(By.CSS_SELECTOR,
                                         ".ant-calendar-range-part > div:nth-child(2) > div.ant-calendar-body > table > tbody > tr")
        clicked = 0

        for tr in data:
            for td in tr.find_elements(By.CSS_SELECTOR, "td"):
                title = td.get_attribute("title")
                if title == self.start.strftime("%Y년 %#m월 %#d일") and clicked == 0:
                    clicked += 1
                    td.click()
                if title == self.end.strftime("%Y년 %#m월 %#d일") and clicked == 1:
                    td.click()
                    break
            else:
                continue
            break

    def select_filters(self):
        # 입실일 기준 선택
        self.driver.find_element(By.CSS_SELECTOR, "div.range-widget > div:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 "body > div:nth-child(4) > div > div > div.ant-select-dropdown-content > ul > li:nth-child(1)").click()

        # 표시 개수
        self.driver.find_element(By.CSS_SELECTOR, "div.filter-box > div:nth-child(1)").click()
        # driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(5) > div > div > div.ant-select-dropdown-content > ul > li:nth-child(1)").click()  # 10개씩 보기
        # driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(5) > div > div > div.ant-select-dropdown-content > ul > li:nth-child(2)").click()  # 20개씩 보기
        # driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(5) > div > div > div.ant-select-dropdown-content > ul > li:nth-child(3)").click()  # 30개씩 보기
        # driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(5) > div > div > div.ant-select-dropdown-content > ul > li:nth-child(4)").click()  # 40개씩 보기
        self.driver.find_element(By.CSS_SELECTOR,
                                 "body > div:nth-child(5) > div > div > div.ant-select-dropdown-content > ul > li:nth-child(5)").click()  # 50개씩 보기

        # 예약상태 확정
        # driver.find_element(By.CSS_SELECTOR, "div.filter-box > div:nth-child(2)").click()
        # driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(6) > div > div > div.ant-select-dropdown-content > ul > li:nth-child(2)").click()
