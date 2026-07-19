from src.cripto.cesar import cifrar, descifrar

def ejecutar_pruebas():

    print("========== PRUEBAS CIFRADO CESAR ==========\n")

    print("Prueba 1")
    print(cifrar("HOLA UNAL", 3))
    print()

    print("Prueba 2")
    print(cifrar("Hola Mundo!", 5))
    print()

    print("Prueba 3")
    print(cifrar("XYZ 2026", 4))
    print()

    print("Prueba 4")
    print(descifrar("KROD XQDO", 3))
    print()


if __name__ == "__main__":
    ejecutar_pruebas()