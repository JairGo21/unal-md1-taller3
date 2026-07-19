import heapq

def grafo_ejemplo() -> dict:
    # Grafo de una ciudad con 8 vertices, 13 conexiones, peso equivalente a tiempo en minutos.
    conexiones = [
        ("Portal", "Calle26", 4),
        ("Portal", "Museo", 2),
        ("Calle26", "Centro", 5),
        ("Calle26", "Museo", 1),
        ("Museo", "Centro", 8),
        ("Museo", "Universidad", 10),
        ("Centro", "Universidad", 2),
        ("Centro", "Parque", 6),
        ("Centro", "Estadio", 4),
        ("Universidad", "Parque", 3),
        ("Universidad", "Estadio", 9),
        ("Parque", "Terminal", 1),
        ("Terminal", "Estadio", 7),
    ]

    grafo = {}
    for a, b, peso in conexiones:
        grafo.setdefault(a, {})[b] = peso
        grafo.setdefault(b, {})[a] = peso  # el grafo es no dirigido
    return grafo


def dijkstra(grafo: dict, origen: str, destino: str):
    # Encuentra la ruta mas corta entre origen y destino con pesos no negativos
    # Devuelve distancia_total, ruta o None si no hay camino.
    if origen not in grafo:
        raise ValueError(f"El vertice de origen '{origen}' no está presente en el grafo")
    if destino not in grafo:
        raise ValueError(f"El vertice de destino '{destino}' no está presente en el grafo")

    distancias = {v: float("inf") for v in grafo}
    distancias[origen] = 0
    previo = {}
    visitados = set()

    cola = [(0, origen)]
    while cola:
        dist_actual, actual = heapq.heappop(cola)

        if actual in visitados:
            continue
        visitados.add(actual)

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
    grafo = grafo_ejemplo()
    distancia, ruta = dijkstra(grafo, "Portal", "Estadio")
    mostrar_resultado("Portal", "Estadio", distancia, ruta)
    assert distancia == 12
    assert ruta == ["Portal", "Museo", "Calle26", "Centro", "Estadio"]
    print("--> Coincide con el resultado esperado -> distancia: 12\n")


if __name__ == "__main__":
    print("=" * 52)
    print("   Dijkstra - Ruta más corta en ciudad")
    print("=" * 52)
    print("1. Ver ejemplo Portal -> Estadio")
    print("2. Elegir origen y destino")

    opcion = input("\nElige una opcion [1/2]: ").strip()
    while opcion not in ("1", "2"):
        opcion = input("Opcion inválida. Elegir 1 o 2: ").strip()

    if opcion == "2":
        grafo = grafo_ejemplo()
        origen, destino = pedir_origen_destino(grafo)
        distancia, ruta = dijkstra(grafo, origen, destino)
        mostrar_resultado(origen, destino, distancia, ruta)
    else:
        ejemplo()

    input("Presiona Enter para salir...")