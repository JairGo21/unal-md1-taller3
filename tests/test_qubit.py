import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from math import isclose

from src.cuantica.simulador import (
    aplicar_compuerta,
    calcular_probabilidades,
    obtener_compuertas
)


def ejecutar_prueba(nombre, funcion, datos):

    print(f"\n{'=' * 18}")
    print(nombre)
    print("=" * 18)
    print(f"Datos: {datos}")

    try:
        funcion()
        print("✓ Prueba superada.")

    except AssertionError as e:
        print("✗ Fallo una comprobacion.")
        print(e)

    except Exception as e:
        print("✗ Error inesperado.")
        print(e)


def prueba_compuerta_x():

    compuertas = obtener_compuertas()

    estado = [1, 0]

    estado = aplicar_compuerta(
        estado,
        compuertas["X"]
    )

    assert isclose(estado[0], 0.0, abs_tol=1e-9)
    assert isclose(estado[1], 1.0, abs_tol=1e-9)


def prueba_compuerta_h():

    compuertas = obtener_compuertas()

    estado = [1, 0]

    estado = aplicar_compuerta(
        estado,
        compuertas["H"]
    )

    p0, p1 = calcular_probabilidades(
        estado
    )

    assert isclose(p0, 0.5, abs_tol=1e-9)
    assert isclose(p1, 0.5, abs_tol=1e-9)


def prueba_doble_h():

    compuertas = obtener_compuertas()

    estado = [1, 0]

    estado = aplicar_compuerta(
        estado,
        compuertas["H"]
    )

    estado = aplicar_compuerta(
        estado,
        compuertas["H"]
    )

    assert isclose(estado[0], 1.0, abs_tol=1e-9)
    assert isclose(estado[1], 0.0, abs_tol=1e-9)


def prueba_compuerta_z():

    compuertas = obtener_compuertas()

    estado = [1, 0]

    estado = aplicar_compuerta(
        estado,
        compuertas["Z"]
    )

    assert isclose(estado[0], 1.0, abs_tol=1e-9)
    assert isclose(estado[1], 0.0, abs_tol=1e-9)


if __name__ == "__main__":

    ejecutar_prueba(
        "Compuerta X",
        prueba_compuerta_x,
        "Estado inicial: [1, 0]"
    )

    ejecutar_prueba(
        "Compuerta H",
        prueba_compuerta_h,
        "Estado inicial: [1, 0]"
    )

    ejecutar_prueba(
        "Doble compuerta H",
        prueba_doble_h,
        "Estado inicial: [1, 0]"
    )

    ejecutar_prueba(
        "Compuerta Z",
        prueba_compuerta_z,
        "Estado inicial: [1, 0]"
    )

    print("\nTodas las pruebas finalizaron correctamente.")