# nlp_pipeline.py : responisble for the NLP processing and extracting the parameters from the user input

import spacy
from spacy.pipeline import EntityRuler
from config import car_type_map, manufacturer_map
from utils import parse_date_range,text_to_number
import re


# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Define patterns for the custom car type entities
patterns1 = [{"label": "CAR_TYPE", "pattern": car_type} for car_type in car_type_map.keys()]
patterns2 = [{"label": "ORG", "pattern": man} for man in manufacturer_map.keys()]

# Create an EntityRuler and add the patterns to it
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns(patterns1)
ruler.add_patterns(patterns2)


def extract_parameters(user_input):
    # Parse the user input
    doc = nlp(user_input)
    
    # Initialize parameters
    car_family_type = []
    year_range = None
    price_range = None
    manufacturers = []

    # Extract parameters
    print("entities: ",doc.ents)
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
        elif ent.label_ == "MONEY" or ent.label_ == "CARDINAL":
            # Convert text to number
            number = text_to_number(ent.text)
            if number:
                price_range = f"-1-{number}"
            else:
                price_digits = re.findall(r'\d+', ent.text)
                if price_digits:
                    if len(price_digits) == 1:
                        price_range = "-1-" + price_digits[0]
                    elif len(price_digits) == 2:
                        price_range = "-".join(price_digits)
        elif ent.label_ == "ORG" or ent.label_ == "PRODUCT":
            manufacturer_id = manufacturer_map.get(ent.text.lower())
            if manufacturer_id:
                manufacturers.append(manufacturer_id)

    return car_family_type, year_range, price_range, manufacturers

