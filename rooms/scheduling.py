from datetime import datetime

import arrow
from ics import Calendar

now = datetime.now()
current_time = now.strftime("%H:%M")


# [Hour, Minute, Second]
SCHEDULES = {
    "7 Period Day": {
        "startFlex": [11, 20, 0],
        "swapFlex": [11, 45, 0],
        "endFlex": [12, 15, 0],
    },
    "3 Period Block": {
        "startFlex": [10, 50, 0],
        "swapFlex": [11, 20, 0],
        "endFlex": [11, 55, 0],
    },
    "4 Period Block": {
        "startFlex": [10, 50, 0],
        "swapFlex": [11, 20, 0],
        "endFlex": [11, 55, 0],
    },
    "Mass Schedule": {
        "startFlex": [11, 10, 0],
        "swapFlex": [11, 35, 0],
        "endFlex": [12, 5, 0],
    },
    "Assembly Schedule": {
        "startFlex": [10, 40, 0],
        "swapFlex": [11, 10, 0],
        "endFlex": [11, 40, 0],
    },
}


def get_today_schedule() -> str:
    today = arrow.now().to("utc").floor("day")

    with open("CalExport.ics", "r") as f:
        file = f.read()

    c = Calendar(file)
    for event in c.events:
        for schedule in SCHEDULES:
            if schedule not in event.name:
                continue

            if event.begin.floor("day") == today:
                return schedule

    return "No School"


def check_flex(day: str) -> int:
    """
    -1 = Invalid Day
    0  = Not Flex
    1  = Flex 1
    2  = Flex 2
    """

    if day not in SCHEDULES:
        return -1

    schedule = SCHEDULES[day]

    # Get current time
    now = arrow.now()

    # Create time objects for startFlex and endFlex using today's date
    start_flex = now.replace(
        hour=schedule["startFlex"][0],
        minute=schedule["startFlex"][1],
        second=schedule["startFlex"][2],
        microsecond=0,
    )

    swap_flex = now.replace(
        hour=schedule["swapFlex"][0],
        minute=schedule["swapFlex"][1],
        second=schedule["swapFlex"][2],
        microsecond=0,
    )

    end_flex = now.replace(
        hour=schedule["endFlex"][0],
        minute=schedule["endFlex"][1],
        second=schedule["endFlex"][2],
        microsecond=0,
    )

    if start_flex <= now <= swap_flex:
        return 1
    elif swap_flex <= now <= end_flex:
        return 2

    return 0


def main():
    day = get_today_schedule()
    print(check_flex(day))


if __name__ == "__main__":
    main()
