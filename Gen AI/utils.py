import dateparser
from datetime import datetime

def parse_date_range(date_text):
    parsed_date = dateparser.parse(date_text)
    if parsed_date:
        start_year = parsed_date.year
        current_year = datetime.now().year
        return f"{start_year}-{current_year}"
    else:
        return None
