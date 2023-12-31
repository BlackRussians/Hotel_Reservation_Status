import pandas
import pandas as pd

from tabulate import tabulate


def enable_table(res_list, start, end):
    date_range = [date.strftime("%Y-%m-%d") for date in pd.date_range(start, periods=(end - start).days + 1)]
    pd_data = {}
    for date in res_list:
        pd_data[date] = [room[1] for room in res_list[date].items()]

    df = pd.DataFrame(
        pd_data,
        index=["스탠다드", "디럭스", "프리미엄", "프리미엄트윈", "스위트", "스위트트윈", "로얄스위트"],
        columns=date_range
    )
    print(tabulate(df, headers='keys', tablefmt="rounded_outline"))


def reset_res_list(res_list, start, end):
    for date in pandas.date_range(start, periods=(end - start).days + 1):
        res_list[date.strftime("%Y-%m-%d")] = {
            "standard": 0,
            "deluxe": 0,
            "premium": 0,
            "premium_twin": 0,
            "suite": 0,
            "suite_twin": 0,
            "royal_suite": 0
        }
