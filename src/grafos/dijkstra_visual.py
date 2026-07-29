import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import csv
import math
import os

from dijkstra import dijkstra, cargar_grafo


COLOR_NODO = "#F3F4F6"
COLOR_NODO_SEL = "#60A5FA"
COLOR_NODO_RUTA = "#34D399"
COLOR_BORDE = "#374151"
COLOR_ARISTA = "#9CA3AF"
COLOR_ARISTA_RUTA = "#10B981"


class DialogoPeso:
    # Ventana para pedir el peso.
    def __init__(self, parent):
        self.resultado = None
        self.top = tk.Toplevel(parent)
        self.top.title("Peso de la arista")
        self.top.resizable(False, False)
        self.top.transient(parent)

        ancho, alto = 420, 130
        x = parent.winfo_rootx() + 100
        y = parent.winfo_rooty() + 150
        self.top.geometry(f"{ancho}x{alto}+{x}+{y}")

        tk.Label(self.top, text="Peso de la arista:").pack(pady=(18, 8))
        self.entry = tk.Entry(self.top, width=15, justify="center", font=("Segoe UI", 11))
        self.entry.pack()
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self._aceptar())

        botones = tk.Frame(self.top)
        botones.pack(pady=14)
        tk.Button(botones, text="Aceptar", command=self._aceptar, width=10).pack(side="left", padx=6)
        tk.Button(botones, text="Cancelar", command=self._cancelar, width=10).pack(side="left", padx=6)

        self.top.grab_set()
        self.top.wait_window()

    def _aceptar(self):
        valor = self.entry.get().strip()
        if valor.isdigit() and int(valor) > 0:
            self.resultado = int(valor)
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Escribe un número entero positivo.", parent=self.top)

    def _cancelar(self):
        self.top.destroy()


class EditorGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra visual - editor de grafos")

        # Estructuras que almacenan el grafo.
        self.nodos = {}       # Nombre -> (x, y)
        self.aristas = []     # (a, b, peso)
        self.modo = "vertice"
        self.seleccionados = []
        self.resaltado = set()  # Pares (a,b) que forman parte de la ruta encontrada

        self._armar_interfaz()

    def _armar_interfaz(self):
        barra = tk.Frame(self.root, pady=6)
        barra.pack(fill="x")

        tk.Button(barra, text="Agregar vértice", command=lambda: self._cambiar_modo("vertice")).pack(side="left", padx=4)
        tk.Button(barra, text="Agregar arista", command=lambda: self._cambiar_modo("arista")).pack(side="left", padx=4)
        tk.Button(barra, text="Calcular ruta", command=lambda: self._cambiar_modo("ruta")).pack(side="left", padx=4)
        tk.Button(barra, text="Guardar CSV", command=self._guardar_csv).pack(side="left", padx=4)
        tk.Button(barra, text="Cargar CSV", command=self._cargar_csv).pack(side="left", padx=4)
        tk.Button(barra, text="Reiniciar", command=self._reiniciar).pack(side="left", padx=4)

        self.estado = tk.Label(self.root, text="", anchor="w", fg="#5f5e5a")
        self.estado.pack(fill="x", padx=8)

        self.canvas = tk.Canvas(self.root, width=816, height=504, bg="#B8AAF8", highlightthickness=1, highlightbackground="#c0bcee")
        self.canvas.pack(padx=8, pady=6)
        self.canvas.bind("<Button-1>", self._click_canvas)

        self.resultado = tk.Label(self.root, text="", anchor="w", font=("Aptos", 11, "bold"))
        self.resultado.pack(fill="x", padx=8, pady=(0, 8))

        self._cambiar_modo("vertice")

    def _cambiar_modo(self, modo):
        self.modo = modo
        self.seleccionados = []
        textos = {
            "vertice": "Modo: agregar vértice. Haz click en el lienzo para colocarlo.",
            "arista": "Modo: agregar arista. Haz click en dos vértices para conectarlos.",
            "ruta": "Modo: calcular ruta. Haz click en el origen y luego en el destino.",
        }
        self.estado.config(text=textos[modo])
        self._dibujar()

    def _nodo_en(self, x, y):
        # Devuelve el vértice sobre el que se hizo clic, si existe.
        for nombre, (nx, ny) in self.nodos.items():
            if math.hypot(nx - x, ny - y) < 20:
                return nombre
        return None

    def _click_canvas(self, event):
        # El comportamiento del clic depende del modo seleccionado.
        x, y = event.x, event.y
        clic = self._nodo_en(x, y)

        if self.modo == "vertice":
            if clic:
                return
            nombre = simpledialog.askstring("Nuevo vértice", "Nombre del vértice:")
            if not nombre:
                return
            if nombre in self.nodos:
                messagebox.showerror("Error", "Ese nombre ya existe.")
                return
            self.nodos[nombre] = (x, y)
            self._dibujar()
            return

        if not clic:
            return

        if self.modo == "arista":
            if clic in self.seleccionados:
                return
            self.seleccionados.append(clic)
            self._dibujar()
            if len(self.seleccionados) == 2:
                peso = DialogoPeso(self.root).resultado
                if peso:
                    self.aristas.append((self.seleccionados[0], self.seleccionados[1], peso))
                self.seleccionados = []
                self._dibujar()

        elif self.modo == "ruta":
            if clic in self.seleccionados:
                return
            self.seleccionados.append(clic)
            self._dibujar()
            if len(self.seleccionados) == 2:
                self._calcular_ruta(self.seleccionados[0], self.seleccionados[1])
                self.seleccionados = []

    def _grafo_actual(self) -> dict:
        # Convierte el editor al formato de grafo usado por Dijkstra
        grafo = {}
                # Como el grafo es no dirigido, cada arista se agrega en ambos sentidos.
                # Se dibujan primero las aristas para que los nodos queden encima.
        for a, b, peso in self.aristas:
            grafo.setdefault(a, {})[b] = peso
            grafo.setdefault(b, {})[a] = peso
                # Conserva también los vértices sin conexiones.
        for nombre in self.nodos:
            grafo.setdefault(nombre, {})
        return grafo

    def _calcular_ruta(self, origen, destino):
        # Ejecuta Dijkstra y actualiza la ruta resaltada.
        grafo = self._grafo_actual()
        distancia, ruta = dijkstra(grafo, origen, destino)
        if distancia is None:
            self.resultado.config(text=f"No existe un camino entre {origen} y {destino}")
            self.resaltado = set()
        else:
            self.resultado.config(text=f"Distancia: {distancia}   |   Ruta: {' -> '.join(ruta)}")
            self.resaltado = {(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)}
        self._dibujar()

    def _en_ruta(self, a, b):
        # Indica si una arista pertenece a la ruta más corta.
        return (a, b) in self.resaltado or (b, a) in self.resaltado

    def _dibujar(self):
        # Borra el dibujo anterior para redibujar el estado actual.
        self.canvas.delete("all")

                # Se dibujan primero las aristas para que los nodos queden encima.
        for a, b, peso in self.aristas:
            xa, ya = self.nodos[a]
            xb, yb = self.nodos[b]
            en_ruta = self._en_ruta(a, b)
            color = COLOR_ARISTA_RUTA if en_ruta else COLOR_ARISTA
            ancho = 3 if en_ruta else 1.5
            self.canvas.create_line(xa, ya, xb, yb, fill=color, width=ancho)
            mx, my = (xa + xb) / 2, (ya + yb) / 2
            self.canvas.create_oval(mx - 11, my - 11, mx + 11, my + 11, fill="white", outline=color)
            self.canvas.create_text(mx, my, text=str(peso), font=("Aptos", 9))

                # Después se dibujan los vértices con su estado correspondiente.
        for nombre, (x, y) in self.nodos.items():
            seleccionado = nombre in self.seleccionados
            en_ruta = any(nombre in par for par in self.resaltado)
            color = COLOR_NODO_SEL if seleccionado else (COLOR_NODO_RUTA if en_ruta else COLOR_NODO)
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline=COLOR_BORDE, width=1.5)
            self.canvas.create_text(x, y, text=nombre, font=("Aptos", 10, "bold"))

    def _guardar_csv(self):
        # Guarda el grafo y las posiciones de los vértices.
        if not self.aristas:
            messagebox.showinfo("Guardar", "Todavia no hay aristas para guardar.")
            return
        carpeta = os.path.join(os.path.dirname(__file__), "datos")
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, "grafo_personalizado.csv")
        ruta_pos = os.path.join(carpeta, "grafo_personalizado_pos.csv")

        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["origen", "destino", "peso"])

            for a, b, peso in self.aristas:
                escritor.writerow([a, b, peso])

        # Guarda las posiciones para recuperar el mismo diseño al cargar.
        with open(ruta_pos, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["nombre", "x", "y"])

            for nombre, (x, y) in self.nodos.items():
                escritor.writerow([nombre, round(x), round(y)])

        messagebox.showinfo("Guardar", "Grafo guardado en:\ndatos/grafo_personalizado.csv")

    def _cargar_posiciones(self, ruta_csv):
        # Carga las posiciones asociadas al grafo, si existen.
        # Busca el archivo de posiciones correspondiente al CSV principal
        carpeta = os.path.dirname(ruta_csv)
        nombre = os.path.splitext(os.path.basename(ruta_csv))[0]

        ruta_pos = os.path.join(carpeta, f"{nombre}_pos.csv")

        if not os.path.exists(ruta_pos):
            return {}

        posiciones = {}

        with open(ruta_pos, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                posiciones[fila["nombre"]] = (float(fila["x"]), float(fila["y"]))

        return posiciones

    def _cargar_csv(self):
        # Recupera el último grafo guardado y su distribución.
        carpeta = os.path.join(os.path.dirname(__file__), "datos")
        ruta = os.path.join(carpeta, "grafo_personalizado.csv")

        if not os.path.exists(ruta):
            messagebox.showerror(
                "Error",
                "No existe un grafo guardado.\nPrimero guarda un grafo."
            )
            return

        grafo = cargar_grafo(ruta)
        posiciones = self._cargar_posiciones(ruta)
        self._reiniciar(limpiar_solo=True)

        nombres = list(grafo.keys())
        centro_x, centro_y, radio = 408, 252, 180

                # Los vértices sin posición guardada se acomodan automáticamente.
        sin_posicion = [n for n in nombres if n not in posiciones]

        for i, nombre in enumerate(sin_posicion):
            angulo = 2 * math.pi * i / max(len(sin_posicion), 1)
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            posiciones[nombre] = (x, y)

        for nombre in nombres:
            self.nodos[nombre] = posiciones[nombre]

                # Evita duplicar aristas al reconstruir el grafo.
        ya_agregadas = set()
        for a, vecinos in grafo.items():
            for b, peso in vecinos.items():
                if (b, a) in ya_agregadas:
                    continue
                self.aristas.append((a, b, peso))
                ya_agregadas.add((a, b))

        self._dibujar()
        self.estado.config(text="Grafo personalizado cargado.")

    def _reiniciar(self, limpiar_solo=False):
        # Limpia el editor para comenzar un nuevo grafo.
        self.nodos = {}
        self.aristas = []
        self.seleccionados = []
        self.resaltado = set()
        self.resultado.config(text="")
        if not limpiar_solo:
            self._cambiar_modo("vertice")
        self._dibujar()


def iniciar_editor():
    root = tk.Tk()
    EditorGrafo(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_editor()
