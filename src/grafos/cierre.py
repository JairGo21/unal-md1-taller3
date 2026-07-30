# Cierre de una estacion: a partir del grafo del punto 4, se elimina
# un vertice o una arista y se vuelven a correr Dijkstra para varios
# pares origen-destino. Asi se mide cuanto cambian las distancias y
# se detecta si algun par queda desconectado.

import os
from dijkstra import dijkstra, grafo_ejemplo, cargar_grafo


def eliminar_vertice(grafo: dict, vertice: str) -> dict:
    # Devuelve un grafo nuevo sin ese vértice y sin las aristas que lo tocaban
    nuevo = {}
    for nodo, vecinos in grafo.items():
        if nodo == vertice:
            continue
        nuevo[nodo] = {v: peso for v, peso in vecinos.items() if v != vertice}
    return nuevo


def eliminar_arista(grafo: dict, a: str, b: str) -> dict:
    # Devuelve un grafo nuevo sin esa conexión puntual.
    nuevo = {nodo: dict(vecinos) for nodo, vecinos in grafo.items()}
    nuevo[a].pop(b, None)
    nuevo[b].pop(a, None)  # tambien al reves porque el grafo es no dirigido
    return nuevo


def comparar_rutas(grafo_antes: dict, grafo_despues: dict, pares) -> list:
    # Para cada par (origen, destino) calcula la distancia antes y después
    # del cierre, arma una fila con la diferencia y el estado resultante
    filas = []
    for origen, destino in pares:
        distancia_antes, _ = dijkstra(grafo_antes, origen, destino)

        if origen not in grafo_despues or destino not in grafo_despues:
            # el vértice cerrado era justo el origen o el destino del par
            filas.append((origen, destino, distancia_antes, None, "-", "Vertice cerrado"))
            continue

        distancia_despues, _ = dijkstra(grafo_despues, origen, destino)

        if distancia_despues is None:
            filas.append((origen, destino, distancia_antes, None, "-", "Desconectado"))
        elif distancia_despues == distancia_antes:
            filas.append((origen, destino, distancia_antes, distancia_despues, 0, "Sin cambio"))
        else:
            diferencia = distancia_despues - distancia_antes
            filas.append((origen, destino, distancia_antes, distancia_despues, diferencia, "Aumentó"))

    return filas


def mostrar_tabla(filas) -> None:
    columnas = ["Origen", "Destino", "Antes", "Después", "Diferencia", "Estado"]

    # Hay que convertir None y guiones a strings antes de medir anchos
    filas_texto = []
    for origen, destino, antes, despues, diferencia, estado in filas:
        despues_txt = str(despues) if despues is not None else "-"
        filas_texto.append([origen, destino, str(antes), despues_txt, str(diferencia), estado])

    anchos = []
    for i, nombre_col in enumerate(columnas):
        largo_datos = max((len(f[i]) for f in filas_texto), default=0)
        anchos.append(max(len(nombre_col), largo_datos))

    def separador():
        return "+" + "+".join("-" * (a + 2) for a in anchos) + "+"

    def fila_texto(valores):
        celdas = [str(v).center(a) for v, a in zip(valores, anchos)]
        return "| " + " | ".join(celdas) + " |"

    print(separador())
    print(fila_texto(columnas))
    print(separador())
    for fila in filas_texto:
        print(fila_texto(fila))
    print(separador())


def pedir_par(grafo):
    print("Vértices disponibles:", ", ".join(sorted(grafo.keys())))
    # Validamos uno por uno para que el usuario no se descuide con el nombre
    while True:
        origen = input("  Origen: ").strip()
        if origen in grafo:
            break
        print("   --> Ese vértice no existe.")
    while True:
        destino = input("  Destino: ").strip()
        if destino in grafo:
            break
        print("   --> Ese vértice no existe.")
    return origen, destino


def elegir_grafo():
    # Deja elegir entre el grafo de ejemplo o uno personalizado
    # armado en el editor visual -> dijkstra_visual.py
    print("\nQué grafo quieres usar?")
    print("1. Grafo punto anterior (ejemplo)")
    print("2. Grafo personalizado -> Editor Visual")
    opcion = input("Elige una opcion [1/2]: ").strip()
    while opcion not in ("1", "2"):
        opcion = input("Opcion invalida. Elige 1 o 2: ").strip()

    if opcion == "1":
        return grafo_ejemplo()

    ruta = os.path.join(os.path.dirname(__file__), "datos", "grafo_personalizado.csv")
    if not os.path.exists(ruta):
        print("\nTodavia no existe un grafo personalizado.")
        print("Primero crea uno y guárdalo usando -> dijkstra_visual.py\n")
        print("Se usará el grafo de ejemplo en su lugar.\n")
        return grafo_ejemplo()

    return cargar_grafo(ruta)


def demo() -> None:
    # Ejemplo con cierre de "Centro"
    grafo_antes = grafo_ejemplo()
    grafo_despues = eliminar_vertice(grafo_antes, "Centro")

    pares = [
        ("Portal", "Estadio"),
        ("Portal", "Terminal"),
        ("Museo", "Terminal"),
        ("Calle26", "Parque"),
        ("Universidad", "Portal"),
    ]

    print("\nCierre del vértice: Centro\n")
    filas = comparar_rutas(grafo_antes, grafo_despues, pares)
    mostrar_tabla(filas)

    afectadas = [f for f in filas if f[5] == "Aumentó"]
    assert len(afectadas) > 0
    print(f"\n--> {len(afectadas)} de {len(filas)} rutas aumentaron su distancia al cerrar Centro\n")


if __name__ == "__main__":
    print("=" * 66)
    print("   Cierre de una estación - impacto en la red")
    print("=" * 66)
    print("1. Ver demo con cierre de Centro")
    print("2. Usar grafo personalizado y elegir cierres.")

    opcion = input("\nElige una opción [1/2]: ").strip()
    while opcion not in ("1", "2"):
        opcion = input("Opción inválida. Elegir 1 o 2: ").strip()

    if opcion == "1":
        demo()
    else:
        grafo_antes = elegir_grafo()
        print("\n1. Cerrar un vértice")
        print("2. Cerrar una arista")
        tipo = input("¿Qué quieres cerrar? [1/2]: ").strip()
        while tipo not in ("1", "2"):
            tipo = input("Opción inválida. Elige 1 o 2: ").strip()

        if tipo == "1":
            print("Vértices disponibles:", ", ".join(sorted(grafo_antes.keys())))
            vertice = input("Vértice a cerrar: ").strip()
            while vertice not in grafo_antes:
                vertice = input("Ese vértice no existe. Intenta de nuevo: ").strip()
            grafo_despues = eliminar_vertice(grafo_antes, vertice)
            print(f"\nCierre del vértice: {vertice}\n")
        else:
            a, b = pedir_par(grafo_antes)
            while b not in grafo_antes[a]:
                print("   --> Esos dos vértices no están conectados directamente.")
                a, b = pedir_par(grafo_antes)
            grafo_despues = eliminar_arista(grafo_antes, a, b)
            print(f"\nCierre de la arista: {a} - {b}\n")

        print("Ingresa al menos 5 pares origen-destino para comparar o escribe 'fin' en el origen para terminar:")
        pares = []
        # El usuario puede ir agregando pares hasta que escriba 'fin' en el origen
        while True:
            origen = input(f"  Par #{len(pares) + 1} - Origen o 'fin': ").strip()
            if origen.lower() == "fin":
                if len(pares) < 1:
                    print("   --> Ingresa al menos un par.")
                    continue
                break
            if origen not in grafo_antes:
                print("   --> Ese vértice no existe.")
                continue
            destino = input("  Destino: ").strip()
            if destino not in grafo_antes:
                print("   --> Ese vértice no existe.")
                continue
            pares.append((origen, destino))

        filas = comparar_rutas(grafo_antes, grafo_despues, pares)
        mostrar_tabla(filas)

    input("\nPresiona Enter para salir...")