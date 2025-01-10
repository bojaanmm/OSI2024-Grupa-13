import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Funkcija za učitavanje podataka iz parking_data.json
def load_parking_data():
    with open('parking_data.json', 'r') as f:
        return json.load(f)

# Funkcija za učitavanje tarife iz parking_administration.json
def load_parking_administration():
    with open('parking_administration.json', 'r') as f:
        return json.load(f)

# Funkcija za brisanje vozila iz parking_data.json
def remove_vehicle_from_parking_data(code):
    parking_data = load_parking_data()
    parking_data = [data for data in parking_data if data["kod"] != code]
    with open('parking_data.json', 'w') as f:
        json.dump(parking_data, f, indent=4)

# Funkcija za ažuriranje broja zauzetih mesta u parking_administration.json
def update_parking_administration():
    parking_administration = load_parking_administration()
    parking_administration["occupied_spots"] -= 1
    with open('parking_administration.json', 'w') as f:
        json.dump(parking_administration, f, indent=4)

# Funkcija za izračunavanje vremena parkiranja i cene
# Funkcija za izračunavanje vremena parkiranja i cene (uzimajući u obzir praznike)
def calculate_parking_time_and_cost(entry_time_str, code, price_per_hour, price_per_day, holidays):
    entry_time = datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()

    # Razlika u vremenu
    parking_duration = current_time - entry_time

    # Ukupni broj sati (uključujući delimične sate)
    hours = (parking_duration.total_seconds() + 3600 - 1) // 3600  # Dodato je 3600-1 kako bi se zaokružilo na sledeći sat

    # Prvo računamo dane, zatim sate
    days = hours // 24

    # Pretvaranje praznika u datetime objekte za poređenje
    holiday_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in holidays]

    # Provera da li je parking obuhvatio praznični dan
    for day_offset in range(int(days) + 1):
        day_to_check = (entry_time + timedelta(days=day_offset)).date()
        if day_to_check in holiday_dates:
            return 0  # Parkiranje je besplatno na praznike

    # Računanje ukupne cene (sati ili dani)
    if days > 0:
        total_cost = days * price_per_day
    else:
        total_cost = hours * price_per_hour  # Za svaki započeti sat

    return total_cost


# Funkcija za generisanje računa
def generate_receipt(reg_oznaka, code, payment_method, total_cost):
    receipt_filename = f"receipt_{code}.txt"  # Korišćenje koda za naziv fajla
    with open(receipt_filename, "w", encoding="utf-8") as file:
        file.write(f"Reg. Oznaka: {reg_oznaka}\n")
        file.write(f"Plaćeno putem koda: {code}\n")  # Dodato ispod reg. oznake
        file.write(f"Ukupno plaćeno: {total_cost} KM\n")
        file.write(f"Način plačanja: {payment_method}\n")

# Funkcija za upisivanje transakcije u mjesecni izvještaj
def update_monthly_report(total_cost):
    today = datetime.now()
    one_month_ago = today - timedelta(days=30)

    # Pročitaj postojeći izvještaj
    try:
        with open('mjesecni_izvjestaj.json', 'r') as f:
            monthly_report = json.load(f)
    except FileNotFoundError:
        monthly_report = {"total_revenue": 0, "total_vehicles": 0, "transactions": []}

    # Dodaj novu transakciju
    transaction = {
        "date": today.strftime('%Y-%m-%d %H:%M:%S'),
        "revenue": total_cost
    }
    monthly_report["transactions"].append(transaction)

    # Ažuriraj ukupni prihod i broj vozila
    monthly_report["total_revenue"] += total_cost
    monthly_report["total_vehicles"] += 1

    # Očisti stare transakcije (koje su starije od mesec dana)
    monthly_report["transactions"] = [t for t in monthly_report["transactions"] if datetime.strptime(t["date"], '%Y-%m-%d %H:%M:%S') > one_month_ago]

    # Upisivanje ažuriranog izvještaja
    with open('mjesecni_izvjestaj.json', 'w') as f:
        json.dump(monthly_report, f, indent=4)

# GUI za unos koda i plaćanje
def on_submit():
    code = entry_code.get()

    # Pronađi korisničke podatke u parking_data.json
    parking_data = load_parking_data()
    parking_administration = load_parking_administration()

    found = False
    for data in parking_data:
        if data["kod"] == code:
            found = True
            reg_oznaka = data["reg_oznaka"]
            entry_time_str = data["vrijeme"]
            break

    if not found:
        messagebox.showerror("Greška", "Kod nije pronađen!")
        return

    # Učitaj praznike iz administrativnih podataka
    holidays = parking_administration.get("holidays", [])

    # Izračunaj cenu parkiranja
    total_cost = calculate_parking_time_and_cost(
        entry_time_str,
        code,
        parking_administration["price_per_hour"],
        parking_administration["price_per_day"],
        holidays
    )

    # Prikazivanje prozora sa informacijama
    def on_payment(payment_method):
        # Generiši račun i ažuriraj podatke
        generate_receipt(reg_oznaka, code, payment_method, total_cost)

        # Ažuriranje podataka nakon plaćanja
        remove_vehicle_from_parking_data(code)
        update_parking_administration()

        # Ažuriraj mesečni izveštaj
        update_monthly_report(total_cost)

        # Zatvori prozor za plaćanje
        payment_window.destroy()

        # Prikazivanje potvrde
        messagebox.showinfo("Račun",
                            f"Račun je generisan!\nUkupno plaćeno: {total_cost} KM\nNačin plaćanja: {payment_method}")

    # Prozor za izbor načina plaćanja
    payment_window = tk.Toplevel(window)
    payment_window.title("Izbor plaćanja")
    payment_window.geometry("200x120")

    label = tk.Label(payment_window, text=f"Ukupna cijena: {total_cost} KM")
    label.pack(pady=10)

    button_cash = tk.Button(payment_window, text="Gotovina", command=lambda: on_payment("Gotovina"))
    button_cash.pack(pady=5)

    button_card = tk.Button(payment_window, text="Kartica", command=lambda: on_payment("Kartica"))
    button_card.pack(pady=5)


# Glavni prozor za unos koda
window = tk.Tk()
window.title("Naplata Parkinga")
window.geometry("300x150")  # Postavljanje minimalne veličine prozora

# Promjena boje pozadine prozora na neutralno plavu
window.config(bg="#A9CFE8")

# Postavljanje ikone prozora
window.iconphoto(False, tk.PhotoImage(file="parking.png"))

label = tk.Label(window, text="Unesite kod:")
label.pack(pady=10)

# Polje za unos koda
entry_code = tk.Entry(window)
entry_code.pack(pady=10)

button_submit = tk.Button(window, text="Unesi", command=on_submit)
button_submit.pack(pady=10)

window.mainloop()
