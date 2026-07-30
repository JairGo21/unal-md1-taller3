from math import isclose

from src.informacion.shannon import (
    calcular_frecuencias,
    calcular_probabilidades,
    calcular_entropia
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


def prueba_simbolos_equiprobables():

    datos = "ABCD"

    frecuencias = calcular_frecuencias(datos)
    probabilidades = calcular_probabilidades(frecuencias)
    entropia = calcular_entropia(probabilidades)

    assert isclose(entropia, 2.0, rel_tol=1e-9)


def prueba_un_solo_simbolo():

    datos = "AAAAAA"

    frecuencias = calcular_frecuencias(datos)
    probabilidades = calcular_probabilidades(frecuencias)
    entropia = calcular_entropia(probabilidades)

    assert isclose(entropia, 0.0, rel_tol=1e-9)


def prueba_dos_simbolos():

    datos = "AABB"

    frecuencias = calcular_frecuencias(datos)
    probabilidades = calcular_probabilidades(frecuencias)
    entropia = calcular_entropia(probabilidades)

    assert isclose(entropia, 1.0, rel_tol=1e-9)


def prueba_distribucion_desigual():

    datos = "AAAB"

    frecuencias = calcular_frecuencias(datos)
    probabilidades = calcular_probabilidades(frecuencias)
    entropia = calcular_entropia(probabilidades)

    assert isclose(entropia, 0.811278, rel_tol=1e-6)


if __name__ == "__main__":

    ejecutar_prueba(
        "Simbolos equiprobables",
        prueba_simbolos_equiprobables,
        'datos="ABCD"'
    )

    ejecutar_prueba(
        "Un solo simbolo",
        prueba_un_solo_simbolo,
        'datos="AAAAAA"'
    )

    ejecutar_prueba(
        "Dos simbolos",
        prueba_dos_simbolos,
        'datos="AABB"'
    )

    ejecutar_prueba(
        "Distribucion desigual",
        prueba_distribucion_desigual,
        'datos="AAAB"'
    )

    print("\nTodas las pruebas finalizaron correctamente.")