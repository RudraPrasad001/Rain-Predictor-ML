from datetime import datetime
import re

def convert_to_isRain_format(city, date_str, time_str):
    formatted_date = None
    formatted_time = None

    try:
        formatted_date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
    except Exception as e:
        print("Date parsing failed:", e)

    try:
        if time_str is not None:
            time_str = time_str.strip().lower()
            if ":" in time_str:
                # HH:MM format like "09:37"
                formatted_time = time_str
                print(time_str)
            elif re.match(r"\d{1,2}(am|pm)", time_str):
                # 12-hour format like "9am", "11PM"
                formatted_time = datetime.strptime(time_str, "%I%p").strftime("%H:%M")
            else:
                print("Unknown time format:", time_str)
        else:
            print("Time string is None")
    except Exception as e:
        print("Time parsing failed:", e)

    return {
        "date": formatted_date,
        "city": city,
        "time": formatted_time
    }
