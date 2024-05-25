import tkinter as tk
from tkinter import messagebox
from nlp_pipeline import extract_parameters
from utils import translate_hebrew_to_english
import pyperclip

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

def search_button_click():
    user_input = text_input.get("1.0", "end").strip()
    if not user_input:
        messagebox.showerror("Error", "Please enter your query.")
        return
    
    user_input = text_input.get("1.0", "end").strip()
    translated_input = translate_hebrew_to_english(user_input)
    print("HE->EN: ",translated_input)
    car_family_type, year_range, price_range, manufacturers = extract_parameters(translated_input)
    url = construct_url(car_family_type, year_range, price_range, manufacturers)
    output_box.delete("1.0", "end")
    output_box.insert("1.0", url)
    print("Generated URL: ",url)
    
def copy_url():
    url = output_box.get("1.0", "end").strip()
    if url:
        pyperclip.copy(url)
        messagebox.showinfo("Success", "URL copied to clipboard.")

def clear_content():
    text_input.delete("1.0", "end")
    output_box.delete("1.0", "end")

# Create the main window
root = tk.Tk()
root.title("Car Search")

# Create a text input box with placeholder text
placeholder_text = " אני מחפש טויוטה מרצדס או אאודי משפחתית במחיר של עד מאה אלף שקלים משנת 2016 "
text_input = tk.Text(root, height=5, width=50)
text_input.insert("1.0", placeholder_text)
text_input.pack()

# Create a search button
search_button = tk.Button(root, text="Search", command=search_button_click)
search_button.pack()

# Create an output box
output_box = tk.Text(root, height=5, width=50)
output_box.pack()

# Create a Copy URL button
copy_button = tk.Button(root, text="Copy URL", command=copy_url)
copy_button.pack()

# Create a Clear button
clear_button = tk.Button(root, text="Clear", command=clear_content)
clear_button.pack()

# Start the GUI event loop
root.mainloop()
