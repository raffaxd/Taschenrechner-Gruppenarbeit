import json
import os
# Wir importieren die Funktion, um die neuesten Kurse direkt von der API zu holen
from api_client import get_exchange_rates

RATES_FILE = "exchange_rates.json"

# Speichert die Wechselkursdaten in einer JSON-Datei.
def save_rates(rates_data):
    try:
        with open(RATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(rates_data, f, indent=4)
        return True
    except IOError as e:
        print(f"Fehler beim Speichern der Wechselkurse: {e}")
        return False

# Lädt die Wechselkursdaten aus einer JSON-Datei.
# Gibt das Dictionary mit den Kursen zurück oder None, wenn die Datei nicht existiert oder leer ist.
def load_rates():
    if not os.path.exists(RATES_FILE):
        return None
    try:
        with open(RATES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Fehler beim Laden oder Lesen der Wechselkursdatei: {e}")
        return None

# Prüft, ob die lokal gespeicherten Kurse mit den neuesten von der API verfügbaren Kursen übereinstimmen.
def are_rates_up_to_date(local_rates_data):
    if not local_rates_data or "date" not in local_rates_data:
        return False
    
    print("Prüfe, ob die lokalen Kurse aktuell sind...")
    # Hole die neuesten Kursdaten von der API, um das aktuelle Datum zu bekommen
    latest_api_data = get_exchange_rates()

    if not latest_api_data:
        # Wenn die API nicht erreichbar ist, können wir nicht prüfen.
        # Wir nehmen an, die lokalen Daten sind "gut genug".
        print("Warnung: Konnte die neuesten Kurse von der API nicht abrufen, um das Datum zu vergleichen.")
        return True

    local_date = local_rates_data.get("date")
    latest_api_date = latest_api_data.get("date")

    print(f"Datum der lokalen Datei: {local_date}")
    print(f"Datum der neuesten API-Kurse: {latest_api_date}")

    # Vergleiche das Datum der lokalen Datei mit dem Datum der neuesten API-Daten
    return local_date == latest_api_date

if __name__ == "__main__":
    # Beispielaufrufe, um die neue Logik zu testen
    
    print("--- Testfall 1: Lade lokale Daten und prüfe, ob sie aktuell sind ---")
    local_data = load_rates()
    if local_data:
        if are_rates_up_to_date(local_data):
            print("\nErgebnis: Die lokalen Kurse sind aktuell.")
        else:
            print("\nErgebnis: Die lokalen Kurse sind veraltet.")
    else:
        print("Keine lokalen Kursdaten gefunden.")

    print("\n--- Testfall 2: Speichere veraltete Testdaten und prüfe erneut ---")
    # Simuliere veraltete Daten
    old_rates = {
        "date": "2020-01-01",
        "rates": {"EUR": 1.0, "USD": 1.1}
    }
    save_rates(old_rates)
    
    # Lade die gerade gespeicherten alten Daten
    old_local_data = load_rates()
    if old_local_data:
        if are_rates_up_to_date(old_local_data):
            print("\nErgebnis: Die (alten) lokalen Kurse sind aktuell. (Sollte nicht passieren)")
        else:
            print("\nErgebnis: Die (alten) lokalen Kurse sind veraltet. (Erwartet)")
    else:
        print("Konnte die alten Testdaten nicht laden.")
