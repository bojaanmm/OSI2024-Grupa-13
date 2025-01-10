import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import json

# Funkcija za spremanje broja parking mesta
def save_parking_spots():
    try:
        total_spots = int(entry_parking_spots.get())
        try:
            with open("parking_administration.json", "r") as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {
                "total_parking_spots": 0,
                "occupied_spots": 0,
                "price_per_hour": 0.0,
                "price_per_day": 0.0,
                "holidays": []
            }

        data["total_parking_spots"] = total_spots

        with open("parking_administration.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        messagebox.showinfo("Uspjeh", "Podaci o parking mjestima su uspješno sačuvani!")
    except ValueError:
        messagebox.showerror("Greška", "Molimo unesite validan broj za parking mjesta.")

# Funkcija za unos tarifa
def open_tariff_window():
    def save_tariffs():
        try:
            price_per_hour = entry_price_per_hour.get()
            price_per_day = entry_price_per_day.get()

            if price_per_hour and price_per_day:
                price_per_hour = float(price_per_hour)
                price_per_day = float(price_per_day)
                if price_per_hour <= 0 or price_per_day <= 0:
                    raise ValueError("Cijene moraju biti pozitivni brojevi.")
                data["price_per_hour"] = price_per_hour
                data["price_per_day"] = price_per_day
            else:
                messagebox.showinfo("Uspjeh", "Praznici su uspješno sačuvani bez promjene tarifa.")

            data["holidays"] = selected_holidays

            with open("parking_administration.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            messagebox.showinfo("Uspjeh", "Praznici su uspješno sačuvani!")
        except ValueError:
            messagebox.showerror("Greška", "Molimo unesite validne brojeve za tarife.")

    def add_holiday():
        selected_date = calendar.get_date()
        if selected_date not in selected_holidays:
            selected_holidays.append(selected_date)
            update_holiday_list()

    def update_holiday_list():
        holidays_text.set("\n".join(selected_holidays))

    def remove_holiday():
        selected_date = calendar.get_date()
        if selected_date in selected_holidays:
            selected_holidays.remove(selected_date)
            update_holiday_list()

    def generate_monthly_report():
        try:
            with open("mjesecni_izvjestaj.json", "r") as f:
                monthly_report = json.load(f)
            with open("mjesecni_izvjestaj.txt", "w") as f:
                f.write(f"Ukupni prihod: {monthly_report['total_revenue']} KM\n")
                f.write(f"Ukupno vozila: {monthly_report['total_vehicles']}\n\n")
                f.write("Detalji transakcija:\n")
                for transaction in monthly_report['transactions']:
                    f.write(f"Datum: {transaction['date']}, Iznos: {transaction['revenue']} KM\n")
            messagebox.showinfo("Izvještaj", "Mesečni izveštaj je uspješno generisan!")
        except FileNotFoundError:
            messagebox.showerror("Greška", "Mesečni izveštaj nije pronađen!")
        except Exception as e:
            messagebox.showerror("Greška", f"Došlo je do greške: {e}")

    try:
        with open("parking_administration.json", "r") as json_file:
            data = json.load(json_file)
        selected_holidays = data.get("holidays", [])
    except FileNotFoundError:
        selected_holidays = []

    tariff_window = tk.Toplevel(root)
    tariff_window.title("Unos tarifa")
    tariff_window.geometry("500x900")

    tk.Label(tariff_window, text="Cijena po satu (KM):").pack(pady=5)
    entry_price_per_hour = tk.Entry(tariff_window)
    entry_price_per_hour.pack(pady=5)

    tk.Label(tariff_window, text="Cijena po danu (KM):").pack(pady=5)
    entry_price_per_day = tk.Entry(tariff_window)
    entry_price_per_day.pack(pady=5)

    tk.Label(tariff_window, text="Odaberite praznične dane:").pack(pady=10)
    calendar = Calendar(tariff_window, selectmode="day", date_pattern="yyyy-MM-dd")
    calendar.pack(pady=10)

    tk.Button(tariff_window, text="Dodaj praznik", command=add_holiday).pack(pady=5)
    tk.Button(tariff_window, text="Ukloni praznik", command=remove_holiday).pack(pady=5)

    holidays_text = tk.StringVar()
    tk.Label(tariff_window, text="Praznici:").pack(pady=5)
    tk.Label(tariff_window, textvariable=holidays_text, justify="left").pack(pady=5)

    tk.Button(tariff_window, text="Spremi sve podatke", command=save_tariffs).pack(pady=20)
    tk.Button(tariff_window, text="Ispiši mesečni izveštaj", command=generate_monthly_report).pack(pady=10)

    update_holiday_list()

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
root.iconphoto(False, tk.PhotoImage(file="parking.png"))
root.config(bg="#A9CFE8")

frame_parking_spots = tk.Frame(root)
frame_parking_spots.pack(pady=10)
tk.Label(frame_parking_spots, text="Unesite broj ukupnih parking mjesta:").pack(side=tk.LEFT, padx=5)
entry_parking_spots = tk.Entry(frame_parking_spots)
entry_parking_spots.pack(side=tk.LEFT, padx=5)
tk.Button(frame_parking_spots, text="Spremi", command=save_parking_spots).pack(side=tk.LEFT, padx=10)

frame_password = tk.Frame(root)
frame_password.pack(pady=20)
tk.Label(frame_password, text="Unesite admin šifru za unos tarifa:").pack(side=tk.LEFT, padx=5)
entry_password = tk.Entry(frame_password, show="*")
entry_password.pack(side=tk.LEFT, padx=5)
tk.Button(frame_password, text="Pristupi", command=check_password).pack(side=tk.LEFT, padx=10)

label_parked_vehicles_title = tk.Label(root, text="Parkirana vozila:", font=("Arial", 12, "bold"))
label_parked_vehicles_title.pack(pady=10)
label_parked_vehicles = tk.Label(root, text="", justify=tk.LEFT, font=("Arial", 10))
label_parked_vehicles.pack()

display_parked_vehicles()
root.mainloop()
