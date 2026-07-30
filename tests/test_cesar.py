import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from src.cripto.cesar import cifrar, descifrar


def ejecutar_pruebas():

    print("========== PRUEBAS DE CIFRADO ==========\n")

    # Prueba 1
    print("--Prueba 1--")
    print("Entrada : HOLA UNAL | k = 3")
    print("Salida  :", cifrar("HOLA UNAL", 3))
    print()

    # Prueba 2
    print("--Prueba 2--")
    print("Entrada : Hola Mundo! | k = 5")
    print("Salida  :", cifrar("Hola Mundo!", 5))
    print()

    # Prueba 3
    print("--Prueba 3--")
    print("Entrada : XYZ 2026 | k = 4")
    print("Salida  :", cifrar("XYZ 2026", 4))
    print()


    print("======== PRUEBAS DE DESCIFRADO ========\n")

    # Prueba 1
    print("--Prueba 1--")
    print("Entrada : KROD XQDO | k = 3")
    print("Salida  :", descifrar("KROD XQDO", 3))
    print()

    # Prueba 2
    print("--Prueba 2--")
    print("Entrada : Mtqf Rzsit! | k = 5")
    print("Salida  :", descifrar("Mtqf Rzsit!", 5))
    print()

    # Prueba 3
    print("--Prueba 3--")
    print("Entrada : BCD 2026 | k = 4")
    print("Salida  :", descifrar("BCD 2026", 4))
    print()


    print("=========== VERIFICACION ===========\n")

    # Si todo esto pasa, el cifrado/descifrado esta devolviendo lo que debe.
    assert cifrar("HOLA UNAL", 3) == "KROD XQDO"
    assert cifrar("Hola Mundo!", 5) == "Mtqf Rzsit!"
    assert cifrar("XYZ 2026", 4) == "BCD 2026"

    assert descifrar("KROD XQDO", 3) == "HOLA UNAL"
    assert descifrar("Mtqf Rzsit!", 5) == "Hola Mundo!"
    assert descifrar("BCD 2026", 4) == "XYZ 2026"

    print("Todas las pruebas fueron exitosas.")


if __name__ == "__main__":
    ejecutar_pruebas()