#utils.py : helper functions 

import dateparser
from datetime import datetime
import re
from translate import Translator
from word2number import w2n


def translate_hebrew_to_english(text):
    translator= Translator(to_lang="en", from_lang="he")
    translation = translator.translate(text)
    return translation

def parse_date_range(date_text):
    parsed_date = dateparser.parse(date_text, settings={"PREFER_DATES_FROM": "future"})
    if parsed_date:
        start_year = parsed_date.year
        # Check if start year is mentioned in the input text
        if str(start_year) in date_text:
            # Extract the end year if it's explicitly mentioned
            years = re.findall(r'\b\d{4}\b', date_text)
            if len(years) == 2:
                end_year = max(years[0],years[1])
            else:
                end_year = -1
        else:
            # If start year is not mentioned, assume the current year as end year
            end_year = datetime.now().year
        return f"{start_year}-{end_year}"
    else:
        years = re.findall(r'\b\d{4}\b', date_text)
        if len(years) == 2:
            start_year, end_year = int(years[0]), int(years[1])
            return f"{start_year}-{end_year}"
        else:
            return f"{years[0]}-{-1}"
        
def text_to_number(text):
    try:
        # Handle specific multipliers like "grand"
        if "grand" in text:
            number = w2n.word_to_num(text.replace("grand", "").strip()) * 1000
        else:
            number = w2n.word_to_num(text)
        return number
    except ValueError:
        return None