Mein Währungsrechner für die Gruppenarbeit
 
Es ist ein einfacher Währungsrechner, der im Terminal läuft.

Das Programm kann sich die aktuellsten Wechselkurse aus dem Internet ziehen und damit dann Beträge umrechnen. Man kann entweder die offiziellen Kürzel (wie EUR, USD) oder auch einfach die Namen (wie Euro, Dollar) eingeben.

Die Daten für die Kurse kommen von der Frankfurter App API.

Wie man es startet

Python: Du brauchst Python auf deinem Rechner, damit du das Skript ausführen kannst.

Bibliotheken installieren: Damit das Programm die Daten aus dem Internet laden kann, muss man eine kleine Bibliothek namens  requests  installieren. Am einfachsten geht das, wenn du im Projektordner diesen Befehl im Terminal eingibst: pip install -r requirements.txt

Programm starten: Danach kannst du das Programm einfach mit diesem Befehl starten: python main.py. Das Menü erklärt sich dann eigentlich von selbst.

Aufbau vom Projekt

Ich habe versucht, den Code ein bisschen aufzuteilen, damit es übersichtlich bleibt:

main.py : Das ist die Hauptdatei, die man startet. Hier ist das Menü und die ganze Logik drin, die alles zusammenhält.
api_client.py : Dieses Skript holt die Daten aus dem Internet von der API.
data_manager.py : Das hier kümmert sich um das Speichern und Laden der Kurse. Die werden in der  exchange_rates.json  zwischengespeichert.
requirements.txt : Hier steht nur drin, welche Bibliotheken man für das Projekt braucht (in dem Fall nur  requests).
exchange_rates.json : In dieser Datei werden die Kurse gespeichert, damit man sie nicht bei jedem Start neu aus dem Internet laden muss.
