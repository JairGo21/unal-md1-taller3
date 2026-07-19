import random

def repartir_nota(x: int, M: int) -> list[int]:
    # Parte una nota x en 3 numeros aleatorios
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

    partes = [repartir_nota(n, M) for n in notas]

    # Vista de cada servidor
    p1 = [x[0] for x in partes]
    p2 = [x[1] for x in partes]
    p3 = [x[2] for x in partes]

    # Cada servidor suma su columna sin saber las notas completas
    t1 = sum(p1) % M
    t2 = sum(p2) % M
    t3 = sum(p3) % M

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


if __name__ == "__main__":
    notas = [40, 35, 50, 25]
    r = mpc(notas)
    print("Notas:", notas)
    print("Vista servidor 1:", r["p1"])
    print("Vista servidor 2:", r["p2"])
    print("Vista servidor 3:", r["p3"])
    print("Suma reconstruida:", r["suma"])
    print("Promedio:", r["promedio"])
    assert r["suma"] == 150
    assert r["promedio"] == 37.5
    print("--> La suma y el promedio son correctos.")
    