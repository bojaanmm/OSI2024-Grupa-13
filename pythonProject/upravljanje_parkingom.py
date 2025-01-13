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


def save_tariffs():
    try:
        # Učitaj podatke iz fajla parking_administration.json
        try:
            with open("parking_administration.json", "r") as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Ako fajl nije pronađen, inicijalizuj data sa podrazumevanom strukturom
            data = {
                "total_parking_spots": 0,
                "occupied_spots": 0,
                "price_per_hour": 0.0,
                "price_per_day": 0.0,
                "holidays": []
            }

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


# Funkcija za spremanje praznika u fajl
def save_holidays():
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

    data["holidays"] = selected_holidays

    with open("parking_administration.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    messagebox.showinfo("Uspjeh", "Praznici su uspješno sačuvani!")


# Funkcija za prikaz podataka o parkiranim vozilima u novom prozoru
def show_parked_vehicles_window():
    vehicles_window = tk.Toplevel(root)
    vehicles_window.title("Parkirana vozila")
    vehicles_window.geometry("500x400")

    try:
        with open("parking_data.json", "r") as f:
            parked_vehicles = json.load(f)

        if parked_vehicles:
            vehicles_text = "Parkirana vozila:\n"
            for vehicle in parked_vehicles:
                vehicles_text += f"Reg. oznaka: {vehicle['reg_oznaka']}, Vrijeme: {vehicle['vrijeme']}, Kod: {vehicle['kod']}\n"
        else:
            vehicles_text = "Nema parkiranih vozila."

        vehicles_label = tk.Label(vehicles_window, text=vehicles_text, justify="left", width=60, height=10)
        vehicles_label.pack(pady=20)
    except FileNotFoundError:
        messagebox.showerror("Greška", "Fajl parking_data.json nije pronađen!")


def get_transactions_last_24_hours():
    try:
        with open("izvjestaj.json", "r") as f:
            report_data = json.load(f)
        transactions = report_data["transactions"]
        now = datetime.now()
        twenty_four_hours_ago = now - timedelta(hours=24)

        recent_transactions = [
            transaction for transaction in transactions
            if datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S") > twenty_four_hours_ago
        ]

        return recent_transactions
    except FileNotFoundError:
        messagebox.showerror("Greška", "Izvještaj nije pronađen!")
        return []


def get_transactions_last_7_days():
    try:
        with open("izvjestaj.json", "r") as f:
            report_data = json.load(f)
        transactions = report_data["transactions"]
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)

        recent_transactions = [
            transaction for transaction in transactions
            if datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S") > seven_days_ago
        ]

        return recent_transactions
    except FileNotFoundError:
        messagebox.showerror("Greška", "Izvještaj nije pronađen!")
        return []


def get_transactions_last_30_days():
    try:
        with open("izvjestaj.json", "r") as f:
            report_data = json.load(f)
        transactions = report_data["transactions"]
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)

        recent_transactions = [
            transaction for transaction in transactions
            if datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S") > thirty_days_ago
        ]

        return recent_transactions
    except FileNotFoundError:
        messagebox.showerror("Greška", "Izvještaj nije pronađen!")
        return []


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

        with open("izvjestaj_24h.txt", "w") as file:
            file.write(report_text)

        messagebox.showinfo("Izvještaj", "Izvještaj za poslednjih 24h je sačuvan u izvjestaj_24h.txt")
    else:
        report_label.config(text="Nema podataka za poslednjih 24h.")


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

        with open("izvjestaj_7d.txt", "w") as file:
            file.write(report_text)

        messagebox.showinfo("Izvještaj", "Izvještaj za poslednjih 7 dana je sačuvan u izvjestaj_7d.txt")
    else:
        report_label.config(text="Nema podataka za poslednjih 7 dana.")


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

        with open("izvjestaj_30d.txt", "w") as file:
            file.write(report_text)

        messagebox.showinfo("Izvještaj", "Izvještaj za poslednjih 30 dana je sačuvan u izvjestaj_30d.txt")
    else:
        report_label.config(text="Nema podataka za poslednjih 30 dana.")


def open_tariff_window():
    if entry_password.get() == "admin123":
        tariff_window = tk.Toplevel(root)
        tariff_window.title("Izveštaj")
        tariff_window.geometry("300x200")

        tk.Button(tariff_window, text="Prikaz izveštaja za poslednjih 24h", command=generate_24h_report).pack(pady=10)
        tk.Button(tariff_window, text="Prikaz izveštaja za poslednjih 7 dana", command=generate_7d_report).pack(pady=10)
        tk.Button(tariff_window, text="Prikaz izveštaja za poslednjih 30 dana", command=generate_30d_report).pack(pady=10)

        global report_label
        report_label = tk.Label(tariff_window, text="", justify="left")
        report_label.pack(pady=20)
    else:
        messagebox.showerror("Greška", "Neispravna lozinka!")


root = tk.Tk()
root.title("Sistem za naplatu parkinga")
root.geometry("600x750")

selected_holidays = []

# Frame za unos broja parking mjesta
frame_parking_spots = tk.Frame(root)
frame_parking_spots.pack(pady=10, fill="x")
frame_parking_spots_label = tk.Label(frame_parking_spots, text="Unesite broj parking mjesta:")
frame_parking_spots_label.pack(side="left", padx=5)
entry_parking_spots = tk.Entry(frame_parking_spots)
entry_parking_spots.pack(side="left", padx=5)
tk.Button(frame_parking_spots, text="Spremi parking mjesta", command=save_parking_spots).pack(side="left", padx=5)

# Frame za unos tarifa
frame_tariffs = tk.LabelFrame(root, text="Tarife", padx=10, pady=10)
frame_tariffs.pack(pady=10, fill="x")

tk.Label(frame_tariffs, text="Cijena po satu:").grid(row=0, column=0, padx=5, sticky="w")
entry_price_per_hour = tk.Entry(frame_tariffs)
entry_price_per_hour.grid(row=0, column=1, padx=5)

tk.Label(frame_tariffs, text="Cijena po danu:").grid(row=0, column=2, padx=5, sticky="w")
entry_price_per_day = tk.Entry(frame_tariffs)
entry_price_per_day.grid(row=0, column=3, padx=5)

tk.Button(frame_tariffs, text="Spremi tarife", command=save_tariffs).grid(row=0, column=4, padx=10)

# Frame za praznike
frame_holidays = tk.LabelFrame(root, text="Praznici", padx=10, pady=10)
frame_holidays.pack(pady=10, fill="x")

calendar = Calendar(frame_holidays, selectmode="day", date_pattern="yyyy-mm-dd")
calendar.grid(row=0, column=0, padx=5)

tk.Button(frame_holidays, text="Dodaj praznik", command=add_holiday).grid(row=0, column=1, padx=5)
tk.Button(frame_holidays, text="Ukloni praznik", command=remove_holiday).grid(row=0, column=2, padx=5)

holidays_label = tk.Label(root, text="Praznici:")
holidays_label.pack(pady=5)
holidays_text = tk.StringVar()
holidays_label = tk.Label(root, textvariable=holidays_text, justify="left")
holidays_label.pack(pady=5)

update_holiday_list()

tk.Button(root, text="Spremi praznike", command=save_holidays).pack(pady=10)

# Unos lozinke i dugme za prikaz tarifnih izvještaja
frame_password = tk.LabelFrame(root, text="Lozinka za tarifne izvještaje", padx=10, pady=10)
frame_password.pack(pady=20, fill="x")

tk.Label(frame_password, text="Unesite lozinku:").pack(side="left", padx=5)
entry_password = tk.Entry(frame_password, show="*")
entry_password.pack(side="left", padx=5)

# Dugme za prikaz tarifnih izvještaja
tk.Button(frame_password, text="Potvrdi", command=open_tariff_window).pack(side="left", padx=5)

# Dugme za prikaz parkiranih vozila
tk.Button(root, text="Prikaz parkiranih vozila", command=show_parked_vehicles_window).pack(pady=10)

root.mainloop()
