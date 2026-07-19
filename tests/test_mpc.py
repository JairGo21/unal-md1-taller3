import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.cripto.mpc import mpc, repartir_nota


def ejecutar_pruebas():
    print("========== PRUEBAS MPC ==========\n")

    print("Prueba 1: Ejemplo enunciado")
    r = mpc([40, 35, 50, 25])
    print("Notas: [40, 35, 50, 25]")
    print("Suma:", r["suma"], "| Promedio:", r["promedio"])
    print()

    print("Prueba 2: Única nota")
    r = mpc([20])
    print("Notas: [20]")
    print("Suma:", r["suma"], "| Promedio:", r["promedio"])
    print()

    print("Prueba 3: Lista grande")
    notas = [10, 45, 30, 0, 50, 25, 33]
    r = mpc(notas)
    print("Notas:", notas)
    print("Suma:", r["suma"], "| Promedio:", round(r["promedio"], 2))
    print()

    print("Prueba 4: Vistas de los servidores")
    partes = repartir_nota(40, 1000003)
    print("Nota real: 40")
    print("Partes repartidas:", partes)
    print()


if __name__ == "__main__":
    ejecutar_pruebas()
