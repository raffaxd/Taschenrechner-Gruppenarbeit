import requests
import json

# Die URL für die neuesten Kurse mit Euro als Basis
API_URL = "https://api.frankfurter.app/latest?from=EUR"

# Ruft die neuesten Wechselkurse von der Frankfurter API (EZB-Daten) ab.
# Gibt ein Dictionary mit den Kursen (Basis EUR) und dem Datum zurück.
# Gibt None bei einem Fehler zurück.
def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Löst einen HTTPError für schlechte Antworten (4xx oder 5xx) aus

        data = response.json()
        
        if data and "rates" in data and "date" in data:
            rates = data.get("rates")
            date = data.get("date")
            
            # Füge EUR als Basiswährung mit Kurs 1.0 hinzu, da die API es nicht explizit enthält
            rates['EUR'] = 1.0
            return {"date": date, "rates": rates}
        else:
            print("Fehler: Ungültige oder unvollständige Daten in der API-Antwort.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler beim Abrufen der Wechselkurse: {e}")
        return None
    except json.JSONDecodeError:
        print("Fehler: Konnte die API-Antwort nicht als JSON dekodieren.")
        return None
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None

if __name__ == "__main__":
    # Beispielaufruf, wenn api_client.py direkt ausgeführt wird
    print("Versuche, die neuesten Wechselkurse abzurufen...")
    rates_data = get_exchange_rates()
    if rates_data:
        print("\nErfolgreich Wechselkurse abgerufen:")
        print(f"Datum der Kurse: {rates_data['date']}")
        print("Kurse (Auszug):")
        
        # Nur ein paar Kurse ausgeben, um die Ausgabe nicht zu überfluten
        counter = 0
        for currency, rate in rates_data['rates'].items():
            if counter < 5:
                print(f"  {currency}: {rate}")
                counter += 1
            else:
                break
    else:
        print("\nKonnte keine Wechselkurse abrufen.")