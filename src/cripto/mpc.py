# MPC: cada nota x se reparte en 3 numeros aleatorios a, b, c tales que (a + b + c) mod M == x. Asi, ningun
# servidor ve la nota completa, solo al juntar las sumas parciales de los tres servidores se recupera la suma total y el promedio.

import random

def repartir_nota(x: int, M: int) -> list[int]:
    # Parte una nota x en 3 numeros aleatorios tales que
    # (a + b + c) mod M == x. Asi ningun servidor puede reconstruir la nota
    # solo con ver su parte.
    a = random.randrange(0, M)
    b = random.randrange(0, M)
    c = (x - a - b) % M
    return [a, b, c]


def mpc(notas: list[int], M: int = 1000003):

    # Reparte cada nota entre 3 servidores, reconstruye solo la suma y el
    # promedio sin que ninguno tenga acceso a la lista original.

    if not notas:
        raise ValueError("La lista de notas no puede estar vacia")
    for n in notas:
        if not (0 <= n <= 50):
            raise ValueError(f"Cada nota debe estar entre 0 y 50, se recibió {n}")

    # Repartimos cada nota en 3 pedazos
    partes = [repartir_nota(n, M) for n in notas]

    # Cada columna es lo que veria un servidor: solo una fraccion de cada nota
    p1 = [x[0] for x in partes]
    p2 = [x[1] for x in partes]
    p3 = [x[2] for x in partes]

    # Cada servidor suma lo que le toco, sin saber nada de las notas completas
    t1 = sum(p1) % M
    t2 = sum(p2) % M
    t3 = sum(p3) % M

    # Al juntar las tres sumas parciales recuperamos la suma total (mod M)
    suma = (t1 + t2 + t3) % M
    promedio = suma / len(notas)

    return {
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "sumas_parciales": [t1, t2, t3],
        "suma": suma,
        "promedio": promedio,
    }


def pedir_notas() -> list[int]:
    # El usuario ingresa las notas una por una. Termina cuando escribe "fin".
    print("=" * 52)
    print("   MPC - Suma y promedio secreto de notas")
    print("=" * 52)
    print("Ingresa las notas una por una.")
    print("Escribe 'fin' cuando termines.\n")

    notas: list[int] = []
    while True:
        entrada = input(f"  Nota #{len(notas) + 1} o 'fin': ").strip()

        if entrada.lower() == "fin":
            if not notas:
                print(" --> Debes ingresar al menos una nota antes de terminar.\n")
                continue
            return notas

        try:
            n = int(entrada)
        except ValueError:
            print(" --> La nota debe ser un numero entero. Intenta de nuevo.\n")
            continue

        if not (0 <= n <= 50):
            print(" --> La nota debe estar entre 0 y 50. Intenta de nuevo.\n")
            continue

        notas.append(n)
        print(f"  -> Nota {n} agregada ({len(notas)} en total)\n")


def mostrar_resultado(notas: list[int], r: dict) -> None:
    # Imprime los resultados con un poco de formato para que se lean mejor
    ancho = 52
    print("\n" + "=" * ancho)
    print("  RESULTADO".center(ancho))
    print("=" * ancho)
    print(f"  Notas ingresadas : {notas}")
    print("-" * ancho)
    print("  Vista de cada servidor:")
    print(f"    Servidor 1 : {r['p1']}")
    print(f"    Servidor 2 : {r['p2']}")
    print(f"    Servidor 3 : {r['p3']}")
    print("-" * ancho)
    print(f"  Suma total        : {r['suma']}")
    print(f"  Promedio          : {round(r['promedio'], 2)}")
    print("=" * ancho + "\n")


def ejemplo() -> None:
    # Caso del enunciado: estas notas deberian dar suma 150 y promedio 37.5
    notas = [40, 35, 50, 25]
    r = mpc(notas)
    mostrar_resultado(notas, r)
    assert r["suma"] == 150
    assert r["promedio"] == 37.5
    print("--> Coincide con el ejemplo - suma: 150 y promedio: 37.5\n")


if __name__ == "__main__":
    print("=" * 52)
    print("   MPC - Suma y promedio secreto de notas")
    print("=" * 52)
    print("1. Ver ejemplo del enunciado [40,35,50,25]")
    print("2. Ingresar mis propias notas")

    opcion = input("\nElige una opcion [1/2]: ").strip()
    while opcion not in ("1", "2"):
        opcion = input("Opcion inválida. Elegir 1 o 2: ").strip()

    if opcion == "2":
        notas = pedir_notas()
        r = mpc(notas)
        mostrar_resultado(notas, r)
    else:
        ejemplo()

    input("Presiona Enter para salir...")