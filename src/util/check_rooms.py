def check_rooms(date, room, res_list):
    if "스탠다드" in room:
        res_list[date]["standard"] += 1
    elif "디럭스" in room:
        res_list[date]["deluxe"] += 1
    elif "프리미엄" in room:
        if "프리미엄 트윈" in room or "프리미엄트윈" in room:
            res_list[date]["premium_twin"] += 1
        else:
            res_list[date]["premium"] += 1
    elif "스위트" in room:
        if "스위트 트윈" in room or "스위트트윈" in room:
            res_list[date]["suite_twin"] += 1
        elif "로얄 스위트" in room or "로얄스위트" in room:
            res_list[date]["royal_suite"] += 1
        else:
            res_list[date]["suite"] += 1
