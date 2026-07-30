import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.grafos.coloreo import (
    colorear_voraz,
    verificar_coloreo,
    grafo_ejemplo_coloreo,
    grafo_personalizado_coloreo,
    hay_grafo_personalizado,
)


def verificar(descripcion, obtenido, esperado):
    estado = "OK" if obtenido == esperado else "ERROR"
    print(f"[{estado}] {descripcion} -> obtenido: {obtenido} | esperado: {esperado}")


def ejecutar_pruebas():
    print("\n========== PRUEBAS COLOREO DE GRAFOS ==========\n")

    # Prueba 1: el grafo de ejemplo debe quedar sin conflictos
    print("Prueba 1: Grafo de ejemplo debe colorearse sin conflictos")
    grafo = grafo_ejemplo_coloreo()
    asignacion = colorear_voraz(grafo)
    verificar("  0 conflictos en el coloreo", verificar_coloreo(grafo, asignacion), True)
    verificar("  todos los vertices quedaron coloreados", len(asignacion), len(grafo))
    verificar("  al menos 6 colores (chi >= 6 por construccion)", max(asignacion.values()) >= 6, True)
    print()

    # Prueba 2: un triángulo siempre necesita 3 colores
    print("Prueba 2: Triangulo - 3 vertices, todos conectados, necesita 3 colores")
    triangulo = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"},
    }
    asig_tri = colorear_voraz(triangulo)
    verificar("  coloreo valido", verificar_coloreo(triangulo, asig_tri), True)
    verificar("  exactamente 3 colores", max(asig_tri.values()), 3)
    verificar("  3 vertices coloreados", len(asig_tri), 3)
    print()

    # Prueba 3: un camino de 3 vertices alcanza con 2 colores
    print("Prueba 3: Camino A-B-C alcanza con 2 colores")
    camino = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B"},
    }
    asig_cam = colorear_voraz(camino)
    verificar("  coloreo válido", verificar_coloreo(camino, asig_cam), True)
    verificar("  2 colores o menos", max(asig_cam.values()) <= 2, True)
    print()

    # Prueba 4: el verificador detecta una mala asignacion
    print("Prueba 4: se debe detectar una asignación inválida")
    grafo_malo = {
        "X": {"Y"},
        "Y": {"X", "Z"},
        "Z": {"Y"},
    }
    asignacion_mala = {"X": 1, "Y": 1, "Z": 2}
    verificar("  detecta conflicto X-Y mismo color", verificar_coloreo(grafo_malo, asignacion_mala), False)
    asignacion_buena = {"X": 1, "Y": 2, "Z": 1}
    verificar("  acepta asignación correcta", verificar_coloreo(grafo_malo, asignacion_buena), True)
    print()

    # Prueba 5: el conteo de colores y los vertices por color son correctos
    print("Prueba 5: conteo de colores y agrupación por color")
    grafo5 = {
        "A": {"B", "C"},
        "B": {"A"},
        "C": {"A"},
    }
    asig5 = colorear_voraz(grafo5)
    grupos = {}
    for v, c in asig5.items():
        grupos.setdefault(c, set()).add(v)
    total_colores = max(asig5.values())
    verificar("  total de colores utilizadoos", total_colores, 2)
    verificar("  hay vértices en el color 1", 1 in grupos and len(grupos[1]) >= 1, True)
    verificar("  cada color tiene al menos un vertice", all(len(s) >= 1 for s in grupos.values()), True)
    print()

if __name__ == "__main__":
    ejecutar_pruebas()