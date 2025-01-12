import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import json
from datetime import datetime, timedelta


# Funkcija za spremanje broja parking mjesta
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


# Funkcija za unos tarifa i praznika
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

        data["holidays"] = selected_holidays

        with open("parking_administration.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        messagebox.showinfo("Uspjeh", "Podaci su uspješno sačuvani!")
    except ValueError:
        messagebox.showerror("Greška", "Molimo unesite validne brojeve za tarife.")


# Funkcije za upravljanje praznicima
def add_holiday():
    selected_date = calendar.get_date()
    if selected_date not in selected_holidays:
        selected_holidays.append(selected_date)
        update_holiday_list()


def remove_holiday():
    selected_date = calendar.get_date()
    if selected_date in selected_holidays:
        selected_holidays.remove(selected_date)
        update_holiday_list()


def update_holiday_list():
    holidays_text.set("\n".join(selected_holidays))

# Funkcija za prikaz podataka o parkiranim vozilima u novom prozoru
def show_parked_vehicles_window():
    # Kreiramo novi prozor
    vehicles_window = tk.Toplevel(root)
    vehicles_window.title("Parkirana vozila")
    vehicles_window.geometry("500x400")

    try:
        # Učitavamo podatke o parkiranim vozilima
        with open("parking_data.json", "r") as f:
            parked_vehicles = json.load(f)

        if parked_vehicles:
            vehicles_text = "Parkirana vozila:\n"
            for vehicle in parked_vehicles:
                vehicles_text += f"Reg. oznaka: {vehicle['reg_oznaka']}, Vrijeme: {vehicle['vrijeme']}, Kod: {vehicle['kod']}\n"
        else:
            vehicles_text = "Nema parkiranih vozila."

        # Labela za prikazivanje podataka
        vehicles_label = tk.Label(vehicles_window, text=vehicles_text, justify="left", width=60, height=10)
        vehicles_label.pack(pady=20)
    except FileNotFoundError:
        messagebox.showerror("Greška", "Fajl parking_data.json nije pronađen!")



# Funkcija za filtriranje transakcija za poslednjih 24h
def get_transactions_last_24_hours():
    try:
        with open("izvjestaj.json", "r") as f:
            report_data = json.load(f)
        transactions = report_data["transactions"]
        now = datetime.now()
        twenty_four_hours_ago = now - timedelta(hours=24)

        # Filtriranje transakcija za poslednjih 24h
        recent_transactions = [
            transaction for transaction in transactions
            if datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S") > twenty_four_hours_ago
        ]

        return recent_transactions
    except FileNotFoundError:
        messagebox.showerror("Greška", "Izvještaj nije pronađen!")
        return []


# Funkcija za filtriranje transakcija za poslednjih 7 dana
def get_transactions_last_7_days():
    try:
        with open("izvjestaj.json", "r") as f:
            report_data = json.load(f)
        transactions = report_data["transactions"]
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)

        # Filtriranje transakcija za poslednjih 7 dana
        recent_transactions = [
            transaction for transaction in transactions
            if datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S") > seven_days_ago
        ]

        return recent_transactions
    except FileNotFoundError:
        messagebox.showerror("Greška", "Izvještaj nije pronađen!")
        return []


# Funkcija za filtriranje transakcija za poslednjih 30 dana
def get_transactions_last_30_days():
    try:
        with open("izvjestaj.json", "r") as f:
            report_data = json.load(f)
        transactions = report_data["transactions"]
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)

        # Filtriranje transakcija za poslednjih 30 dana
        recent_transactions = [
            transaction for transaction in transactions
            if datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S") > thirty_days_ago
        ]

        return recent_transactions
    except FileNotFoundError:
        messagebox.showerror("Greška", "Izvještaj nije pronađen!")
        return []


# Funkcija za generisanje izveštaja za poslednjih 24h i čuvanje u txt fajlu
def generate_24h_report():
    transactions = get_transactions_last_24_hours()
    if transactions:
        total_revenue = sum(transaction["revenue"] for transaction in transactions)
        total_vehicles = len(transactions)
        report_text = f"Ukupni prihod za poslednjih 24h: {total_revenue} KM\n"
        report_text += f"Ukupno vozila: {total_vehicles}\n\nDetalji transakcija:\n"
        for transaction in transactions:
            report_text += f"Datum: {transaction['date']}, Iznos: {transaction['revenue']} KM\n"

        report_label.config(text=report_text)

        # Snimanje u TXT fajl
        with open("izvjestaj_24h.txt", "w") as file:
            file.write(report_text)

        messagebox.showinfo("Izvještaj", "Izvještaj za poslednjih 24h je sačuvan u izvjestaj_24h.txt")
    else:
        report_label.config(text="Nema podataka za poslednjih 24h.")


# Funkcija za generisanje izveštaja za poslednjih 7 dana i čuvanje u txt fajlu
def generate_7d_report():
    transactions = get_transactions_last_7_days()
    if transactions:
        total_revenue = sum(transaction["revenue"] for transaction in transactions)
        total_vehicles = len(transactions)
        report_text = f"Ukupni prihod za poslednjih 7 dana: {total_revenue} KM\n"
        report_text += f"Ukupno vozila: {total_vehicles}\n\nDetalji transakcija:\n"
        for transaction in transactions:
            report_text += f"Datum: {transaction['date']}, Iznos: {transaction['revenue']} KM\n"

        report_label.config(text=report_text)

        # Snimanje u TXT fajl
        with open("izvjestaj_7d.txt", "w") as file:
            file.write(report_text)

        messagebox.showinfo("Izvještaj", "Izvještaj za poslednjih 7 dana je sačuvan u izvjestaj_7d.txt")
    else:
        report_label.config(text="Nema podataka za poslednjih 7 dana.")


# Funkcija za generisanje izveštaja za poslednjih 30 dana i čuvanje u txt fajlu
def generate_30d_report():
    transactions = get_transactions_last_30_days()
    if transactions:
        total_revenue = sum(transaction["revenue"] for transaction in transactions)
        total_vehicles = len(transactions)
        report_text = f"Ukupni prihod za poslednjih 30 dana: {total_revenue} KM\n"
        report_text += f"Ukupno vozila: {total_vehicles}\n\nDetalji transakcija:\n"
        for transaction in transactions:
            report_text += f"Datum: {transaction['date']}, Iznos: {transaction['revenue']} KM\n"

        report_label.config(text=report_text)

        # Snimanje u TXT fajl
        with open("izvjestaj_30d.txt", "w") as file:
            file.write(report_text)

        messagebox.showinfo("Izvještaj", "Izvještaj za poslednjih 30 dana je sačuvan u izvjestaj_30d.txt")
    else:
        report_label.config(text="Nema podataka za poslednjih 30 dana.")


# Funkcija za otvaranje prozora za izveštaje
def open_tariff_window():
    if entry_password.get() == "admin123":
        tariff_window = tk.Toplevel(root)
        tariff_window.title("Izveštaj")
        tariff_window.geometry("500x400")

        # Dugmadi za generisanje izveštaja
        tk.Button(tariff_window, text="Prikaz izveštaja za poslednjih 24h", command=generate_24h_report).pack(pady=10)
        tk.Button(tariff_window, text="Prikaz izveštaja za poslednjih 7 dana", command=generate_7d_report).pack(pady=10)
        tk.Button(tariff_window, text="Prikaz izveštaja za poslednjih 30 dana", command=generate_30d_report).pack(
            pady=10)

        global report_label
        report_label = tk.Label(tariff_window, text="", justify="left", width=50, height=15)
        report_label.pack(pady=20)
    else:
        messagebox.showerror("Greška", "Pogrešna šifra. Pristup zabranjen.")


# Kreiranje glavnog prozora
root = tk.Tk()
root.title("Upravljanje parkingom")
root.geometry("600x700")
root.iconphoto(False, tk.PhotoImage(file="parking.png"))
root.config(bg="#A9CFE8")

# Učitavanje podataka iz datoteke
try:
    with open("parking_administration.json", "r") as json_file:
        data = json.load(json_file)
    selected_holidays = data.get("holidays", [])
except FileNotFoundError:
    data = {}
    selected_holidays = []

# Sekcija za broj parking mesta
frame_parking_spots = tk.Frame(root, bg="#A9CFE8")
frame_parking_spots.pack(pady=10)
tk.Label(frame_parking_spots, text="Unesite broj ukupnih parking mjesta:", bg="#A9CFE8").pack(side=tk.LEFT, padx=5)
entry_parking_spots = tk.Entry(frame_parking_spots)
entry_parking_spots.pack(side=tk.LEFT, padx=5)
tk.Button(frame_parking_spots, text="Spremi", command=save_parking_spots).pack(side=tk.LEFT, padx=10)

# Sekcija za unos tarifa
tk.Label(root, text="Cijena po satu (KM):", bg="#A9CFE8").pack(pady=5)
entry_price_per_hour = tk.Entry(root)
entry_price_per_hour.pack(pady=5)

tk.Label(root, text="Cijena po danu (KM):", bg="#A9CFE8").pack(pady=5)
entry_price_per_day = tk.Entry(root)
entry_price_per_day.pack(pady=5)

tk.Button(root, text="Spremi tarife", command=save_tariffs).pack(pady=10)

# Sekcija za praznike
calendar = Calendar(root)
calendar.pack(pady=20)

tk.Button(root, text="Dodaj praznik", command=add_holiday).pack(pady=5)
tk.Button(root, text="Ukloni praznik", command=remove_holiday).pack(pady=5)

holidays_text = tk.StringVar()
holidays_label = tk.Label(root, textvariable=holidays_text, bg="#A9CFE8")
holidays_label.pack(pady=10)

# Sekcija za prikaz parkiranih vozila
tk.Button(root, text="Prikaz parkiranih vozila", command=show_parked_vehicles_window).pack(pady=10)

# Sekcija za pristup izveštajima
frame_password = tk.Frame(root, bg="#A9CFE8")
frame_password.pack(pady=20)
tk.Label(frame_password, text="Unesite admin šifru:", bg="#A9CFE8").pack(side=tk.LEFT, padx=5)
entry_password = tk.Entry(frame_password, show="*")
entry_password.pack(side=tk.LEFT, padx=5)
tk.Button(frame_password, text="Pristupi", command=open_tariff_window).pack(side=tk.LEFT, padx=10)

root.mainloop()
