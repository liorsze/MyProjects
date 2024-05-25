#main.py : the main code for user input and output

from nlp_pipeline import extract_parameters
from utils import translate_hebrew_to_english

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
    user_input = " אני מחפש טויוטה משפחתית במחיר של עד מאה אלף שקלים משנת 2016 ומעלה "
    translated_input = translate_hebrew_to_english(user_input)
    print(translated_input)
    car_family_type, year_range, price_range, manufacturers = extract_parameters(translated_input)
    url = construct_url(car_family_type, year_range, price_range, manufacturers)
    print("Generated URL:", url)

if __name__ == "__main__":
    main()
