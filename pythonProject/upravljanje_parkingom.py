import tkinter as tk
from tkinter import messagebox
import json


# Funkcija za spremanje broja parking mesta
def save_parking_spots():
    try:
        total_spots = int(entry_parking_spots.get())
        try:
            with open("parking_administration.json", "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}

        data.update({"total_parking_spots": total_spots})
        with open("parking_administration.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        messagebox.showinfo("Uspjeh", "Podaci o parking mjestima su uspješno sačuvani!")
    except ValueError:
        messagebox.showerror("Greška", "Molimo unesite validan broj za parking mjesta.")


# Funkcija za unos tarifa
def open_tariff_window():
    def save_tariffs():
        try:
            price_per_hour = float(entry_price_per_hour.get())
            price_per_day = float(entry_price_per_day.get())
            if price_per_hour <= 0 or price_per_day <= 0:
                raise ValueError("Cijene moraju biti pozitivni brojevi.")
            try:
                with open("parking_administration.json", "r") as json_file:
                    data = json.load(json_file)
            except FileNotFoundError:
                data = {}

            data.update({"price_per_hour": price_per_hour, "price_per_day": price_per_day})
            with open("parking_administration.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            messagebox.showinfo("Uspjeh", "Tarife su uspješno sačuvane!")
            tariff_window.destroy()
        except ValueError:
            messagebox.showerror("Greška", "Molimo unesite validne brojeve za tarife.")

    # Funkcija za generisanje mesečnog izveštaja u .txt fajl
    def generate_monthly_report():
        try:
            with open("mjesecni_izvjestaj.json", "r") as f:
                monthly_report = json.load(f)

            # Kreiranje i upisivanje u fajl
            with open("mjesecni_izvjestaj.txt", "w") as f:
                f.write(f"Ukupni prihod: {monthly_report['total_revenue']} KM\n")
                f.write(f"Ukupno vozila: {monthly_report['total_vehicles']}\n\n")
                f.write("Detalji transakcija:\n")
                for transaction in monthly_report['transactions']:
                    f.write(f"Datum: {transaction['date']}, Iznos: {transaction['revenue']} KM\n")

            messagebox.showinfo("Izvještaj", "Mesečni izveštaj je uspešno generisan!")
        except FileNotFoundError:
            messagebox.showerror("Greška", "Mesečni izveštaj nije pronađen!")
        except Exception as e:
            messagebox.showerror("Greška", f"Došlo je do greške: {e}")

    tariff_window = tk.Toplevel(root)
    tariff_window.title("Unos tarifa")
    tariff_window.geometry("400x300")
    tk.Label(tariff_window, text="Cijena po satu (KM):").pack(pady=5)
    entry_price_per_hour = tk.Entry(tariff_window)
    entry_price_per_hour.pack(pady=5)
    tk.Label(tariff_window, text="Cijena po danu (KM):").pack(pady=5)
    entry_price_per_day = tk.Entry(tariff_window)
    entry_price_per_day.pack(pady=5)
    tk.Button(tariff_window, text="Spremi tarife", command=save_tariffs).pack(pady=10)

    # Dodavanje dugmeta za ispis mesečnog izveštaja u `tariff_window`
    tk.Button(tariff_window, text="Ispisi mesečni izveštaj", command=generate_monthly_report).pack(pady=10)


# Funkcija za provjeru šifre
def check_password():
    password = entry_password.get()
    if password == "admin123":
        open_tariff_window()
    else:
        messagebox.showerror("Greška", "Pogrešna šifra. Pristup zabranjen.")


# Funkcija za prikaz parkiranih vozila
def display_parked_vehicles():
    try:
        with open("parking_data.json", "r") as json_file:
            data = json.load(json_file)
        if isinstance(data, list):
            vehicles_text = "".join(
                [f"Registracija: {vehicle['reg_oznaka']}, Vrijeme: {vehicle['vrijeme']}, Kod: {vehicle['kod']}\n" for
                 vehicle in data]
            )
        else:
            vehicles_text = "Podaci nisu u očekivanom formatu."
        if not vehicles_text.strip():
            vehicles_text = "Nema parkiranih vozila."
        label_parked_vehicles.config(text=vehicles_text)
    except FileNotFoundError:
        label_parked_vehicles.config(text="Podaci o parkiranim vozilima nisu pronađeni.")
    except Exception as e:
        label_parked_vehicles.config(text=f"Greška pri čitanju podataka: {e}")
    root.after(1000, display_parked_vehicles)


# Kreiranje glavnog prozora
root = tk.Tk()
root.title("Upravljanje parkingom")
root.geometry("600x500")

# Frame za unos broja parking mjesta
frame_parking_spots = tk.Frame(root)
frame_parking_spots.pack(pady=10)
tk.Label(frame_parking_spots, text="Unesite broj ukupnih parking mjesta:").pack(side=tk.LEFT, padx=5)
entry_parking_spots = tk.Entry(frame_parking_spots)
entry_parking_spots.pack(side=tk.LEFT, padx=5)
tk.Button(frame_parking_spots, text="Spremi", command=save_parking_spots).pack(side=tk.LEFT, padx=10)

# Frame za unos šifre za administraciju
frame_password = tk.Frame(root)
frame_password.pack(pady=20)
tk.Label(frame_password, text="Unesite admin šifru za unos tarifa:").pack(side=tk.LEFT, padx=5)
entry_password = tk.Entry(frame_password, show="*")
entry_password.pack(side=tk.LEFT, padx=5)
tk.Button(frame_password, text="Pristupi", command=check_password).pack(side=tk.LEFT, padx=10)

# Label za prikaz parkiranih vozila
label_parked_vehicles_title = tk.Label(root, text="Parkirana vozila:", font=("Arial", 12, "bold"))
label_parked_vehicles_title.pack(pady=10)
label_parked_vehicles = tk.Label(root, text="", justify=tk.LEFT, font=("Arial", 10))
label_parked_vehicles.pack()

# Pokretanje funkcije za prikaz parkiranih vozila
display_parked_vehicles()

# Pokretanje glavne petlje
root.mainloop()
