import os
import json
import requests
import ipaddress


# Legt den Dateinamen für die gespeicherten Kurse fest
RATES_FILE = "exchange_rates.json"
# Die Adresse der API für die Wechselkurse
API_URL = "https://api.frankfurter.app/latest?from=EUR"
# Erlaubt die Eingabe von gängigen Namen statt der offiziellen Kürzel
COMMON_CURRENCIES = {
    "euro": "EUR", "dollar": "USD", "pfund": "GBP", "yen": "JPY", "franken": "CHF"
}

# Leert das Terminal (funktioniert für Windows, Mac und Linux)
def clear_screen():
    os.system('cls') if os.name == 'nt' else os.system('clear')

# Taschenrechner Funktionen

# Führt die gewählte Rechenoperation aus
def calculate(num1, num2, choice):
    if choice == '1': return num1 + num2
    if choice == '2': return num1 - num2
    if choice == '3': return num1 * num2
    if choice == '4':
        if num2 == 0: return "Fehler: Division durch Null ist nicht erlaubt."
        return num1 / num2

# Taschenrechner-Teil des Programms
def run_calculator():
    while True:
        clear_screen()
        print("--- Taschenrechner ---")
        print("1. Addieren (+)\n2. Subtrahieren (-)\n3. Multiplizieren (*)\n4. Dividieren (/)\n5. Zurück zum Hauptmenü")
        choice = input("\nWähle eine Rechenart: ")
        if choice == '5': break
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Gib die erste Zahl ein: ").replace(',', '.'))
                num2 = float(input("Gib die zweite Zahl ein: ").replace(',', '.'))
                result = calculate(num1, num2, choice)
                print(f"\nDas Ergebnis ist: {result}")
            except ValueError:
                print("\nFehler: Bitte gib gültige Zahlen ein.")
            input("\nDrücke Enter, um fortzufahren...")
        else:
            print("\nUngültige Eingabe.")
            input("Drücke Enter, um es erneut zu versuchen...")

# IP-Rechner Funktionen

# IP-Rechner-Teil des Programms
def run_ip_calculator():
    while True:
        clear_screen()
        print("--- IP-Rechner ---")
        print("Gib eine IP-Adresse mit Subnetzmaske ein (z.B. 192.168.1.50/24).")
        print("Oder tippe 'exit', um zum Hauptmenü zurückzukehren.")
        user_input = input("\nEingabe: ")
        if user_input.lower() == 'exit': break
        try:
            # strict=False erlaubt auch Host-Adressen statt nur Netz-Adressen
            network = ipaddress.ip_network(user_input, strict=False)
            print("\n--- Ergebnisse ---")
            print(f"Netzwerkadresse: {network.network_address}")
            print(f"Broadcast-Adresse: {network.broadcast_address}")
            if network.prefixlen >= 31:
                print("Anzahl der nutzbaren Host-Adressen: 0")
            else:
                hosts = list(network.hosts())
                print(f"Anzahl der nutzbaren Host-Adressen: {len(hosts)}")
                print(f"Erste nutzbare Host-Adresse: {hosts[0]}")
                print(f"Letzte nutzbare Host-Adresse: {hosts[-1]}")
            ip_addr = ipaddress.ip_address(user_input.split('/')[0])
            print(f"Ist die IP privat? {'Ja' if ip_addr.is_private else 'Nein'}")
        except ValueError:
            print("\nFehler: Ungültige Eingabe. Bitte gib eine gültige IP-Adresse im CIDR-Format ein.")
        input("\nDrücke Enter, um eine neue Berechnung zu starten...")

# API und Daten-Management (Währungsrechner)

# Holt die neuesten Wechselkurse von der Frankfurter API
def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        # Gibt einen Fehler, wenn die Seite nicht erreichbar ist (Error-404 etc.)
        response.raise_for_status()
        data = response.json()
        if data and "rates" in data and "date" in data:
            rates = data.get("rates")
            # Fügt EUR zur Liste hinzu, da es nicht in der API enthalten ist
            rates['EUR'] = 1.0
            return {"date": data.get("date"), "rates": rates}
        else:
            print("Fehler: Ungültige oder unvollständige Daten in der API-Antwort.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler beim Abrufen der Wechselkurse: {e}")
        return None
    except json.JSONDecodeError:
        print("Fehler: Konnte die API-Antwort nicht als JSON dekodieren.")
        return None

# Speichert die Wechselkursdaten in einer JSON-Datei
def save_rates(rates_data):
    try:
        with open(RATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(rates_data, f, indent=4)
        return True
    except IOError as e:
        print(f"Fehler beim Speichern der Wechselkurse: {e}")
        return False

# Lädt die Wechselkursdaten aus der JSON-Datei
def load_rates():
    if not os.path.exists(RATES_FILE):
        return None
    try:
        with open(RATES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Fehler beim Laden oder Lesen der Wechselkursdatei.")
        return None

# Prüft, ob die lokal gespeicherten Kurse aktuell sind
def are_rates_up_to_date(local_rates_data):
    if not local_rates_data or "date" not in local_rates_data:
        return False
    print("Prüfe, ob die lokalen Kurse aktuell sind...")
    latest_api_data = get_exchange_rates()
    if not latest_api_data:
        print("Warnung: Konnte API nicht erreichen, um Datum zu prüfen. Verwende lokale Daten.")
        return True
    local_date = local_rates_data.get("date")
    latest_api_date = latest_api_data.get("date")
    print(f"Datum der lokalen Datei: {local_date}")
    print(f"Datum der neuesten API-Kurse: {latest_api_date}")
    return local_date == latest_api_date

# Währungsrechner Funktionen

# Lädt Kurse oder holt neue von der API
def update_and_load_rates():
    rates_data = load_rates()
    if not rates_data or not are_rates_up_to_date(rates_data):
        print("Wechselkurse sind nicht aktuell oder nicht vorhanden. Lade neue Kurse...")
        new_rates_data = get_exchange_rates()
        if new_rates_data:
            save_rates(new_rates_data)
            print("Neue Wechselkurse erfolgreich gespeichert.")
            return new_rates_data
        else:
            print("Fehler: Konnte keine neuen Wechselkurse abrufen.")
            return rates_data
    else:
        print("Aktuelle Wechselkurse erfolgreich aus lokaler Datei geladen.")
        return rates_data

# Rechnet einen Betrag um
def convert_currency(amount, from_input, to_input, rates_data):
    rates = rates_data.get("rates")
    if not rates:
        print("\nFehler: Keine Wechselkurse verfügbar.")
        return None, from_input, to_input
    from_currency = COMMON_CURRENCIES.get(from_input.lower(), from_input.upper())
    to_currency = COMMON_CURRENCIES.get(to_input.lower(), to_input.upper())
    if from_currency not in rates or to_currency not in rates:
        print("\nFehler: Eine der Währungen wurde nicht gefunden.")
        return None, from_input, to_input
    try:
        amount_in_eur = amount / rates[from_currency]
        converted_amount = amount_in_eur * rates[to_currency]
        return converted_amount, from_currency, to_currency
    except Exception as e:
        print(f"\nFehler bei der Umrechnung: {e}")
        return None, from_currency, to_currency

# Zeigt verfügbare Währungen an
def display_available_currencies(rates_data):
    if rates_data and "rates" in rates_data:
        currencies = sorted(rates_data["rates"].keys())
        print("\n--- Verfügbare Währungen ---")
        col_width = max(len(c) for c in currencies) + 4
        num_cols = 80 // col_width
        for i, currency in enumerate(currencies):
            print(f"{currency:{col_width}}", end="")
            if (i + 1) % num_cols == 0: print()
        print("\n")
    else:
        print("\nKeine Währungen verfügbar.")

# Steuert den Währungsrechner-Teil
def run_currency_converter():
    clear_screen()
    print("Lade Währungsrechner...")
    current_rates_data = update_and_load_rates()
    if not current_rates_data:
        print("\nStart des Währungsrechners fehlgeschlagen. Keine Kursdaten verfügbar.")
        input("\nDrücke Enter, um zum Hauptmenü zurückzukehren...")
        return
    while True:
        clear_screen()
        print("--- Währungsrechner ---")
        print("1. Währung umrechnen\n2. Wechselkurse manuell aktualisieren\n3. Verfügbare Währungen anzeigen\n4. Zurück zum Hauptmenü")
        choice = input("\nIhre Wahl: ")
        if choice == '1':
            try:
                amount = float(input("Betrag (z.B. 10,50): ").replace(',', '.'))
                from_input = input("Von Währung (z.B. Euro): ")
                to_input = input("Nach Währung (z.B. Dollar): ")
                result, from_code, to_code = convert_currency(amount, from_input, to_input, current_rates_data)
                if result is not None:
                    print(f"\nErgebnis: {amount:.2f} {from_code} sind {result:.2f} {to_code}")
            except Exception as e:
                print(f"\nFehler bei der Eingabe: {e}")
            input("\nDrücke Enter, um fortzufahren...")
        elif choice == '2':
            new_rates = get_exchange_rates()
            if new_rates:
                save_rates(new_rates)
                current_rates_data = new_rates
                print("\nWechselkurse wurden manuell aktualisiert.")
            else:
                print("\nFehler beim Aktualisieren.")
            input("\nDrücke Enter, um fortzufahren...")
        elif choice == '3':
            display_available_currencies(current_rates_data)
            input("\nDrücke Enter, um fortzufahren...")
        elif choice == '4':
            break
        else:
            print("\nUngültige Eingabe.")
            input("Drücke Enter, um es erneut zu versuchen...")

# Hauptprogramm

def main():
    while True:
        clear_screen()
        print("- Willkommen beim Multifunktionstaschenrechner -")
        print("\nBitte wählen Sie ein Werkzeug:")
        print("1. Normaler Taschenrechner\n2. Währungsrechner\n3. IP-Rechner\n4. Programm beenden")
        choice = input("\nIhre Wahl: ")
        if choice == '1': run_calculator()
        elif choice == '2': run_currency_converter()
        elif choice == '3': run_ip_calculator()
        elif choice == '4':
            clear_screen()
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        else:
            print("\nUngültige Eingabe.")
            input("Drücke Enter, um es erneut zu versuchen...")

# Stellt sicher, dass main() nur ausgeführt wird, wenn die Datei direkt gestartet wird
if __name__ == "__main__":
    main()