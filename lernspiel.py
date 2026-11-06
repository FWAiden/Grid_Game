"""Ein animiertes Lernspiel für verschachtelte Schleifen. Start: python lernspiel.py"""

import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk


SIZE = 8
START_CODE = '''# feld ist eine Liste mit 8 Zeilen.
# Jede Zeile enthält 8 Felder (anfangs False).
# feld[y][x] bezeichnet ein Feld.
# x: Spalte, y: Zeile; jeweils 0 bis 7.
# mark() markiert das Feld bei deinen Variablen x und y.

x = 0
y = 0
mark()

# Deine Aufgabe: Ersetze das Beispiel oben durch
# zwei verschachtelte for-Schleifen und markiere
# damit alle 64 Felder!
# Hilfen: range(...), len(...), feld[y]
'''


class RunStopped(Exception):
    pass


class LoopGame:
    def __init__(self, root):
        self.root = root
        root.title("Schleifen-Abenteuer · 64 Felder, zwei Schleifen")
        root.geometry("1120x760")
        root.minsize(940, 690)
        self.events = queue.Queue()
        self.stop_event = threading.Event()
        self.worker = None
        self.delay = 0.22
        self.marked = set()
        self.position = (0, 0)
        self.build_ui()
        self.draw_board()
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(25, self.poll)

    def build_ui(self):
        self.root.configure(bg="#101827")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#101827")
        style.configure("TLabel", background="#101827", foreground="#e5eaf3")
        outer = ttk.Frame(self.root, padding=22)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="SCHLEIFEN-ABENTEUER", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Deine Mission: Besuche und markiere alle 64 Felder mit zwei verschachtelten for-Schleifen.",
                  wraplength=1020, font=("Segoe UI", 11)).pack(anchor="w", pady=(5, 18))
        columns = ttk.Frame(outer)
        columns.pack(fill="both", expand=True)
        columns.columnconfigure(0, weight=1)
        columns.columnconfigure(1, weight=1)
        columns.rowconfigure(0, weight=1)
        left = ttk.Frame(columns, padding=(0, 0, 20, 0))
        left.grid(row=0, column=0, sticky="nsew")
        right = ttk.Frame(columns)
        right.grid(row=0, column=1, sticky="nsew")
        ttk.Label(left, text="DEIN PYTHON-CODE", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
        self.editor = tk.Text(left, width=46, height=23, bg="#182438", fg="#e6edf7",
                              insertbackground="white", font=("Consolas", 11), wrap="none",
                              undo=True, padx=12, pady=12)
        self.editor.pack(fill="both", expand=True)
        self.editor.insert("1.0", START_CODE)
        self.editor.tag_configure("active", background="#344660")
        self.editor.bind("<Tab>", self.indent)
        self.editor.bind("<Return>", self.newline)
        actions = ttk.Frame(left)
        actions.pack(fill="x", pady=12)
        self.run_button = ttk.Button(actions, text="▶ Ausführen", command=self.run)
        self.run_button.pack(side="left")
        self.stop_button = ttk.Button(actions, text="■ Stoppen", command=self.stop, state="disabled")
        self.stop_button.pack(side="left", padx=8)
        ttk.Button(actions, text="Zurücksetzen", command=self.reset).pack(side="left")
        ttk.Label(left, text="Langsam                                          Schnell").pack(anchor="w")
        speed = ttk.Scale(left, from_=0.6, to=0.05, command=self.change_speed)
        speed.set(self.delay)
        speed.pack(fill="x")
        ttk.Label(left, text="Die helle Codezeile zeigt den aktuellen Schritt.\nTab fügt vier Leerzeichen ein. Jeder Start leert das Feld.",
                  wraplength=450).pack(anchor="w", pady=10)
        ttk.Label(right, text="DEIN SPIELFELD · feld[y][x]", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
        self.canvas = tk.Canvas(right, width=440, height=440, bg="#101827", highlightthickness=0)
        self.canvas.pack(anchor="center")
        self.progress = ttk.Label(right, text="", font=("Segoe UI", 13, "bold"))
        self.progress.pack(anchor="w", pady=(12, 8))
        ttk.Label(right, text="Tipp: nutze die Funktion 'mark()', um ein Feld zu markieren, auf dem du stehst.",
                  wraplength=440, font=("Segoe UI", 11)).pack(anchor="w")
        ttk.Label(right, text="Weißes X = deine Position · Rot = markiert\nSetze x (Spalte) und y (Zeile) in deinen Schleifen.\nOben links: (0, 0) · Unten rechts: (7, 7)",
                  wraplength=440).pack(anchor="w", pady=10)
        self.status = ttk.Label(outer, text="Bereit! Probiere zunächst das Beispiel aus.", wraplength=1020,
                                font=("Segoe UI", 11))
        self.status.pack(anchor="w", pady=(12, 0))

    def indent(self, _event):
        self.editor.insert("insert", "    ")
        return "break"

    def newline(self, _event):
        line = self.editor.get("insert linestart", "insert")
        indent = len(line) - len(line.lstrip(" "))
        self.editor.insert("insert", "\n" + " " * (indent + (4 if line.rstrip().endswith(":") else 0)))
        return "break"

    def change_speed(self, value):
        self.delay = float(value)

    def draw_board(self):
        self.canvas.delete("all")
        cell, margin = 48, 40
        for n in range(SIZE):
            self.canvas.create_text(margin + n * cell + cell / 2, 20, text=str(n), fill="#b8c9e0")
            self.canvas.create_text(20, margin + n * cell + cell / 2, text=str(n), fill="#b8c9e0")
        for y in range(SIZE):
            for x in range(SIZE):
                px, py = margin + x * cell, margin + y * cell
                color = "#e3424b" if (x, y) in self.marked else "#24364e"
                self.canvas.create_rectangle(px + 2, py + 2, px + cell - 2, py + cell - 2,
                                             fill=color, outline="")
        x, y = self.position
        self.canvas.create_text(margin + x * cell + cell / 2, margin + y * cell + cell / 2,
                                text="X", fill="white", font=("Consolas", 23, "bold"))
        self.progress.configure(text=f"{len(self.marked)} / 64 markiert · Position ({x}, {y})")

    def reset(self):
        if self.worker and self.worker.is_alive():
            self.status.configure(text="Stoppe den laufenden Code, bevor du zurücksetzt.")
            return
        self.marked.clear()
        self.position = (0, 0)
        self.editor.tag_remove("active", "1.0", "end")
        self.draw_board()
        self.status.configure(text="Neues Spielfeld – dein Code bleibt erhalten.")

    def run(self):
        if self.worker and self.worker.is_alive():
            return
        self.reset()
        source = self.editor.get("1.0", "end-1c")
        try:
            code = compile(source, "<dein-code>", "exec")
        except SyntaxError as error:
            self.status.configure(text=f"Syntaxfehler in Zeile {error.lineno}: {error.msg}")
            return
        self.stop_event.clear()
        self.editor.configure(state="disabled")
        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status.configure(text="Dein Code läuft … verfolge das weiße X!")
        self.worker = threading.Thread(target=self.execute, args=(code,), daemon=True)
        self.worker.start()

    def execute(self, code):
        field = [[False for _ in range(SIZE)] for _ in range(SIZE)]
        steps = 0

        def position(local):
            x, y = local.get("x", 0), local.get("y", 0)
            if type(x) is not int or type(y) is not int or not (0 <= x < SIZE and 0 <= y < SIZE):
                raise ValueError("x und y müssen ganze Zahlen von 0 bis 7 sein.")
            return x, y

        def pause():
            if self.stop_event.wait(self.delay):
                raise RunStopped()

        def trace(frame, event, _arg):
            nonlocal steps
            if frame.f_code.co_filename == "<dein-code>" and event == "line":
                steps += 1
                if self.stop_event.is_set():
                    raise RunStopped()
                if steps > 10000:
                    raise ValueError("Zu viele Schritte. Prüfe deine Schleifen (maximal 10.000 Schritte).")
                self.events.put(("step", (frame.f_lineno, position(frame.f_locals))))
                pause()
            return trace

        def mark():
            x, y = position(sys._getframe(1).f_locals)
            field[y][x] = True
            self.events.put(("mark", (x, y)))
            pause()

        # Bewusst kleine Lernumgebung; kein Sicherheits-Sandbox für fremden Code.
        namespace = {"__builtins__": {"range": range, "len": len, "enumerate": enumerate,
                                      "list": list, "int": int, "bool": bool},
                     "feld": field, "mark": mark}
        try:
            sys.settrace(trace)
            exec(code, namespace)
            self.events.put(("done", "finished"))
        except RunStopped:
            self.events.put(("done", "stopped"))
        except BaseException as error:
            self.events.put(("error", f"{type(error).__name__}: {error}"))
        finally:
            sys.settrace(None)

    def stop(self):
        self.stop_event.set()

    def poll(self):
        for _ in range(100):
            try:
                kind, payload = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == "step":
                line, self.position = payload
                self.editor.tag_remove("active", "1.0", "end")
                self.editor.tag_add("active", f"{line}.0", f"{line}.end")
                self.editor.see(f"{line}.0")
                self.draw_board()
            elif kind == "mark":
                self.position = payload
                self.marked.add(payload)
                self.draw_board()
                if len(self.marked) == SIZE * SIZE:
                    self.status.configure(text="★ Gewonnen! Du hast alle 64 Felder markiert!")
            else:
                self.editor.configure(state="normal")
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                self.editor.tag_remove("active", "1.0", "end")
                if kind == "error":
                    self.status.configure(text=payload)
                elif payload == "stopped":
                    self.status.configure(text="Gestoppt. Ändere deinen Code und probiere es erneut.")
                elif len(self.marked) == SIZE * SIZE:
                    self.status.configure(text="★ Gewonnen! Du hast alle 64 Felder markiert!")
                else:
                    self.status.configure(text=f"Code beendet: {len(self.marked)} von 64 Feldern. Schaffst du den Rest?")
        self.root.after(25, self.poll)

    def close(self):
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    LoopGame(tk.Tk()).root.mainloop()
