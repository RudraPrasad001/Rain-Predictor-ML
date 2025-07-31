from datetime import datetime

def convert_to_isRain_format(city: str, date_str: str, time_str: str):
    # Convert date from dd-mm-yyyy to yyyy-mm-dd
    formatted_date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

    # Convert time from 12hr format (like '11pm') to 24hr (like '23:00')
    formatted_time = datetime.strptime(time_str.lower(), "%I%p").strftime("%H:%M")

    return {
        "date": formatted_date,
        "city": city,
        "time": formatted_time
    }
