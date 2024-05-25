from nlp_pipeline import extract_parameters
from config import car_type_map, manufacturer_map

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
