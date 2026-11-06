# Schleifen-Abenteuer

Starte das Lernspiel mit `python lernspiel.py` (unter Windows auch `py lernspiel.py`).
Es benötigt Python 3 mit Tkinter, das bei der normalen Python-Installation für Windows enthalten ist. Weitere Pakete sind nicht nötig.

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
