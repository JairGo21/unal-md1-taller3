from itertools import product


def expr1(A, B, C):
    # (A and B) or (not C) -- las tres expresiones del enunciado
    return (A and B) or (not C)


def expr2(A, B, C):
    # (A xor B) and C
    return (A ^ B) and C


def expr3(A, B, C):
    # (A or B) and (not A or C)
    return (A or B) and (not A or C)


EXPRESIONES = [
    ("(A and B) or (not C)", expr1),
    ("(A xor B) and C", expr2),
    ("(A or B) and (not A or C)", expr3),
]

def normalizar(expresion):
    # Convierte la expresión a mayúsculas y adapta los operadores al formato de Python.
    expresion = expresion.upper()
    expresion = expresion.replace("XOR", "^")
    expresion = expresion.replace("AND", "and")
    expresion = expresion.replace("OR", "or")
    expresion = expresion.replace("NOT", "not")
    return expresion

def mostrar_tabla(nombre, func):
    # Prueba las 8 combinaciones de A,B,C y las imprime en forma de tabla
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


def elegir_variables():
    # El usuario marca con 1/0 cuales de A,B,C,D quiere usar.
    # Devuelve la lista de variables elegidas.
    print("Elegir variables a usar (1 = incluir, 0 = no incluir):")
    variables = []
    for letra in ("A", "B", "C", "D"):
        entrada = input(f"  Incluir {letra}? (1/0): ").strip()
        while entrada not in ("0", "1"):
            entrada = input("   --> Escribe 1 o 0: ").strip()
        if entrada == "1":
            variables.append(letra)
    # Si no eligió ninguna, le pedimos de nuevo
    if not variables:
        print("   --> Debes incluir al menos una variable.\n")
        return elegir_variables()
    return variables


def mostrar_tabla_personalizada(expresion, variables):
    # Genera la tabla de verdad para una expresion escrita por el usuario.
    columnas = variables + ["Resultado"]
    anchos = [max(len(c), 3) for c in columnas]
    separador = "+" + "+".join("-" * (a + 2) for a in anchos) + "+"

    print(f"\nTabla de verdad: {expresion}")
    print(separador)
    print("| " + " | ".join(c.center(a) for c, a in zip(columnas, anchos)) + " |")
    print(separador)
    # Pasamos AND/OR/NOT/XOR del usuario a la sintaxis de python
    expresion = normalizar(expresion)
    for combinacion in product([True, False], repeat=len(variables)):
        valores = dict(zip(variables, combinacion))
        try:
            resultado = eval(expresion, {"__builtins__": {}}, valores)
        except Exception as e:
            print(f"Error al evaluar la expresion: {e}")
            return
        letras = ["V" if valores[v] else "F" for v in variables]
        letras.append("V" if resultado else "F")
        print("| " + " | ".join(l.center(a) for l, a in zip(letras, anchos)) + " |")

    print(separador)


if __name__ == "__main__":
    print("=" * 52)
    print("   Tablas de verdad")
    print("=" * 52)
    print("1. Ver las 3 tablas de verdad completas")
    print("2. Evaluar una expresión en una entrada especifica")
    print("3. Crear tu propia expresión")

    opcion = input("\nElige una opción [1/2/3]: ").strip()
    while opcion not in ("1", "2", "3"):
        opcion = input("Opción inválida. Elegir 1, 2 o 3: ").strip()

    if opcion == "1":
        for nombre, func in EXPRESIONES:
            mostrar_tabla(nombre, func)

    elif opcion == "2":
        print("\nExpresiones disponibles:")
        for i, (nombre, _) in enumerate(EXPRESIONES, start=1):
            print(f"  {i}. {nombre}")
        indice = input("Elige una expresión [1/2/3]: ").strip()
        while indice not in ("1", "2", "3"):
            indice = input("Opción inválida. Elige 1, 2 o 3: ").strip()
        nombre, func = EXPRESIONES[int(indice) - 1]

        print()
        A = pedir_valor("A")
        B = pedir_valor("B")
        C = pedir_valor("C")
        resultado = func(A, B, C)
        print(f"\n{nombre} con A={A}, B={B}, C={C} => {'Verdadero' if resultado else 'Falso'}")

    else:
        variables = elegir_variables()
        print(f"\nVariables elegidas: {', '.join(variables)}")
        print("Escribe tu expresión usando AND, OR, NOT, XOR y/o Paréntesis")
        expresion = input("Tu expresión: ").strip()
        mostrar_tabla_personalizada(expresion, variables)

    input("\nPresiona Enter para salir...")