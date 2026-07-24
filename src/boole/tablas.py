from itertools import product

def expr1(A, B, C):
    return (A and B) or (not C)

def expr2(A, B, C):
    return (A ^ B) and C

def expr3(A, B, C):
    return (A or B) and (not A or C)


EXPRESIONES = [
    ("(A and B) or (not C)", expr1),
    ("(A xor B) and C", expr2),
    ("(A or B) and (not A or C)", expr3),
]


def mostrar_tabla(nombre, func):
    # Prueba las 8 combinaciones de A,B,C (2^3) y las imprime en forma de tabla
    print(f"\nTabla de verdad: {nombre}")
    print("+-----+-----+-----+-----------+")
    print("|  A  |  B  |  C  | Resultado |")
    print("+-----+-----+-----+-----------+")
    for A, B, C in product([True, False], repeat=3):
        resultado = func(A, B, C)
        letras = ["V" if v else "F" for v in (A, B, C)]
        print(f"|  {letras[0]}  |  {letras[1]}  |  {letras[2]}  |     {'V' if resultado else 'F'}     |")
    print("+-----+-----+-----+-----------+")


def pedir_valor(nombre):
    while True:
        entrada = input(f"  {nombre} (V/F): ").strip().upper()
        if entrada in ("V", "F"):
            return entrada == "V"
        print("   --> Escribe V o F.")


if __name__ == "__main__":
    print("=" * 52)
    print("   Tablas de verdad")
    print("=" * 52)
    print("1. Ver las 3 tablas de verdad completas")
    print("2. Evaluar una expresión en una entrada especifica")

    opcion = input("\nElige una opcion [1/2]: ").strip()
    while opcion not in ("1", "2"):
        opcion = input("Opcion inválida. Elegir 1 o 2: ").strip()

    if opcion == "1":
        for nombre, func in EXPRESIONES:
            mostrar_tabla(nombre, func)
    else:
        print("\nExpresiones disponibles:")
        for i, (nombre, _) in enumerate(EXPRESIONES, start=1):
            print(f"  {i}. {nombre}")
        indice = input("Elige una expresión [1/2/3]: ").strip()
        while indice not in ("1", "2", "3"):
            indice = input("Opcion inválida. Elige 1, 2 o 3: ").strip()
        nombre, func = EXPRESIONES[int(indice) - 1]

        print()
        A = pedir_valor("A")
        B = pedir_valor("B")
        C = pedir_valor("C")
        resultado = func(A, B, C)
        print(f"\n{nombre} con A={A}, B={B}, C={C} => {'Verdadero' if resultado else 'Falso'}")

    input("\nPresiona Enter para salir...")