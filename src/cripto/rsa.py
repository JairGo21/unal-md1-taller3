"""
Matematicas Discretas I
Ejercicio 2 - RSA de juguete

Implementación propia de:
- Verificación de primos.
- Algoritmo de Euclides.
- Euclides Extendido.
- Inverso modular.
- Generación de llaves RSA.
"""

def es_primo(numero):
    #Retorna True si el numero es primo.

    if numero < 2:
        return False

    if numero == 2:
        return True

    if numero % 2 == 0:
        return False

    divisor = 3

    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 2

    return True


def mcd(a, b):
    #Calcula el maximo común divisor.

    while b != 0:
        a, b = b, a % b

    return abs(a)


def euclides_extendido(a, b):
    # Calcula x, y tal que:
    # ax + by = mcd(a,b)

    if b == 0:
        return a, 1, 0

    mcd_actual, x1, y1 = euclides_extendido(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return mcd_actual, x, y


def inverso_modular(e, phi):
    #Calcula el inverso modular de e modulo phi.

    mcd_actual, x, _ = euclides_extendido(e, phi)

    if mcd_actual != 1:
        raise ValueError(
            #No existe inverso modular para ese valor de e.
        )

    return x % phi


def generar_claves(p, q, e):
    """
    Genera los parametros necesarios para RSA.
    Retorna un diccionario con:
        n
        phi
        e
        d
    """

    if not es_primo(p):
        raise ValueError(f"{p} no es un numero primo.")

    if not es_primo(q):
        raise ValueError(f"{q} no es un numero primo.")

    if p == q:
        raise ValueError("p y q deben ser diferentes.")

    n = p * q
    phi = (p - 1) * (q - 1)

    if not (1 < e < phi):
        raise ValueError(
            f"e debe cumplir 1 < e < {phi}."
        )

    if mcd(e, phi) != 1:
        raise ValueError(
            "e no es coprimo con φ(n)."
        )

    d = inverso_modular(e, phi)

    #Comprobación del inverso modular
    if (e * d) % phi != 1:
        raise ValueError(
            "Error al calcular el inverso modular."
        )

    return {
        "n": n,
        "phi": phi,
        "e": e,
        "d": d
    }


def cifrar(mensaje, llaves):
    #Cifra un mensaje entero.

    n = llaves["n"]
    e = llaves["e"]

    if mensaje < 0:
        raise ValueError(
            "El mensaje no puede ser negativo."
        )

    if mensaje >= n:
        raise ValueError(
            f"El mensaje debe ser menor que {n}."
        )

    return pow(mensaje, e, n)


def descifrar(cifrado, llaves):
    #Descifra un mensaje.

    return pow(
        cifrado,
        llaves["d"],
        llaves["n"]
    )

def mostrar_resultados(llaves, mensaje, cifrado, descifrado):
    #Imprime los resultados del proceso.

    print("\n" + "=" * 45)
    print("RESULTADOS")
    print("=" * 45)

    print(f"n      : {llaves['n']}")
    print(f"φ(n)   : {llaves['phi']}")
    print(f"e      : {llaves['e']}")
    print(f"d      : {llaves['d']}")

    print("\nMensaje original   :", mensaje)
    print("Mensaje cifrado    :", cifrado)
    print("Mensaje descifrado :", descifrado)

    if mensaje == descifrado:
        print("\n✓ El proceso se realizó correctamente.")
    else:
        print("\n✗ El mensaje recuperado no coincide con el original.")


def main():

    print("=" * 45)
    print("        RSA DE JUGUETE")
    print("=" * 45)

    try:
        p = int(input("Ingrese el primo p: "))
        q = int(input("Ingrese el primo q: "))
        e = int(input("Ingrese el exponente público e: "))
        mensaje = int(input("Ingrese el mensaje (entero): "))

        llaves = generar_claves(p, q, e)

        cifrado = cifrar(mensaje, llaves)
        descifrado = descifrar(cifrado, llaves)

        mostrar_resultados(
            llaves,
            mensaje,
            cifrado,
            descifrado
        )

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()