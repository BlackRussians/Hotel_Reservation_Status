import re
import time
from datetime import datetime, timedelta
from common.partner_center import PartnerCenter
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from util.check_rooms import check_rooms


class HotelTime(PartnerCenter):
    def __init__(self, driver, res_list, start, end, account):
        super().__init__(driver, res_list, start, end, account)
        self.login_url = "https://partner.goodchoice.kr/login"
        self.reg_date = re.compile(r"^\d{1,4}\.\d{1,2}\.\d{1,2}")
        self.run()

    def run(self):
        self.login(self.login_url, "form > div:nth-child(3) > div > input[type=text]",
                   "form > div:nth-child(4) > div > input[type=password]", "form > div:nth-child(6) > button", "호텔타임")
        time.sleep(0.5)

        print("데이터 불러 오는 중..", end=" ", flush=True)
        self.driver.get("https://partner.goodchoice.kr/reservations/reservation-list")
        time.sleep(2)

        self.select_filters(3)  # 필터 설정 1: 10개씩 보기, 2: 20개씩 보기, 3: 50개씩 보기
        self.click_calender()  # 날짜 선택
        time.sleep(1)

        page_items = self.driver.find_elements(By.CSS_SELECTOR, "div.css-16l3vya.euxpggr3 > button")
        len_pages = len(page_items)-2  # 총 페이지 수
        if len_pages > 1:
            for i, page in enumerate(page_items):
                if i == 1:
                    self.collect_data()  # 데이터 취합
                elif 1 < i <= len_pages:
                    page.click()
                    self.collect_data()  # 데이터 취합
        else:
            self.collect_data()
        print("[완료]")

    def collect_data(self):
        # time.sleep(1)  # 예약 상태 fetch 대기 시간
        # 예약상태, 통합예약번호, 예약자 정보, 상품명 및 판매유형, 입실/퇴실 일시, 금액 및 할인정보 등 데이터
        time_table_value = "div.fix.css-1u0qfsj.e1kggxuk2 > table > tbody > tr"
        # 예약 상태가 있는 테이블
        time_table_rows: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, time_table_value)
        cancel_rows = []
        nl = "\n"  # newline

        # 예약취소 index 찾아서 cancel_rows list에 append 하기
        for i, tr in enumerate(time_table_rows):  # type: int, WebElement
            status = tr.find_elements(By.CSS_SELECTOR, "td")
            # print(status[0].text.split(nl)[0], status[1].text.split(nl)[0], status[2].text.split(nl)[0])  # 에약 목록 출력
            if status[0].text.split(nl)[0] == "예약취소":
                # print(status[0].text.split(nl)[0], status[1].text.split(nl)[0], status[2].text.split(nl)[0])  # 에약취소 목록 출력
                cancel_rows.append(i)

        # 예약취소 row index를 제외한 데이터 취합하기
        for i, tr in enumerate(time_table_rows):  # type: int, WebElement
            room_dec = tr.find_elements(By.CSS_SELECTOR, "td")
            # 예) 스위트 트윈 [2인조식포함, 넷플릭스 시청가능] 2023.11.04 (토) 20:00 2023.11.05 (일) 12:00
            # print(room_dec[3].text.split(nl)[0], room_dec[4].text.split(nl)[0], room_dec[4].text.split(nl)[1])
            if i not in cancel_rows:
                # 예) 예약확정 이름 디럭스 [2인조식포함, 넷플릭스 시청가능], 2023.10.31 (화) 18:00 2023.11.01 (수) 12:00
                t1 = datetime.strptime(
                    self.reg_date.search(room_dec[4].text.split(nl)[0]).group().replace(".", ""), "%Y%m%d")
                t2 = datetime.strptime(
                    self.reg_date.search(room_dec[4].text.split(nl)[1]).group().replace(".", ""), "%Y%m%d")
                for idx in range((t2 - t1).days):
                    check_in = t1 + timedelta(days=idx)
                    check_rooms(str(check_in.date()), room_dec[3].text.split(nl)[0], self.res_list)

    def click_calender(self):
        calendar_sel = "div.Box_picker__Yz68i"
        data_sel = "div.react-calendar.yeogi-calendar > div > div > div > div > div.react-calendar__month-view__days > button"
        next_month_button = "div.Navigation_navigation__h8sDM > div > button:nth-child(3)"
        next_month = 1 if self.start.month != self.end.month else 0
        clicked = 0

        self.driver.find_element(By.CSS_SELECTOR, calendar_sel).click()  # 캘린더 클릭
        time.sleep(0.5)

        while True:
            data: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, data_sel)
            if clicked == 0:
                for date in data:
                    calendar_date = date.find_element(By.CSS_SELECTOR, "abbr").get_attribute("aria-label")
                    if calendar_date == self.start.strftime("%Y년 %#m월 %#d일") and clicked == 0:
                        clicked += 1
                        date.click()
                        if next_month == 1:
                            self.driver.find_element(By.CSS_SELECTOR, next_month_button).click()  # 다음달 클릭
                            break
                    if calendar_date == self.end.strftime("%Y년 %#m월 %#d일") and clicked == 1 and next_month == 0:
                        clicked += 1
                        date.click()
                        self.driver.find_element(By.CSS_SELECTOR,
                                                 "div.css-z127pw.ec44zn12 > button:nth-child(2)").click()  # 캘린더 적용 클릭
                        break
                continue
            if next_month == 1 and clicked == 1:
                for date in data:
                    calendar_date = date.find_element(By.CSS_SELECTOR, "abbr").get_attribute("aria-label")
                    if calendar_date == self.end.strftime("%Y년 %#m월 %#d일") and clicked == 1:
                        clicked += 1
                        date.click()
                        break
                self.driver.find_element(By.CSS_SELECTOR, "div.css-cqouxt.ec44zn14 > div:nth-child(2) > button:nth-child(2)").click()  # 캘린더 적용 클릭
                break
            else:
                break
        time.sleep(0.5)

    def select_filters(self, display):
        # CSS SELECTOR
        st_check_in = "div.css-1kiy3dg.ehynccb1 > div:nth-child(1)"
        st_date = "div.css-1kiy3dg.ehynccb1 > div:nth-child(2)"
        st_display = "div.styled__RightFilterDiv-sc-ljl4di-7.hNmXkV > div.css-gauqmr.eifwycs3"

        # 입실일 기준 선택
        self.driver.find_element(By.CSS_SELECTOR, st_check_in).click()
        self.driver.find_element(By.CSS_SELECTOR, f"{st_check_in} > div > ul > li:nth-child(3)").click()  # 투숙일
        time.sleep(1)

        # 날짜 기준 선택
        self.driver.find_element(By.CSS_SELECTOR, st_date).click()
        self.driver.find_element(By.CSS_SELECTOR, f"{st_date} > div > ul > li:nth-child(4)").click()  # 직접 선택
        time.sleep(1)

        # 표시 개수
        self.driver.find_element(By.CSS_SELECTOR, st_display).click()
        self.driver.find_element(By.CSS_SELECTOR, f"{st_display} > div > ul > li:nth-child({display})").click()
        time.sleep(1)
