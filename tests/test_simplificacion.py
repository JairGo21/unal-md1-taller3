import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.boole.simplificacion import simplificar


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


def prueba_una_variable():

    _, _, _, expresion = simplificar(
        [4, 5, 6, 7],
        3
    )

    assert expresion == "A"


def prueba_variable_negada():

    _, _, _, expresion = simplificar(
        [0, 1, 2, 3],
        3
    )

    assert expresion == "A'"


def prueba_todas_las_combinaciones():

    _, _, _, expresion = simplificar(
        list(range(8)),
        3
    )

    assert expresion == "1"


def prueba_un_mintermino():

    _, _, _, expresion = simplificar(
        [5],
        3
    )

    assert expresion == "AB'C"


def prueba_cuatro_variables():

    _, _, _, expresion = simplificar(
        [8, 9, 10, 11, 12, 13, 14, 15],
        4
    )

    assert expresion == "A"


if __name__ == "__main__":

    ejecutar_prueba(
        "Una variable",
        prueba_una_variable,
        "bits=3, minterminos=[4,5,6,7]"
    )

    ejecutar_prueba(
        "Variable negada",
        prueba_variable_negada,
        "bits=3, minterminos=[0,1,2,3]"
    )

    ejecutar_prueba(
        "Funcion constante",
        prueba_todas_las_combinaciones,
        "bits=3, minterminos=[0,1,2,3,4,5,6,7]"
    )

    ejecutar_prueba(
        "Un solo mintermino",
        prueba_un_mintermino,
        "bits=3, minterminos=[5]"
    )

    ejecutar_prueba(
        "Cuatro variables",
        prueba_cuatro_variables,
        "bits=4, minterminos=[8,9,10,11,12,13,14,15]"
    )

    print("\nTodas las pruebas finalizaron correctamente.")