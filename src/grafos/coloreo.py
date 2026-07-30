# Coloreo de grafos: se asigna un color a cada vertice de manera que
# ningun par adyacente comparta color. Usamos el algoritmo voraz de
# Welsh-Powell. No siempre da el mínimo, pero siempre produce un coloreo válido.

import csv
import os


def cargar_grafo_coloreo(ruta: str) -> dict:
    # Lee el CSV con columnas origen y destino y arma el grafo
    grafo: dict[str, set] = {}
    with open(ruta, encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            a = fila["origen"].strip()
            b = fila["destino"].strip()
            grafo.setdefault(a, set()).add(b)
            grafo.setdefault(b, set()).add(a)
    return grafo

def grafo_ejemplo_coloreo() -> dict:
    # Carga el grafo de ejemplo en la ruta guardada
    ruta = os.path.join(os.path.dirname(__file__), "datos", "grafo_ejemplo_coloreo.csv")
    return cargar_grafo_coloreo(ruta)


def grafo_personalizado_coloreo() -> dict:
    # Carga el grafo que el usuario haya guardado antes desde
    # el editor visual de Dijkstra (mismo archivo compartido)
    ruta = os.path.join(os.path.dirname(__file__), "datos", "grafo_personalizado.csv")
    return cargar_grafo_coloreo(ruta)


def hay_grafo_personalizado() -> bool:
    ruta = os.path.join(os.path.dirname(__file__), "datos", "grafo_personalizado.csv")
    return os.path.exists(ruta)

def colorear_voraz(grafo: dict) -> dict:
    # Se usa el algorimo welsh powell, ordenamos los vertices descendente por grado y
    # le asignamos a cada nodo el color más bajo posible que no esté en ninguno de sus vecinos

    vertices = sorted(grafo.keys(), key=lambda v: len(grafo[v]), reverse=True)
    asignacion: dict[str, int] = {}
    for v in vertices:
        colores_usados = {asignacion[w] for w in grafo[v] if w in asignacion}
        color = 1
        while color in colores_usados:
            color += 1
        asignacion[v] = color
    return asignacion


def verificar_coloreo(grafo: dict, asignacion: dict) -> bool:
    # Revisa que ningun par de vertices adyacentes comparta color
    # Devuelve True si el coloreo es valido, False si hay un conflicto
    for v, vecinos in grafo.items():
        for w in vecinos:
            if asignacion.get(v) == asignacion.get(w):
                return False
    return True



PALETA = ["Rojo", "Azul", "Verde", "Amarillo","Naranja", "Morado", "Rosado", "Cian","Café", "Gris", "Turquesa", "Lima",]


def nombre_color(indice: int) -> str:
    # Devuelve el nombre del color segun su índice
    return PALETA[(indice - 1) % len(PALETA)]


def mostrar_resultado(asignacion: dict) -> None:
    # Imprime cuantos colores se usaron y que vertices tiene cada color
    ancho = 52
    print("\n"+"=" *ancho)
    print("  RESULTADO DEL COLOREO".center(ancho))
    print("=" * ancho)

    total = max(asignacion.values())
    print(f"  Colores usados: {total}")

    grupos: dict[int, list] = {}
    for v, c in asignacion.items():
        grupos.setdefault(c, []).append(v)

    for c in sorted(grupos):
        verts = ", ".join(sorted(grupos[c]))
        print(f"  {nombre_color(c):10} ({c}): {verts}")
    print("=" * ancho + "\n")


def ejemplo() -> None:
    # Corre el coloreo sobre el grafo de ejemplo y verifica que sea valido
    grafo = grafo_ejemplo_coloreo()
    asignacion = colorear_voraz(grafo)
    mostrar_resultado(asignacion)
    assert verificar_coloreo(grafo, asignacion) is True
    print("--> El coloreo es válido pues ningún par de vértices adyacentes comparte colores.\n")


if __name__ == "__main__":
    print("=" * 52)
    print("   Coloreo de grafos - algoritmo voraz")
    print("=" * 52)
    print("1. Usar el grafo de ejemplo")
    print("2. Usar el grafo personalizado guardado")

    opcion = input("\nElige una opción [1/2]: ").strip()
    while opcion not in ("1", "2"):
        opcion = input("Opción inválida. Elige 1 o 2: ").strip()

    if opcion == "1":
        ejemplo()
    else:
        if not hay_grafo_personalizado():
            print("\nNo hay un grafo personalizado guardado todavía.")
            print("Crea uno desde src/grafos/dijkstra_visual.py y vuelve a intentarlo.\n")
            input("Presiona Enter para salir...")
            exit()
        grafo = grafo_personalizado_coloreo()
        asignacion = colorear_voraz(grafo)
        mostrar_resultado(asignacion)
        if verificar_coloreo(grafo, asignacion):
            print("--> El coloreo es válido pues ningún par de vértices adyacentes comparte colores.\n")
        else:
            print("--> ERROR: el coloreo tiene conflictos.\n")

    input("Presiona Enter para salir...")