# Multifunktionstaschenrechner

Dieses Projekt ist eine befehlszeilenbasierte Multi-Tool-Anwendung, die in Python geschrieben wurde. Es bietet eine Sammlung nützlicher Rechner, die über ein Hauptmenü zugänglich sind.

## Funktionen

*   **Standard-Taschenrechner:** Führt grundlegende arithmetische Operationen wie Addition, Subtraktion, Multiplikation und Division aus.
*   **Währungsrechner:** Ruft die neuesten Wechselkurse von der Frankfurter.app-API ab, um zwischen verschiedenen Währungen umzurechnen. Die Kurse werden lokal zwischengespeichert, um die Anzahl der API-Aufrufe zu minimieren.
*   **IP-Rechner:** Berechnet Netzwerkinformationen (Netzwerkadresse, Broadcast-Adresse, nutzbare Hosts usw.) aus einer gegebenen IP-Adresse und Subnetzmaske im CIDR-Format.

## Technologien

*   **Python 3:** Die Kernprogrammiersprache.
*   **requests:** Eine Python-Bibliothek zur Durchführung von HTTP-Anfragen an die Währungs-API.

## Architektur

Die Anwendung ist in einer einzigen Datei (`main.py`) strukturiert, die die gesamte Logik enthält:

*   **`main.py`**: Dient als Einstiegspunkt der Anwendung. Die Datei enthält das Hauptmenü zur Auswahl der Werkzeuge sowie die vollständige Implementierung des Taschenrechners, des Währungsrechners und des IP-Rechners. Sie verwaltet auch die API-Aufrufe zum Abrufen von Wechselkursen und deren lokale Speicherung.

## Installation und Ausführung

### 1. Voraussetzungen

*   Stellen Sie sicher, dass Python 3 auf Ihrem System installiert ist.

### 2. Installation der Abhängigkeiten

Navigieren Sie zum Projektverzeichnis und installieren Sie die erforderlichen Pakete mit dem folgenden Befehl:

```bash
pip install -r requirements.txt
```

### 3. Starten der Anwendung

Um die Anwendung zu starten, führen Sie das Hauptskript aus:

```bash
python main.py
```

Anschließend wird ein Menü angezeigt, in dem Sie das gewünschte Werkzeug auswählen können.