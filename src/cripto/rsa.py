from math import gcd


def es_primo(numero):
    #Verifica si un numero es primo.

    if numero < 2:
        return False

    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False

    return True


def euclides_extendido(a, b):
    #Algoritmo de Euclides Extendido.

    if b == 0:
        return a, 1, 0

    mcd, x1, y1 = euclides_extendido(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return mcd, x, y


def inverso_modular(e, phi):
    #Calcula el inverso modular de e modulo phi.

    mcd, x, _ = euclides_extendido(e, phi)

    if mcd != 1:
        return None

    return x % phi


def calcular_parametros(p, q, e):
    #Calcula n, phi y d.

    n = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        return None

    d = inverso_modular(e, phi)

    return n, phi, d


def cifrar(mensaje, e, n):
    return pow(mensaje, e, n)


def descifrar(cifrado, d, n):
    return pow(cifrado, d, n)


def main():

    print("=" * 40)
    print("        RSA DE JUGUETE")
    print("=" * 40)

    try:
        p = int(input("Ingrese el primo p: "))
        q = int(input("Ingrese el primo q: "))
        e = int(input("Ingrese el exponente publico e: "))
        mensaje = int(input("Ingrese el mensaje (entero): "))
    except ValueError:
        print("\nDebe ingresar únicamente numeros enteros.")
        return

    if not es_primo(p):
        print(f"\n{p} no es un numero primo.")
        return

    if not es_primo(q):
        print(f"\n{q} no es un numero primo.")
        return

    if p == q:
        print("\np y q deben ser primos diferentes.")
        return

    parametros = calcular_parametros(p, q, e)

    if parametros is None:
        print("\ne no es valido. Debe ser coprimo con φ(n).")
        return

    n, phi, d = parametros

    if e <= 1 or e >= phi:
        print(f"\ne debe cumplir 1 < e < {phi}.")
        return

    if mensaje < 0 or mensaje >= n:
        print(f"\nEl mensaje debe estar entre 0 y {n - 1}.")
        return

    cifrado = cifrar(mensaje, e, n)
    descifrado = descifrar(cifrado, d, n)

    print("\n------------- Parametros RSA -------------")
    print(f"n      = {n}")
    print(f"φ(n)   = {phi}")
    print(f"d      = {d}")

    print("\n------------- Resultado -------------")
    print(f"Mensaje original : {mensaje}")
    print(f"Mensaje cifrado  : {cifrado}")
    print(f"Mensaje recuperado: {descifrado}")

    if mensaje == descifrado:
        print("\nProceso completado correctamente.")
    else:
        print("\nOcurrio un error durante el descifrado.")


if __name__ == "__main__":
    main()