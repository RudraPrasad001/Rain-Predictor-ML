import dateparser


def parse_natural_date(raw_date: str) -> str:
    parsed = dateparser.parse(raw_date)
    if parsed:
        return parsed.strftime("%d-%m-%Y")
    return None