from src.cripto.rsa import (
    generar_claves,
    cifrar,
    descifrar
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


def prueba_caso_taller():
    llaves = generar_claves(61, 53, 17)

    assert llaves["n"] == 3233
    assert llaves["phi"] == 3120
    assert llaves["d"] == 2753

    mensaje = 65

    cifrado = cifrar(mensaje, llaves)

    assert cifrado == 2790

    mensaje_recuperado = descifrar(cifrado, llaves)

    assert mensaje_recuperado == mensaje


def prueba_otro_caso():
    llaves = generar_claves(17, 11, 7)

    mensaje = 88

    cifrado = cifrar(mensaje, llaves)

    assert descifrar(cifrado, llaves) == mensaje


def prueba_p_no_primo():

    try:
        generar_claves(15, 53, 17)

    except ValueError:
        return

    raise AssertionError("No detecto que p no era primo.")


def prueba_q_no_primo():

    try:
        generar_claves(61, 25, 17)

    except ValueError:
        return

    raise AssertionError("No detecto que q no era primo.")


def prueba_primos_iguales():

    try:
        generar_claves(17, 17, 5)

    except ValueError:
        return

    raise AssertionError("Acepto dos primos iguales.")


def prueba_e_no_coprimo():

    try:
        generar_claves(61, 53, 12)

    except ValueError:
        return

    raise AssertionError("No detecto un e invalido.")


def prueba_mensaje_fuera_de_rango():

    llaves = generar_claves(61, 53, 17)

    try:
        cifrar(5000, llaves)

    except ValueError:
        return

    raise AssertionError("No detecto un mensaje fuera del rango.")


if __name__ == "__main__":

    ejecutar_prueba(
        "Caso obligatorio del taller",
        prueba_caso_taller,
        "p=61, q=53, e=17, mensaje=65"
    )

    ejecutar_prueba(
        "Otro caso valido",
        prueba_otro_caso,
        "p=17, q=11, e=7, mensaje=88"
    )

    ejecutar_prueba(
        "p no primo",
        prueba_p_no_primo,
        "p=15, q=53, e=17"
    )

    ejecutar_prueba(
        "q no primo",
        prueba_q_no_primo,
        "p=61, q=25, e=17"
    )

    ejecutar_prueba(
        "Primos iguales",
        prueba_primos_iguales,
        "p=17, q=17, e=5"
    )

    ejecutar_prueba(
        "e invalido",
        prueba_e_no_coprimo,
        "p=13, q=17, e=24"
    )

    ejecutar_prueba(
        "Mensaje fuera de rango",
        prueba_mensaje_fuera_de_rango,
        "p=61, q=53, e=17, mensaje=5000"
    )

    print("\nTodas las pruebas finalizaron correctamente.")