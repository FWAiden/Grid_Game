# Schleifen-Abenteuer

Starte das Lernspiel mit `python lernspiel.py` (unter Windows auch `py lernspiel.py`).
Es benötigt Python 3 mit Tkinter, das bei der normalen Python-Installation für Windows enthalten ist. Weitere Pakete sind nicht nötig.

## Installation und Start unter Windows

### 1. Python installieren oder prüfen

Mit **Python 3.10.11 und Tkinter 8.6** wurde das Spiel bereits getestet. Wenn Python installiert ist, öffne PowerShell und prüfe:

```powershell
py --version
py -m tkinter
```

Der zweite Befehl sollte ein kleines Testfenster öffnen. Schließe es anschließend wieder.

Wenn Python fehlt, lade eine stabile Python-3-Version von der [offiziellen Windows-Downloadseite](https://www.python.org/downloads/windows/) herunter. Nutze den Python Install Manager oder einen regulären Windows-Installer, kein „embeddable package“.

Beim regulären Installer aktiviere **Add python.exe to PATH** und lasse **pip**, **Python Launcher** sowie **Tcl/Tk and IDLE** aktiviert. Beim Install Manager folge der Einrichtung einer Python-3-Version. Öffne nach der Installation PowerShell erneut und führe die beiden Prüfungen oben aus. Weitere Hinweise stehen in der [offiziellen Windows-Anleitung](https://docs.python.org/3/using/windows.html).

### 2. Spiel herunterladen

Lade das Repository auf GitHub über **Code → Download ZIP** herunter und entpacke die ZIP-Datei vollständig. Git ist dafür nicht erforderlich. Öffne den entpackten Ordner, in dem `lernspiel.py`, `requirements.txt` und diese Anleitung liegen.

### 3. PowerShell im Spielordner öffnen

Klicke im Windows-Explorer in die Adressleiste des Spielordners, tippe `powershell` ein und drücke Enter. Das Terminal startet direkt im richtigen Ordner.

### 4. Abhängigkeiten prüfen und Spiel starten

```powershell
py -m pip install -r requirements.txt
py lernspiel.py
```

Das Spielfenster öffnet sich. Links kannst du deinen Code schreiben und mit **Ausführen** starten.

Die `requirements.txt` enthält nur Kommentare, da das Spiel keine externen Pakete benötigt. Der pip-Befehl ist deshalb optional. Tkinter gehört zur Python-Installation und wird nicht über pip nachinstalliert. Eine virtuelle Umgebung ist für dieses Spiel nicht erforderlich.

### Hilfe bei Startproblemen

- **„py wurde nicht erkannt“:** Öffne das Terminal erneut. Wenn `python --version` funktioniert, ersetze in allen Befehlen `py` durch `python`. Andernfalls richte Python wie in Schritt 1 ein.
- **„No module named tkinter“ oder „_tkinter“:** Beim regulären Python-Installer wähle **Modify** und aktiviere **Tcl/Tk and IDLE**. Bei einer anderen Python-Distribution installiere eine vollständige Version von python.org. Prüfe danach erneut mit `py -m tkinter`.
- **„No module named pip“:** Führe `py -m ensurepip --upgrade` aus. Für das Spiel selbst kannst du den pip-Schritt auch überspringen.
- **„lernspiel.py nicht gefunden“:** Öffne PowerShell im entpackten Spielordner, wie in Schritt 3 beschrieben.
- **Beim Doppelklick schließt sich ein Fenster sofort:** Starte das Spiel mit `py lernspiel.py` in PowerShell. Dort bleibt eine mögliche Fehlermeldung sichtbar.

## So funktioniert das Spiel

Links schreibst du Python, rechts siehst du jeden Schritt. Mit dem Regler kannst du die Animation verlangsamen. „Stoppen“ unterbricht den Code; „Zurücksetzen“ leert das Feld und behält deinen Code.

## Deine Aufgabe

Markiere mit zwei verschachtelten `for`-Schleifen alle 64 Felder. `feld` ist eine Liste mit acht Zeilen, die jeweils acht Werte enthalten. `feld[y][x]` spricht einen Wert an. Die Variablen `x` und `y` bestimmen die Position des weißen X. `mark()` markiert diese Position rot und setzt den entsprechenden Listenwert auf `True`.

Die Indizes gehen in Python von **0 bis 7**. Ein Feld von (0, 0) bis einschließlich (8, 8) hätte 9 × 9 Felder.

Verfügbar sind `range`, `len`, `enumerate`, `list`, `int`, `bool`, `feld` und `mark`. Der Editor zeigt nur deinen Übungscode, die Hilfsfunktion bleibt im Hintergrund. Jeder Start setzt das Spielfeld zurück. Die Anwendung führt lokalen Python-Code aus und ist keine Sicherheits-Sandbox für nicht vertrauenswürdigen Code.

<details>
<summary>Lösung ansehen, wenn du nicht weiterkommst</summary>

```python
for y in range(len(feld)):
    for x in range(len(feld[y])):
        mark()
```

Die äußere Schleife geht durch die Zeilen. Für jede Zeile geht die innere Schleife durch alle Spalten.

</details>
