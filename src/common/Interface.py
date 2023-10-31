import datetime
from common.yanolja import Yanolja
from common.goodchoice import GoodChoice
from common.hoteltime import HotelTime
from common.coolstay import CoolStay
from util.chrome import web_driver
from util.color import Color
from util.table import enable_table
from config import YanoljaAccount, GoodChoiceAccount, HotelTimeAccount, CoolStayAccount


class Interface:
    """
    Interface class
    Author : Choi Soobin
    Date : 2023.01.05
    """

    def __init__(self):
        self.reservation_list = {}
        self.start_date = datetime.datetime.now().date()  # 오늘 날짜
        # self.start_date = datetime.date(2023, 2, 16)  # 날짜 직접 지정
        self.end_date = self.start_date + datetime.timedelta(days=14)
        self.driver = web_driver()

    def main_menu(self):
        try:
            print(f"검색 범위: {Color.CYAN}{self.start_date} ~ {self.end_date}{Color.END} ({Color.YELLOW}{(self.end_date - self.start_date).days}일{Color.END})\n")
            Yanolja(self.driver, self.reservation_list, self.start_date, self.end_date, YanoljaAccount.account, "모텔")  # 야놀자모텔
            Yanolja(self.driver, self.reservation_list, self.start_date, self.end_date, YanoljaAccount.account, "호텔")  # 야놀자호텔
            GoodChoice(self.driver, self.reservation_list, self.start_date, self.end_date, GoodChoiceAccount.account)  # 여기어때
            HotelTime(self.driver, self.reservation_list, self.start_date, self.end_date, HotelTimeAccount.account)  # 여기어때호텔
            CoolStay(self.driver, self.reservation_list, self.start_date, self.end_date, CoolStayAccount.account)  # 꿀스테이
            enable_table(self.reservation_list, self.start_date, self.end_date)  # pandas 테이블 적용
            # print(self.reservation_list)
            self.driver.quit()
        except Exception as e:
            print(e)
            self.driver.quit()
