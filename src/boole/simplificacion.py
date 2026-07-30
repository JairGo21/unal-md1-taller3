"""
Matematicas Discretas I
Ejercicio 8 - Simplificacion de expresiones booleanas

Implementacion del algoritmo de Quine-McCluskey.
"""


def decimal_a_binario(numero, bits):
    #Convierte un numero decimal a binario con una cantidad fija de bits.
    

    return format(numero, f"0{bits}b")


def contar_unos(binario):
    #Cuenta la cantidad de unos de una cadena binaria.

    return binario.count("1")


def agrupar_minterminos(minterminos, bits):
    #Agrupa los minterminos segun la cantidad de unos

    grupos = {}

    for mintermino in sorted(minterminos):

        binario = decimal_a_binario(mintermino, bits)
        cantidad = contar_unos(binario)

        if cantidad not in grupos:
            grupos[cantidad] = []

        grupos[cantidad].append({
            "termino": binario,
            "minterminos": [mintermino],
            "combinado": False
        })

    return grupos


def imprimir_grupos(grupos):

    print("\nGrupos iniciales")
    print("-" * 40)

    for cantidad in sorted(grupos.keys()):

        print(f"\nGrupo {cantidad}:")

        for termino in grupos[cantidad]:
            print(
                f"{termino['termino']}   "
                f"{termino['minterminos']}"
            )

def diferencia_un_bit(termino1, termino2):
    #Verifica si dos terminos difieren en un solo bit.

    diferencias = 0
    resultado = ""

    for bit1, bit2 in zip(termino1, termino2):

        if bit1 == bit2:
            resultado += bit1

        else:
            diferencias += 1
            resultado += "-"

            if diferencias > 1:
                return False, ""

    return diferencias == 1, resultado


def combinar_grupos(grupos):
    #Combina grupos consecutivos y genera una nueva lista de grupos.


    nuevos_grupos = {}
    cantidades = sorted(grupos.keys())

    for i in range(len(cantidades) - 1):

        grupo_actual = grupos[cantidades[i]]
        grupo_siguiente = grupos[cantidades[i + 1]]

        for termino1 in grupo_actual:

            for termino2 in grupo_siguiente:

                combinar, nuevo_termino = diferencia_un_bit(
                    termino1["termino"],
                    termino2["termino"]
                )

                if combinar:

                    termino1["combinado"] = True
                    termino2["combinado"] = True

                    nuevo = {
                        "termino": nuevo_termino,
                        "minterminos": sorted(
                            termino1["minterminos"] +
                            termino2["minterminos"]
                        ),
                        "combinado": False
                    }

                    cantidad = contar_unos(
                        nuevo_termino.replace("-", "")
                    )

                    if cantidad not in nuevos_grupos:
                        nuevos_grupos[cantidad] = []

                    existe = False

                    for existente in nuevos_grupos[cantidad]:

                        if (
                            existente["termino"] == nuevo["termino"] and
                            existente["minterminos"] == nuevo["minterminos"]
                        ):
                            existe = True
                            break

                    if not existe:
                        nuevos_grupos[cantidad].append(nuevo)

    return nuevos_grupos


def obtener_implicantes_primos(grupos):
    #Obtiene los terminos que nunca fueron combinados.
    

    implicantes = []

    for grupo in grupos.values():

        for termino in grupo:

            if not termino["combinado"]:
                implicantes.append(termino)

    return implicantes


def imprimir_implicantes(implicantes):

    print("\nImplicantes primos")
    print("-" * 40)

    if not implicantes:
        print("No hay implicantes.")
        return

    for termino in implicantes:
        print(
            f"{termino['termino']} -> "
            f"{termino['minterminos']}"
        )

def generar_implicantes_primos(minterminos, bits):
    
    #Ejecuta todas las iteraciones del algoritmo hasta que no sea posible combinar mas terminos.

    grupos = agrupar_minterminos(minterminos, bits)
    implicantes_primos = []

    while True:

        nuevos_grupos = combinar_grupos(grupos)

        implicantes_primos.extend(
            obtener_implicantes_primos(grupos)
        )

        if not nuevos_grupos:
            break

        grupos = nuevos_grupos

    implicantes_unicos = []

    for implicante in implicantes_primos:

        existe = False

        for existente in implicantes_unicos:

            if (
                existente["termino"] == implicante["termino"] and
                existente["minterminos"] == implicante["minterminos"]
            ):
                existe = True
                break

        if not existe:
            implicantes_unicos.append(implicante)

    return implicantes_unicos


def construir_tabla_cobertura(implicantes, minterminos):
    #Construye la tabla de cobertura.

    tabla = {}

    for mintermino in minterminos:

        tabla[mintermino] = []

        for indice, implicante in enumerate(implicantes):

            if mintermino in implicante["minterminos"]:
                tabla[mintermino].append(indice)

    return tabla


def obtener_implicantes_esenciales(tabla):
    #Encuentra los implicantes primos esenciales.

    esenciales = []

    for implicantes in tabla.values():

        if len(implicantes) == 1:

            indice = implicantes[0]

            if indice not in esenciales:
                esenciales.append(indice)

    return esenciales

def seleccionar_implicantes_adicionales(
    implicantes,
    tabla,
    esenciales,
    minterminos
):
    #Selecciona implicantes adicionales para cubrir los minterminos que aun no estan cubiertos.
    

    cubiertos = set()

    for indice in esenciales:
        cubiertos.update(
            implicantes[indice]["minterminos"]
        )

    restantes = set(minterminos) - cubiertos

    seleccionados = list(esenciales)

    while restantes:

        mejor_indice = None
        mejor_cobertura = set()

        for indice, implicante in enumerate(implicantes):

            if indice in seleccionados:
                continue

            cobertura = (
                set(implicante["minterminos"])
                & restantes
            )

            if len(cobertura) > len(mejor_cobertura):
                mejor_indice = indice
                mejor_cobertura = cobertura

        if mejor_indice is None:
            break

        seleccionados.append(mejor_indice)
        restantes -= mejor_cobertura

    return seleccionados

def imprimir_tabla(tabla):

    print("\nTabla de cobertura")
    print("-" * 40)

    for mintermino in sorted(tabla.keys()):
        print(f"{mintermino}: {tabla[mintermino]}")

def termino_a_expresion(termino):
    """
    Convierte un termino binario a una expresion booleana.
    Ejemplo:
        1-0- -> AC'
    """

    variables = ["A", "B", "C", "D"]

    expresion = ""

    for indice, bit in enumerate(termino):

        if bit == "-":
            continue

        if bit == "1":
            expresion += variables[indice]

        else:
            expresion += variables[indice] + "'"

    if expresion == "":
        return "1"

    return expresion


def construir_expresion(implicantes, esenciales):
    
    #Construye la expresion simplificada.
    expresiones = []

    for indice in esenciales:
        expresiones.append(
            termino_a_expresion(
                implicantes[indice]["termino"]
            )
        )

    return " + ".join(expresiones)


def simplificar(minterminos, bits):

    implicantes = generar_implicantes_primos(
        minterminos,
        bits
    )

    tabla = construir_tabla_cobertura(
        implicantes,
        minterminos
    )

    esenciales = obtener_implicantes_esenciales(
        tabla
    )

    seleccionados = seleccionar_implicantes_adicionales(
        implicantes,
        tabla,
        esenciales,
        minterminos
    )

    expresion = construir_expresion(
        implicantes,
        seleccionados
    )

    return (
        implicantes,
        tabla,
        seleccionados,
        expresion
    )


def main():

    print("=" * 50)
    print("SIMPLIFICACION DE EXPRESIONES BOOLEANAS")
    print("=" * 50)

    try:

        bits = int(
            input("Numero de variables (3 o 4): ")
        )

        if bits not in [3, 4]:
            raise ValueError(
                "Solo se permiten 3 o 4 variables."
            )

        entrada = input(
            "Ingrese los minterminos separados por espacio: "
        )

        minterminos = sorted(
            list(
                map(int, entrada.split())
            )
        )

        limite = 2 ** bits

        for numero in minterminos:

            if numero < 0 or numero >= limite:
                raise ValueError(
                    f"El mintermino {numero} no es valido."
                )

        implicantes, tabla, seleccionados, expresion = simplificar(
            minterminos,    
            bits
        )

        print("\nImplicantes primos")
        print("-" * 50)

        for implicante in implicantes:
            print(
                f"{implicante['termino']} -> "
                f"{implicante['minterminos']}"
            )

        imprimir_tabla(tabla)

        print("\nImplicantes seleccionados")

        for indice in seleccionados:
            print(
                implicantes[indice]["termino"]
            )

        print("\nExpresion simplificada")   
        print("-" * 50)
        print(expresion)

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()