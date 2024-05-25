import spacy
import re
from spacy.pipeline import EntityRuler
from datetime import datetime
import dateparser

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Map car types to IDs
car_type_map = {
    "crossover": "10",
    "family car": "2",
    "luxury car": "8",
    "jeep": "5",
    "mini car": "1",
    "minivan": "9",
    "executive car": "3",
    "sports car": "4",
    "commercial vehicle": "7",
    "pickup truck": "6"
}

# Map manufacturers to IDs
manufacturer_map = {
    "baw": "193",
    "eveasy": "323",
    "ktm": "72",
    "xpeng": "290",
    "zeekr": "333",
    "audi": "1",
    "abarth": "53",
    "autobianchi": "96",
    "oldsmobile": "76",
    "austin": "102",
    "opel": "2",
    "ora": "224",
    "aiways": "288",
    "iveco": "85",
    "infiniti": "3",
    "isuzu": "4",
    "levc": "299",
    "lti": "77",
    "alfa romeo": "5",
    "alpine": "115",
    "mg": "6",
    "aston martin": "54",
    "few": "168",
    "bmw": "7",
    "byd": "141",
    "buick": "8",
    "bentley": "55",
    "gac": "99",
    "gmc": "9",
    "geo": "94",
    "jiayuan": "346",
    "jac": "200",
    "geely": "177",
    "jeep": "10",
    "jeep (idf)": "59",
    "genesis": "93",
    "great wall": "11",
    "dacia": "12",
    "dodge": "13",
    "dongfeng": "88",
    "ds": "14",
    "daewoo": "60",
    "daihatsu": "15",
    "hummer": "16",
    "hongqi": "301",
    "honda": "17",
    "hino": "95",
    "wey": "284",
    "voyah": "322",
    "volvo": "18",
    "tata": "87",
    "toyota": "19",
    "tesla": "62",
    "jaguar": "20",
    "hyundai": "21",
    "lada": "80",
    "lynk & co": "321",
    "lincoln": "23",
    "leapmotor": "320",
    "lixiang": "98",
    "lamborghini": "63",
    "land rover": "24",
    "lancia": "25",
    "lexus": "26",
    "mazda": "27",
    "man": "86",
    "maserati": "28",
    "mini": "29",
    "mitsubishi": "30",
    "maxus": "89",
    "mercedes": "31",
    "nio": "289",
    "nissan": "32",
    "nanjing": "78",
    "saab": "33",
    "sun living": "302",
    "ssangyong": "34",
    "sunshine": "56",
    "subaru": "35",
    "suzuki": "36",
    "seat": "37",
    "citroën": "38",
    "smart": "39",
    "centro": "97",
    "skoda": "40",
    "skywell": "300",
    "seres": "287",
    "polestar": "231",
    "volkswagen": "41",
    "pontiac": "42",
    "ford": "43",
    "porsche": "44",
    "forthing": "334",
    "piaggio": "90",
    "fiat": "45",
    "peugeot": "46",
    "ferrari": "57",
    "chery": "147",
    "cadillac": "47",
    "cupra": "92",
    "kia": "48",
    "chrysler": "49",
    "rover": "50",
    "renault": "51",
    "chevrolet": "52"
}

# Define patterns for the custom car type entities
patterns = [{"label": "CAR_TYPE", "pattern": car_type} for car_type in car_type_map.keys()]

# Create an EntityRuler and add the patterns to it
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns(patterns)

def parse_date_range(date_text):
    parsed_date = dateparser.parse(date_text)
    if parsed_date:
        start_year = parsed_date.year
        current_year = datetime.now().year
        return f"{start_year}-{current_year}"
    else:
        return None


def extract_parameters(user_input):
    # Parse the user input using spaCy
    doc = nlp(user_input)
    
    # Initialize parameters
    car_family_type = []
    year_range = None
    price_range = None
    manufacturers = []

    # Extract parameters using spaCy's NER and syntactic parsing
    for ent in doc.ents:
        if ent.label_ == "CAR_TYPE":
            car_type_id = car_type_map.get(ent.text.lower())
            if car_type_id:
                car_family_type.append(car_type_id)
        elif ent.label_ == "DATE":
            parsed_range = parse_date_range(ent.text.lower())
            if parsed_range:
                year_range = parsed_range
            else:
                year_range = ent.text
        elif ent.label_ == "MONEY":
            # Extract digits from the money string
            price_digits = re.findall(r'\d+', ent.text)
            if len(price_digits) == 2:
                price_range = "-".join(price_digits)
        elif ent.label_ == "ORG":
            manufacturer_id = manufacturer_map.get(ent.text.lower())
            if manufacturer_id:
                manufacturers.append(manufacturer_id)

    return car_family_type, year_range, price_range, manufacturers

def construct_url(car_family_type, year_range, price_range, manufacturers):
    base_url = "https://www.yad2.co.il/vehicles/cars?"
    params = []

    if car_family_type:
        params.append("carFamilyType=" + ",".join(car_family_type))

    if year_range:
        params.append(f"year={year_range}")

    if price_range:
        params.append(f"price={price_range}")

    if manufacturers:
        params.append("manufacturer=" + ",".join(manufacturers[:4]))

    return base_url + "&".join(params)

def main():
    user_input = "I am looking for an executive car or jeep from 2018 that costs between 5000$-7000$ and is made by Toyota,Jeep,MG,BMW or Mazda."
    car_family_type, year_range, price_range, manufacturers = extract_parameters(user_input)
    url = construct_url(car_family_type, year_range, price_range, manufacturers)
    print("Generated URL:", url)

if __name__ == "__main__":
    main()
