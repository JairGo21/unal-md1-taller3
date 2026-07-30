# Dijkstra: algoritmo para encontrar la ruta mas corta entre dos
# vertices en un grafo con pesos no negativos. Parte del origen con
# distancia 0 y va expandiendo, con una cola de prioridad, el vertice
# con menor distancia tentativa hasta llegar al destino.

import heapq
import csv
import os


def cargar_grafo(ruta: str) -> dict:
    # Lee un archivo CSV con columnas origen, destino y peso
    # y arma el grafo como diccionario de diccionarios (no dirigido)
    grafo = {}
    with open(ruta, encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            a, b, peso = fila["origen"], fila["destino"], int(fila["peso"])
            grafo.setdefault(a, {})[b] = peso
            grafo.setdefault(b, {})[a] = peso
    return grafo


def grafo_ejemplo() -> dict:
    # Carga el grafo de ejemplo guardado en datos/grafo_ejemplo_dijkstra.csv
    ruta = os.path.join(os.path.dirname(__file__), "datos", "grafo_ejemplo_dijkstra.csv")
    return cargar_grafo(ruta)


def dijkstra(grafo: dict, origen: str, destino: str):
    # Encuentra la ruta mas corta entre origen y destino con pesos no negativos
    # Devuelve distancia_total, ruta o None si no hay camino
    if origen not in grafo:
        raise ValueError(f"El vértice de origen '{origen}' no está presente en el grafo.")
    if destino not in grafo:
        raise ValueError(f"El vértice de destino '{destino}' no está presente en el grafo.")

    distancias = {v: float("inf") for v in grafo}
    distancias[origen] = 0
    previo = {}
    visitados = set()

    # La cola de prioridad siempre saca el nodo con menor distancia
    cola = [(0, origen)]
    while cola:
        dist_actual, actual = heapq.heappop(cola)

        # Si ya lo procesamos, lo saltamos
        if actual in visitados:
            continue
        visitados.add(actual)

        # Cuando llegamos al destino podemos cortar
        if actual == destino:
            break

        for vecino, peso in grafo[actual].items():
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                previo[vecino] = actual
                heapq.heappush(cola, (nueva_dist, vecino))

    if distancias[destino] == float("inf"):
        return None, None                # Sin conexión entre origen y destino

    # Reconstruir la ruta hacia atras siguiendo los "previos" hasta llegar al origen
    ruta = [destino]
    while ruta[-1] != origen:
        ruta.append(previo[ruta[-1]])
    ruta.reverse()

    return distancias[destino], ruta


def mostrar_resultado(origen: str, destino: str, distancia, ruta) -> None:
    ancho = 52
    print("\n" + "=" * ancho)
    print("  RESULTADO".center(ancho))
    print("=" * ancho)
    if distancia is None:
        print(f"  No existe un camino entre {origen} y {destino}")
    else:
        print(f"  Origen   : {origen}")
        print(f"  Destino  : {destino}")
        print(f"  Distancia: {distancia}")
        print(f"  Ruta     : {' -> '.join(ruta)}")
    print("=" * ancho + "\n")


def pedir_origen_destino(grafo: dict):
    print("Vértices disponibles:", ", ".join(sorted(grafo.keys())))
    while True:
        origen = input("Origen: ").strip()

        if origen in grafo:
            break
        print(" --> Ese vértice no está presente en el grafo. Intenta de nuevo.")
    while True:
        destino = input("Destino: ").strip()
        if destino in grafo:
            break
        print(" --> Ese vértice no está presente en el grafo. Intenta de nuevo.")
    return origen, destino


def ejemplo() -> None:
    # Caso de ejemplo, ruta mas corta de portal a estadio
    grafo = grafo_ejemplo()
    distancia, ruta = dijkstra(grafo, "Portal", "Estadio")
    mostrar_resultado("Portal", "Estadio", distancia, ruta)
    assert distancia == 12
    assert ruta == ["Portal", "Museo", "Calle26", "Centro", "Estadio"]
    print("--> Coincide con el resultado esperado -> distancia: 12\n")

def abrir_interfaz():
    # Importación local
    from dijkstra_visual import iniciar_editor
    iniciar_editor()

if __name__ == "__main__":
    print("=" * 52)
    print("   Dijkstra - Ruta más corta en ciudad")
    print("=" * 52)
    print("1. Ver ejemplo Portal -> Estadio")
    print("2. Elegir origen y destino")
    print("3. Abrir interfaz gráfica")

    opcion = input("\nElige una opción [1/2/3]: ").strip()
    while opcion not in ("1", "2", "3"):
        opcion = input("Opción inválida. Elegir 1, 2 o 3: ").strip()

    if opcion == "1":
        ejemplo()

    elif opcion == "2":
        grafo = grafo_ejemplo()
        origen, destino = pedir_origen_destino(grafo)
        distancia, ruta = dijkstra(grafo, origen, destino)
        mostrar_resultado(origen, destino, distancia, ruta)

    else:
        abrir_interfaz()
    input("Presiona Enter para salir...")