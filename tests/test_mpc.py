import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.cripto.mpc import mpc, repartir_nota


def ejecutar_pruebas():
    print("========== PRUEBAS MPC ==========\n")

    print("Prueba 1: Ejemplo enunciado")
    r = mpc([40, 35, 50, 25])
    print("Notas: [40, 35, 50, 25]")
    print("Suma:", r["suma"], "| Promedio:", r["promedio"])
    print("OK" if r["suma"] == 150 and r["promedio"] == 37.5 else "Inválido - No coincide con el enunciado")
    print()

    print("Prueba 2: Única nota")
    r = mpc([20])
    print("Notas: [20]")
    print("Suma:", r["suma"], "| Promedio:", r["promedio"])
    print("OK" if r["suma"] == 20 and r["promedio"] == 20.0 else "Inválido")
    print()

    print("Prueba 3: Lista grande")
    notas = [10, 45, 30, 0, 50, 25, 33]
    r = mpc(notas)
    print("Notas:", notas)
    print("Suma:", r["suma"], "| Promedio:", round(r["promedio"], 2))
    print("OK" if r["suma"] == sum(notas) else "Inválido - Suma incorrecta")
    print()

    print("Prueba 4: Vistas de los servidores")
    # Sanity check: las tres partes sumadas (mod M) deben reconstruir la nota original
    partes = repartir_nota(40, 1000003)
    print("Nota real: 40")
    print("Partes repartidas:", partes)
    print("OK" if sum(partes) % 1000003 == 40 else "Inválido - Las partes no reconstruyen la nota")
    print()

    print("Prueba 5: Nota fuera de rango debe fallar")
    try:
        mpc([40, 99])
        print("Inválido - no lanzó excepción con una nota inválida")
    except ValueError as e:
        print("OK: se rechazó correctamente ->", e)
    print()

    print("Prueba 6: Lista vacia debe fallar")
    try:
        mpc([])
        print("Inválido - no lanzó excepción con lista vacía")
    except ValueError as e:
        print("OK: se rechazó correctamente ->", e)
    print()


if __name__ == "__main__":
    ejecutar_pruebas()
