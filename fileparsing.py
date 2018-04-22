#-*- coding: utf-8 -*-
import datetime
DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
def get_timetable():
    tomorrow = datetime.date.today()+datetime.timedelta(days=1)
    timetable = open("timetable.txt", "r")
    found = False
    rStr = ""
    for line in timetable.readlines():
        if line.__contains__(DAYS[tomorrow.weekday()]):
            found = True
            continue
        elif found:
            split = line.split("|")
            is_top = (int(tomorrow.strftime("%W")) - 5)%2
            search_week = "T" if is_top else "B"
            if line.isspace():
                found = False
                break
            elif split[0] == search_week or split[0] == "E":
                if not rStr=="":
                    rStr+="\n"
                rStr+=split[1].rstrip()
    return rStr


if __name__ == "__main__":
    print get_timetable()