from datetime import datetime, timedelta
import dateparser
import re

# Add this function to handle "next hour" logic
def resolve_relative_time(text: str):
    text = text.lower()
    now = datetime.now()

    if "next hour" in text:
        return now + timedelta(hours=1)
    elif match := re.search(r"in (\d+) hour", text):
        return now + timedelta(hours=int(match.group(1)))
    elif match := re.search(r"in (\d+) minutes?", text):
        return now + timedelta(minutes=int(match.group(1)))
    
    return None  # fallback