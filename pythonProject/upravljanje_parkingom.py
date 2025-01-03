import tkinter as tk
from tkinter import messagebox
import json


# Funkcija za spremanje broja parking mjesta i tarife u JSON fajl
def save_parking_spots():
    try:
        # Dohvatanje unosa i provjera da li je cijeli broj za broj parking mjesta
        total_spots = int(entry_parking_spots.get())

        # Dohvatanje unosa za cijenu po satu i po danu, te provjera da li su validni brojevi
        price_per_hour = float(entry_price_per_hour.get())
        price_per_day = float(entry_price_per_day.get())

        # Pokušaj učitavanja postojećeg fajla
        try:
            with open("parking_administration.json", "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}

        # Dodavanje novih podataka u postojeći sadržaj
        data.update({
            "total_parking_spots": total_spots,
            "price_per_hour": price_per_hour,
            "price_per_day": price_per_day
        })

        # Spremanje podataka u JSON fajl
        with open("parking_administration.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        # Poruka o uspjehu
        messagebox.showinfo("Uspjeh", "Podaci o parking mjestima i tarifi su uspješno sačuvani!")
    except ValueError:
        # Poruka o grešci ako unos nije validan
        messagebox.showerror("Greška", "Molimo unesite validan broj za parking mjesta i tarife.")


# Kreiranje glavnog prozora
root = tk.Tk()
root.title("Upravljanje parkingom")
root.geometry("600x300")  # Širina x Visina

# Frame za postavljanje elemenata u vertikalnom redu
frame = tk.Frame(root)
frame.pack(pady=20)

# Frame za unos broja parking mjesta
frame_parking_spots = tk.Frame(frame)
frame_parking_spots.pack(pady=5)
label_parking_spots = tk.Label(frame_parking_spots, text="Unesite broj ukupnih parking mjesta:")
label_parking_spots.pack(side=tk.LEFT, padx=5)
entry_parking_spots = tk.Entry(frame_parking_spots)
entry_parking_spots.pack(side=tk.LEFT, padx=5)

# Frame za unos cijene po satu
frame_price_per_hour = tk.Frame(frame)
frame_price_per_hour.pack(pady=5)
label_price_per_hour = tk.Label(frame_price_per_hour, text="Unesite cijenu po satu (KM):")
label_price_per_hour.pack(side=tk.LEFT, padx=5)
entry_price_per_hour = tk.Entry(frame_price_per_hour)
entry_price_per_hour.pack(side=tk.LEFT, padx=5)

# Frame za unos cijene po danu
frame_price_per_day = tk.Frame(frame)
frame_price_per_day.pack(pady=5)
label_price_per_day = tk.Label(frame_price_per_day, text="Unesite cijenu po danu (KM):")
label_price_per_day.pack(side=tk.LEFT, padx=5)
entry_price_per_day = tk.Entry(frame_price_per_day)
entry_price_per_day.pack(side=tk.LEFT, padx=5)

# Dugme za spremanje podataka
button_save = tk.Button(frame, text="Spremi", command=save_parking_spots)
button_save.pack(pady=10)

# Pokretanje glavne petlje
root.mainloop()
