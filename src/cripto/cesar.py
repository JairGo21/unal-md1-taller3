def main():
    ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


    def desplazar_caracter(caracter: str, desplazamiento: int) -> str:
        """
        Desplaza un carácter dentro del alfabeto.
        Conserva espacios, números y signos.
        """

        if not caracter.isalpha():
            return caracter

        es_minuscula = caracter.islower()
        caracter = caracter.upper()

        indice = ALFABETO.index(caracter)
        nuevo_indice = (indice + desplazamiento) % len(ALFABETO)

        nuevo_caracter = ALFABETO[nuevo_indice]

        return nuevo_caracter.lower() if es_minuscula else nuevo_caracter


    def cifrar(texto: str, desplazamiento: int) -> str:
        """
        Cifra un texto utilizando el cifrado César.
        """
        return "".join(
            desplazar_caracter(caracter, desplazamiento)
            for caracter in texto
        )


    def descifrar(texto: str, desplazamiento: int) -> str:
        """
        Descifra un texto utilizando el desplazamiento contrario.
        """
        return cifrar(texto, -desplazamiento)


    def fuerza_bruta(texto: str) -> None:
        """
        Prueba todos los desplazamientos posibles.
        """

        print("\nPosibles descifrados:\n")

        for desplazamiento in range(26):
            print(
                f"Desplazamiento {desplazamiento:2}: "
                f"{descifrar(texto, desplazamiento)}"
            )

    #MENU QUE VERAN LOS USUARIOS/PERSONAS QUE USEN EL PROGRAMA

    while True:

        print("\n========== CIFRADO CESAR ==========")
        print("1. Cifrar")
        print("2. Descifrar")
        print("3. Fuerza bruta")
        print("4. Salir")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":

            texto = input("Texto: ")
            k = int(input("Desplazamiento: "))

            print("\nResultado:")
            print(cifrar(texto, k))

        elif opcion == "2":

            texto = input("Texto cifrado: ")
            k = int(input("Desplazamiento: "))

            print("\nResultado:")
            print(descifrar(texto, k))

        elif opcion == "3":

            texto = input("Texto cifrado: ")
            fuerza_bruta(texto)

        elif opcion == "4":

            print("Hasta luego.")
            break

        else:

            print("Opcion invalida.")


if __name__ == "__main__":
    main()


