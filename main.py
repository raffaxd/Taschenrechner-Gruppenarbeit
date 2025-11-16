import sys
import os
from api_client import get_exchange_rates
# Wir ändern den Import, um die neue Funktion zu verwenden
from data_manager import load_rates, save_rates, are_rates_up_to_date

# Stellt sicher, dass das aktuelle Verzeichnis im Python-Pfad ist,
# damit die Module gefunden werden, wenn main.py direkt ausgeführt wird.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Wörterbuch für gängige Währungsnamen
COMMON_CURRENCIES = {
    "euro": "EUR",
    "euros": "EUR",
    "dollar": "USD",
    "dollars": "USD",
    "us dollar": "USD",
    "us dollars": "USD",
    "usd": "USD",
    "pfund": "GBP",
    "gbp": "GBP",
    "yen": "JPY",
    "jpy": "JPY",
    "franken": "CHF",
    "chf": "CHF",
    "kanadischer dollar": "CAD",
    "cad": "CAD",
    "australischer dollar": "AUD",
    "aud": "AUD",
    "chinesischer yuan": "CNY",
    "cny": "CNY",
    "indische rupie": "INR",
    "inr": "INR",
    "brasilianischer real": "BRL",
    "brl": "BRL",
    "russischer rubel": "RUB",
    "rub": "RUB",
    "mexikanischer peso": "MXN",
    "mxn": "MXN",
    "südafrikanischer rand": "ZAR",
    "zar": "ZAR",
}

# Leert den Terminal-Bildschirm, plattformunabhängig
def clear_screen():
    os.system('cls') if os.name == 'nt' else os.system('clear')

# Versucht, Wechselkurse zu laden. Wenn sie nicht aktuell sind oder nicht existieren,
# werden neue von der API abgerufen und gespeichert.
def update_and_load_rates():
    rates_data = load_rates()

    # Wir verwenden hier die neue, korrekte Prüffunktion
    if not rates_data or not are_rates_up_to_date(rates_data):
        print("Lokale Wechselkurse sind nicht aktuell oder nicht vorhanden. Versuche, neue abzurufen...")
        new_rates_data = get_exchange_rates()
        if new_rates_data:
            if save_rates(new_rates_data):
                print("Neue Wechselkurse erfolgreich abgerufen und gespeichert.")
                return new_rates_data
            else:
                print("Fehler: Konnte neue Wechselkurse nicht speichern.")
                # Wenn das Speichern fehlschlägt, aber wir alte Daten haben, nutzen wir diese
                return rates_data if rates_data else None
        else:
            print("Fehler: Konnte keine neuen Wechselkurse von der API abrufen.")
            if rates_data: # Wenn alte Kurse vorhanden sind, diese verwenden
                print("Verwende vorhandene (möglicherweise veraltete) lokale Wechselkurse.")
                return rates_data
            return None
    else:
        print("Aktuelle Wechselkurse erfolgreich aus lokaler Datei geladen.")
        return rates_data

# Rechnet einen Betrag von einer Quellwährung in eine Zielwährung um.
# Die Basiswährung der Kurse ist EUR.
def convert_currency(amount, from_currency_input, to_currency_input, rates_data):
    rates = rates_data.get("rates")
    if not rates:
        print("Fehler: Keine Wechselkurse verfügbar.")
        return None

    # Versuche, die Währungscodes zu normalisieren
    from_currency = COMMON_CURRENCIES.get(from_currency_input.lower(), from_currency_input.upper())
    to_currency = COMMON_CURRENCIES.get(to_currency_input.lower(), to_currency_input.upper())

    if from_currency not in rates:
        print(f"Fehler: Quellwährung '{from_currency_input}' (versucht als '{from_currency}') nicht gefunden.")
        print("Bitte überprüfen Sie die Schreibweise oder wählen Sie Option 3 im Hauptmenü, um alle verfügbaren Währungen zu sehen.")
        return None, None, None # Geben jetzt auch die Währungen zurück
    if to_currency not in rates:
        print(f"Fehler: Zielwährung '{to_currency_input}' (versucht als '{to_currency}') nicht gefunden.")
        print("Bitte überprüfen Sie die Schreibweise oder wählen Sie Option 3 im Hauptmenü, um alle verfügbaren Währungen zu sehen.")
        return None, None, None # Geben jetzt auch die Währungen zurück

    try:
        # Umrechnung über EUR als Basis
        amount_in_eur = amount / rates[from_currency]
        converted_amount = amount_in_eur * rates[to_currency]
        return converted_amount, from_currency, to_currency
    except ZeroDivisionError:
        print("Fehler: Wechselkurs der Quellwährung ist Null.")
        return None, from_currency, to_currency
    except Exception as e:
        print(f"Ein unerwarteter Fehler bei der Umrechnung ist aufgetreten: {e}")
        return None, from_currency, to_currency

# Zeigt die verfügbaren Währungen formatiert in Spalten an.
def display_available_currencies(rates_data):
    if rates_data and "rates" in rates_data:
        currencies = sorted(rates_data["rates"].keys())
        print("\n--- Verfügbare Währungen ---")
        
        col_width = max(len(c) for c in currencies) + 4
        num_cols = 80 // col_width
        
        for i, currency in enumerate(currencies):
            print(f"{currency:{col_width}}", end="")
            if (i + 1) % num_cols == 0:
                print()
        print("\n")
    else:
        print("Keine Währungen verfügbar.")

def main():
    clear_screen()
    print("Willkommen beim Währungsrechner!")
    current_rates_data = update_and_load_rates()

    if not current_rates_data:
        print("\nDas Programm kann ohne Wechselkurse nicht gestartet werden.")
        print("Bitte überprüfen Sie Ihre Internetverbindung oder die API.")
        input("\nDrücken Sie Enter, um das Programm zu beenden.")
        return
    
    input("\nDrücken Sie Enter, um zum Hauptmenü zu gelangen...")

    while True:
        clear_screen()
        print("--- Hauptmenü ---")
        print("1. Währung umrechnen")
        print("2. Wechselkurse jetzt aktualisieren")
        print("3. Verfügbare Währungen anzeigen")
        print("4. Beenden")

        choice = input("\nIhre Wahl: ")

        if choice == '1':
            clear_screen()
            print("--- Währung umrechnen ---")
            try:
                amount_str = input("Betrag (z.B. 10.50 oder 10,50): ")
                amount = float(amount_str.replace(',', '.'))
                from_currency_input = input("Von Währung (z.B. EUR oder Euro): ")
                to_currency_input = input("Nach Währung (z.B. USD oder Dollar): ")

                result, from_code, to_code = convert_currency(amount, from_currency_input, to_currency_input, current_rates_data)
                if result is not None:
                    print(f"\nErgebnis: {amount:.2f} {from_code} sind {result:.2f} {to_code}")
            except ValueError:
                print("\nFehler: Ungültiger Betrag. Bitte geben Sie eine Zahl ein.")
            except Exception as e:
                print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}")
            
            input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")

        elif choice == '2':
            clear_screen()
            print("--- Wechselkurse manuell aktualisieren ---")
            # Hier erzwingen wir ein Neuladen, indem wir die Prüfung überspringen
            new_rates = get_exchange_rates()
            if new_rates:
                save_rates(new_rates)
                current_rates_data = new_rates
                print("Wechselkurse wurden erfolgreich manuell aktualisiert.")
            else:
                print("Fehler: Konnte keine neuen Wechselkurse von der API abrufen.")
            
            input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        
        elif choice == '3':
            clear_screen()
            display_available_currencies(current_rates_data)
            input("Drücken Sie Enter, um zum Menü zurückzukehren...")

        elif choice == '4':
            clear_screen()
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        else:
            print("\nUngültige Eingabe. Bitte wählen Sie eine Option von 1 bis 4.")
            input("Drücken Sie Enter, um es erneut zu versuchen...")

if __name__ == "__main__":
    main()
