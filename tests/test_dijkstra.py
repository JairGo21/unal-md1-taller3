import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.grafos.dijkstra import grafo_ejemplo, dijkstra


def ejecutar_pruebas():
    print("========== PRUEBAS DIJKSTRA ==========\n")
    grafo = grafo_ejemplo()

    print("Prueba 1: Portal -> Estadio")
    distancia, ruta = dijkstra(grafo, "Portal", "Estadio")
    print("Distancia:", distancia, "| Ruta:", " -> ".join(ruta))
    print("OK" if distancia == 12 and ruta == ["Portal", "Museo", "Calle26", "Centro", "Estadio"] else "ERROR")
    print()

    print("Prueba 2: Mismo origen y destino.")
    distancia, ruta = dijkstra(grafo, "Centro", "Centro")
    print("Distancia:", distancia, "| Ruta:", " -> ".join(ruta))
    print("OK" if distancia == 0 and ruta == ["Centro"] else "ERROR")
    print()

    print("Prueba 3: Centro -> Terminal")
    distancia, ruta = dijkstra(grafo, "Centro", "Terminal")
    print("Distancia:", distancia, "| Ruta:", " -> ".join(ruta))
    print("OK" if distancia == 6 and ruta == ["Centro", "Universidad", "Parque", "Terminal"] else "ERROR")
    print()

    print("Prueba 4: Grafo mínimo 8 vertices y 12 aristas")
    num_vertices = len(grafo)
    num_aristas = sum(len(vecinos) for vecinos in grafo.values()) // 2  # Cada arista se cuenta 2 veces
    print(f"Vertices: {num_vertices} | Aristas: {num_aristas}")
    print("OK" if num_vertices >= 8 and num_aristas >= 12 else "ERROR")
    print()

    print("Prueba 5: Vértice de origen que no existe")
    try:
        dijkstra(grafo, "Hola1", "Centro")
        print("ERROR: no lanzó excepción")
    except ValueError as e:
        print("OK: Se rechazó correctamente ->", e)
    print()


if __name__ == "__main__":
    ejecutar_pruebas()