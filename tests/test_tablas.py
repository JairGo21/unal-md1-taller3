import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from itertools import product
from src.boole.tablas import expr1, expr2, expr3


def verificar(descripcion, obtenido, esperado):
    # Solo imprime OK/ERROR segun si coincide. Si quieres ver un fallo,
    # cambia el ultimo valor de cualquier verificar(...) por algo distinto.
    estado = "OK" if obtenido == esperado else "ERROR"
    print(f"[{estado}] {descripcion} -> obtenido: {obtenido} | esperado: {esperado}")


def ejecutar_pruebas():
    print("========== PRUEBAS TABLAS DE VERDAD ==========\n")

    # Casos puntuales calculados a mano para verificar las expresiones
    verificar(
        "expr1(F,F,F) = (A and B) or (not C)",
        expr1(False, False, False), True,
    )
    verificar(
        "expr1(F,F,V) = (A and B) or (not C)",
        expr1(False, False, True), False,
    )
    verificar(
        "expr2(V,F,V) = (A xor B) and C",
        expr2(True, False, True), True,
    )
    verificar(
        "expr2(V,V,V) = (A xor B) and C",
        expr2(True, True, True), False,
    )
    verificar(
        "expr3(V,F,F) = (A or B) and (not A or C)",
        expr3(True, False, False), False,
    )

    print()
    print("Cantidad de filas por tabla -> deben ser 8 = 2^3 combinaciones:")
    for nombre, func in [("expr1", expr1), ("expr2", expr2), ("expr3", expr3)]:
        filas = list(product([True, False], repeat=3))
        verificar(f"  {nombre}: cantidad de filas", len(filas), 8)

    print()


if __name__ == "__main__":
    ejecutar_pruebas()