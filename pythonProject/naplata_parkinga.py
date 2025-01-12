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
    receipt_filename = f"parking_ticket_{code}.txt"
    with open(receipt_filename, "w", encoding="utf-8") as file:
        # Kreiranje sadržaja računa u tekstualnom obliku
        file.write("Račun za parkiranje\n")
        file.write("=====================\n")
        file.write(f"Registarska oznaka: {reg_oznaka}\n")
        file.write(f"Vrijeme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Jedinstveni kod: {code}\n")
        file.write(f"Ukupno plaćeno: {total_cost} KM\n")
        file.write(f"Način plaćanja: {payment_method}\n")
        file.write(f"Status: Plaćeno\n")
        file.write("=====================\n")
        file.write("Hvala na korištenju našeg sistema!\n")

# Funkcija za upisivanje transakcije u ukupni izvještaj
def update_report(total_cost, reg_oznaka, code, payment_method):
    today = datetime.now()

    # Pročitaj postojeći izvještaj
    try:
        with open('izvjestaj.json', 'r') as f:
            report = json.load(f)
    except FileNotFoundError:
        report = {"total_revenue": 0, "total_vehicles": 0, "transactions": []}

    # Dodaj novu transakciju
    transaction = {
        "date": today.strftime('%Y-%m-%d %H:%M:%S'),
        "revenue": total_cost,
        "reg_oznaka": reg_oznaka,
        "code": code,
        "payment_method": payment_method
    }
    report["transactions"].append(transaction)

    # Ažuriraj ukupni prihod i broj vozila
    report["total_revenue"] += total_cost
    report["total_vehicles"] += 1

    # Upisivanje ažuriranog izvještaja
    with open('izvjestaj.json', 'w') as f:
        json.dump(report, f, indent=4)


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

        # Ažuriraj ukupni izvještaj
        update_report(total_cost, reg_oznaka, code, payment_method)

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
