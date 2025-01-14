import tkinter as tk
import json
import random
import string
from datetime import datetime, timedelta
from tkinter import messagebox

# Kreiranje glavnog prozora
root = tk.Tk()
root.title("Ulaz i izlaz")
root.geometry("400x300")  # Širina x Visina

# Postavljanje ikone prozora
root.iconphoto(False, tk.PhotoImage(file="parking.png"))

# Promjena boje pozadine prozora na neutralno plavu
root.config(bg="#A9CFE8")

# Funkcija za generisanje nasumičnog jedinstvenog koda
def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Funkcija za učitavanje podataka iz JSON fajla
def load_parking_data():
    try:
        with open("parking_administration.json", "r") as file:
            data = json.load(file)
            # Osiguravanje da svi potrebni ključevi postoje
            if "total_parking_spots" not in data:
                data["total_parking_spots"] = 10
            if "occupied_spots" not in data:
                data["occupied_spots"] = 0
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"total_parking_spots": 10, "occupied_spots": 0}  # Defaultni podaci
        save_parking_data(data)
        return data

# Funkcija za ažuriranje podataka u JSON fajlu
def save_parking_data(data):
    with open("parking_administration.json", "w") as file:
        json.dump(data, file, indent=4)

# Funkcija za ažuriranje prikaza slobodnih mjesta
def update_free_spots():
    data = load_parking_data()
    total_spots = data.get("total_parking_spots", 0)
    occupied_spots = data.get("occupied_spots", 0)
    free_spots = total_spots - occupied_spots
    label_free_spots.config(text=f"Slobodna mjesta: {free_spots}")

# Funkcija za rukovanje unosom registarskih oznaka
def handle_input():
    reg_oznaka = entry.get()
    if reg_oznaka:
        # Provjera da li je registarska oznaka VIP korisnik
        try:
            with open("vip_users.json", "r") as vip_file:
                vip_users = json.load(vip_file)
        except (FileNotFoundError, json.JSONDecodeError):
            vip_users = []

        if reg_oznaka in vip_users:
            messagebox.showinfo("VIP Korisnik", f"Hvala na korištenju naših VIP usluga. Dobrodošli!")
            entry.delete(0, tk.END)
            return

        # Učitavanje postojećih podataka
        data = load_parking_data()

        if data["occupied_spots"] >= data["total_parking_spots"]:
            messagebox.showwarning("Upozorenje", "Nema slobodnih mjesta!")
            entry.delete(0, tk.END)
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unique_code = generate_unique_code()
        parking_record = {"reg_oznaka": reg_oznaka, "vrijeme": current_time, "kod": unique_code}

        # Dodavanje zauzetog mjesta
        data["occupied_spots"] += 1
        save_parking_data(data)

        # Dodavanje novog vozila u parking_data.json
        try:
            with open("parking_data.json", "r") as json_file:
                parked_vehicles = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            parked_vehicles = []

        # Dodavanje nove evidencije u listu
        parked_vehicles.append(parking_record)

        # Spremanje ažurirane liste u fajl
        with open("parking_data.json", "w") as json_file:
            json.dump(parked_vehicles, json_file, indent=4)

        # Kreiranje .txt fajla sa informacijama
        with open(f"parking_ticket_{unique_code}.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write("Račun za parkiranje\n")
            txt_file.write("=====================\n")
            txt_file.write(f"Registarska oznaka: {reg_oznaka}\n")
            txt_file.write(f"Vrijeme: {current_time}\n")
            txt_file.write(f"Jedinstveni kod: {unique_code}\n")
            txt_file.write(f"Status: Nije plaćeno\n")
            txt_file.write("=====================\n")
            txt_file.write("Hvala na korištenju našeg sistema!\n")

        # Prikaz poruke o uspjehu
        messagebox.showinfo("Uspjeh", f"Unos registarskih oznaka '{reg_oznaka}' je uspješno zabilježen!")

        print(f"Unesena registarska oznaka: {reg_oznaka}, Vrijeme: {current_time}, Kod: {unique_code}")
        update_free_spots()
        entry.delete(0, tk.END)

# Funkcija za provjeru statusa izlaza
def handle_exit():
    reg_oznaka = exit.get()
    if not reg_oznaka:
        messagebox.showwarning("Upozorenje", "Molimo unesite registarsku oznaku za izlaz!")
        return

    try:
        # Učitavanje izvještaja
        with open("izvjestaj.json", "r") as file:
            report_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Greška", "Fajl 'izvjestaj.json' nije pronađen ili je oštećen.")
        return

    # Provjera da li je registarska oznaka VIP korisnik
    try:
        with open("vip_users.json", "r") as vip_file:
            vip_users = json.load(vip_file)
    except (FileNotFoundError, json.JSONDecodeError):
        vip_users = []

    if reg_oznaka in vip_users:
        messagebox.showinfo("VIP Korisnik", f"Hvala na korištenju naših VIP usluga, doviđenja!")
        # Oslobađanje zauzetog mjesta
        data = load_parking_data()
        if data["occupied_spots"] > 0:
            data["occupied_spots"] -= 1
            save_parking_data(data)
            update_free_spots()
        exit.delete(0, tk.END)
        return

    # Trenutno vrijeme
    now = datetime.now()

    # Filtriranje transakcija unutar posljednjih 15 minuta
    recent_transactions = [
        transaction for transaction in report_data.get("transactions", [])
        if transaction["reg_oznaka"] == reg_oznaka and
           now - datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S") <= timedelta(minutes=15)
    ]

    if recent_transactions:
        # Provjeravanje plaćanja
        if any(tx["revenue"] > 0 for tx in recent_transactions):
            messagebox.showinfo("Uspjeh",
                                f"Parking za vozilo registarskih oznaka '{reg_oznaka}' je plaćen. Možete izaći.")

            # Oslobađanje zauzetog mjesta
            data = load_parking_data()
            if data["occupied_spots"] > 0:
                data["occupied_spots"] -= 1
                save_parking_data(data)
                update_free_spots()

            exit.delete(0, tk.END)
        else:
            messagebox.showwarning("Upozorenje", f"Parking za vozilo registarskih oznaka '{reg_oznaka}' nije plaćen!")
    else:
        # Ako je vrijeme od 15 minuta isteklo, tretirati kao novi ulaz
        data = load_parking_data()
        if data["occupied_spots"] >= data["total_parking_spots"]:
            messagebox.showwarning("Upozorenje", "Nema slobodnih mjesta za ponovni ulaz!")
            exit.delete(0, tk.END)
            return

        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        unique_code = generate_unique_code()
        parking_record = {"reg_oznaka": reg_oznaka, "vrijeme": current_time, "kod": unique_code}

        # Dodavanje zauzetog mjesta
        data["occupied_spots"] += 1
        save_parking_data(data)

        # Dodavanje nove evidencije u parking_data.json
        try:
            with open("parking_data.json", "r") as json_file:
                parked_vehicles = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            parked_vehicles = []

        parked_vehicles.append(parking_record)

        with open("parking_data.json", "w") as json_file:
            json.dump(parked_vehicles, json_file, indent=4)

        # Poruka korisniku
        messagebox.showinfo("Obavijest",
                            f"Vozilo s registarskom oznakom '{reg_oznaka}' tretirano je kao novi ulaz na parking.")

        print(f"Unesena registarska oznaka: {reg_oznaka}, Vrijeme: {current_time}, Kod: {unique_code}")
        update_free_spots()
        exit.delete(0, tk.END)

# Funkcija za ažuriranje prikaza cjenovnika
def update_price_list():
    data = load_parking_data()
    price_per_hour = data.get("price_per_hour", 0)
    price_per_day = data.get("price_per_day", 0)
    label_price_list.config(text=f"Cijena po satu: {price_per_hour} KM\nCijena po danu: {price_per_day} KM")

# Dodavanje oznake za prikaz cjenovnika
label_price_list = tk.Label(root, text="", bg="#A9CFE8", justify="center")
label_price_list.pack(pady=10)

# Ažuriranje prikaza cjenovnika
update_price_list()


# Dodavanje labela za unos registarskih oznaka
label = tk.Label(root, text="Unesite registarsku oznaku za ulaz:", bg="#A9CFE8")
label.pack(pady=5)

# Polje za unos registarskih oznaka
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Dugme za potvrdu
button = tk.Button(root, text="Ulaz", command=handle_input)
button.pack(pady=5)

label = tk.Label(root, text="Unesite registarsku oznaku za izlaz:", bg="#A9CFE8")
label.pack(pady=5)

# Polje za unos registarskih oznaka
exit = tk.Entry(root, width=30)
exit.pack(pady=5)

# Dugme za potvrdu
buttonExit = tk.Button(root, text="Izlaz", command=handle_exit)
buttonExit.pack(pady=5)

# Oznaka za prikaz slobodnih mjesta
label_free_spots = tk.Label(root, text="Slobodna mjesta: 0", bg="#A9CFE8")
label_free_spots.pack(pady=10)

# Učitavanje početnih podataka i ažuriranje prikaza
update_free_spots()

# Pokretanje glavne petlje
root.mainloop()
