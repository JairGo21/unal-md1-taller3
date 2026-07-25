import sys, os

# Agrega las rutas para importar los módulos del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "grafos"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Importa las funciones que se van a probar
from src.grafos.dijkstra import grafo_ejemplo
from src.grafos.cierre import eliminar_vertice, eliminar_arista, comparar_rutas


def verificar(descripcion, obtenido, esperado):
# Comprueba si el resultado obtenido coincide con el esperado
    estado = "OK" if obtenido == esperado else "ERROR"
    print(f"[{estado}] {descripcion} -> obtenido: {obtenido} | esperado: {esperado}")


def ejecutar_pruebas():
    print("\n========== PRUEBAS CIERRE DE ESTACION ==========\n")

    # Se crea el grafo original y otro con la estación Centro eliminada
    grafo_antes = grafo_ejemplo()
    grafo_despues = eliminar_vertice(grafo_antes, "Centro")

    # Verifica que cerrar Centro obliga a tomar una ruta más larga
    print("Prueba 1: Portal -> Estadio con Centro cerrado, debe aumentar de 12 a 21")
    filas = comparar_rutas(grafo_antes, grafo_despues, [("Portal", "Estadio")])
    origen, destino, antes, despues, diferencia, estado = filas[0]
    verificar("  distancia antes", antes, 12)
    verificar("  distancia después", despues, 21)
    verificar("  diferencia", diferencia, 9)
    verificar("  estado", estado, "Aumentó")
    print()

    # Verifica que la ruta Portal -> Museo no cambia al ser una conexión directa
    print("Prueba 2: Portal -> Museo con Centro cerrado, no deberia cambiar pues es conexión directa")
    filas = comparar_rutas(grafo_antes, grafo_despues, [("Portal", "Museo")])
    _, _, antes, despues, diferencia, estado = filas[0]
    verificar("  distancia antes == después", antes == despues, True)
    verificar("  estado", estado, "Sin cambio")
    print()

    # Comprueba que eliminar un vértice también elimina todas sus conexiones
    print("Prueba 3: eliminar_vertice quita el vértice y todas sus conexiones")
    verificar("  Centro ya no está en el grafo", "Centro" in grafo_despues, False)
    verificar("  ningún vecino apunta a Centro", any("Centro" in v for v in grafo_despues.values()), False)
    print()

    # Comprueba que eliminar una arista solo afecta esa conexión
    print("Prueba 4: eliminar_arista solo quita esa conexión puntual, los demás vértices quedan igual")
    sin_arista = eliminar_arista(grafo_antes, "Portal", "Museo")
    verificar("  Portal ya no conecta con Museo", "Museo" in sin_arista["Portal"], False)
    verificar("  Museo ya no conecta con Portal", "Portal" in sin_arista["Museo"], False)
    verificar("  Portal sigue conectado con Calle26", "Calle26" in sin_arista["Portal"], True)
    print()

    # Verifica que se puedan comparar varios pares de estaciones al mismo tiempo
    print("Prueba 5: Pares distintos deben poder compararse de una vez")
    pares = [
        ("Portal", "Estadio"),
        ("Portal", "Terminal"),
        ("Museo", "Terminal"),
        ("Calle26", "Parque"),
        ("Universidad", "Portal"),
    ]
    filas = comparar_rutas(grafo_antes, grafo_despues, pares)
    verificar("  cantidad de pares comparados", len(filas), 5)
    print()

    # Crea un grafo simple para verificar que el algoritmo detecte una desconexión
    print("Prueba 6: el programa debe detectar cuando un cierre desconecta un par")

    # Grafo lineal: X - Y - Z
    grafo_lineal = {
        "X": {"Y": 1},
        "Y": {"X": 1, "Z": 1},
        "Z": {"Y": 1},
    }

    # Elimina el vértice central Y
    grafo_lineal_sin_y = eliminar_vertice(grafo_lineal, "Y")

    filas = comparar_rutas(grafo_lineal, grafo_lineal_sin_y, [("X", "Z")])
    _, _, _, despues, _, estado = filas[0]
    verificar("  X -> Z queda desconectado", despues, None)
    verificar("  estado", estado, "Desconectado")
    print()


if __name__ == "__main__":
    ejecutar_pruebas()