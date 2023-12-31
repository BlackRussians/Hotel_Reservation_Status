import time
import colorama
import locale
from common.Interface import Interface
from util.color import Color
from config import __VERSION__


def main():
    print(f"{Color.YELLOW}Ver {__VERSION__}{Color.END}")
    start_time = time.time()  # 시간 측정 시작
    interface.main_menu()
    end_time = time.time() - start_time  # 시간 측정 종료
    print(f'Finished in {end_time:.2f}s\n')
    input("Press enter to close...")  # 종료 메시지


if __name__ == '__main__':
    locale.setlocale(locale.LC_CTYPE, "korean")  # time.strftime locale 에러해결(pyinstaller 사용시)
    colorama.init()  # 글 색상 적용 라이브러리
    interface = Interface()
    main()
