import tkinter as tk
import json
import random
import string
from datetime import datetime

# Kreiranje glavnog prozora
root = tk.Tk()
root.title("Ulaz i izlaz")
root.geometry("400x300")  # Širina x Visina

# Postavljanje ikone prozora
root.iconphoto(False, tk.PhotoImage(file="parking.png"))

# Promjena boje pozadine prozora na neutralno plavu
root.config(bg="#A9CFE8")  # Ovdje možete promijeniti boju

# Funkcija za generisanje nasumičnog jedinstvenog koda
def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Funkcija za učitavanje postojećih podataka iz JSON fajla
def load_parking_data():
    try:
        with open("parking_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Funkcija za prikaz greške u novom prozoru
def show_error(message):
    error_window = tk.Toplevel(root)
    error_window.title("Greška")
    error_window.geometry("300x150")
    error_label = tk.Label(error_window, text=message, fg="red", bg="#A9CFE8")  # Pozadina greške prozora
    error_label.pack(pady=20)
    close_button = tk.Button(error_window, text="Zatvori", command=error_window.destroy, bg="#A9CFE8")
    close_button.pack(pady=10)

# Funkcija za rukovanje unosom registarskih oznaka
def handle_input():
    reg_oznaka = entry.get()
    if reg_oznaka:
        # Učitavanje postojećih podataka
        parking_data = load_parking_data()

        # Provjera da li su registarske oznake već unijete
        for record in parking_data:
            if record["reg_oznaka"] == reg_oznaka:
                show_error(f"Registarska oznaka {reg_oznaka} već postoji u evidenciji.")
                entry.delete(0, tk.END)
                return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unique_code = generate_unique_code()
        data = {"reg_oznaka": reg_oznaka, "vrijeme": current_time, "kod": unique_code}

        # Dodavanje novih podataka
        parking_data.append(data)

        # Upis u .json fajl
        with open("parking_data.json", "w") as file:
            json.dump(parking_data, file, indent=4)

        # Kreiranje .txt fajla sa informacijama
        with open(f"parking_ticket_{unique_code}.txt", "w") as txt_file:
            txt_file.write(f"Registarska oznaka: {reg_oznaka}\n")
            txt_file.write(f"Vrijeme: {current_time}\n")
            txt_file.write(f"Jedinstveni kod: {unique_code}\n")

        print(f"Unesena registarska oznaka: {reg_oznaka}, Vrijeme: {current_time}, Kod: {unique_code}")
        entry.delete(0, tk.END)

# Dodavanje labela za unos registarskih oznaka
label = tk.Label(root, text="Unesite registarsku oznaku:", bg="#A9CFE8")
label.pack(pady=10)

# Dodavanje polja za unos
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Dodavanje dugmeta za potvrdu
button = tk.Button(root, text="Potvrdi", command=handle_input)
button.pack(pady=10)

# Pokretanje glavne petlje
root.mainloop()
