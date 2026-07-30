from math import log2

#Compara la entropia de dos mensajes
def comparar_mensajes(mensaje1, mensaje2):

    frecuencias1 = calcular_frecuencias(mensaje1)
    probabilidades1 = calcular_probabilidades(frecuencias1)
    entropia1 = calcular_entropia(probabilidades1)

    frecuencias2 = calcular_frecuencias(mensaje2)
    probabilidades2 = calcular_probabilidades(frecuencias2)
    entropia2 = calcular_entropia(probabilidades2)

    print("\nComparacion de mensajes")
    print("-" * 40)

    print(f"Mensaje 1: {mensaje1}")
    print(f"Entropia : {entropia1:.6f} bits\n")

    print(f"Mensaje 2: {mensaje2}")
    print(f"Entropia : {entropia2:.6f} bits\n")

    if entropia1 > entropia2:
        print("El mensaje 1 tiene mayor entropia.")
        print("Porque presenta una distribucion mas variada de simbolos, lo que genera mayor incertidumbre.")

    elif entropia2 > entropia1:
        print("El mensaje 2 tiene mayor entropia.")
        print("Porque presenta una distribucion mas variada de simbolos, lo que genera mayor incertidumbre.")

    else:
        print("Los dos mensajes tienen la misma entropia.")
        print("Porque poseen una distribucion de probabilidades equivalente.")

def calcular_frecuencias(datos):
    #Cuenta la frecuencia de cada simbolo.
    

    frecuencias = {}

    for simbolo in datos:

        if simbolo in frecuencias:
            frecuencias[simbolo] += 1
        else:
            frecuencias[simbolo] = 1

    return frecuencias


def calcular_probabilidades(frecuencias):
    #Calcula la probabilidad de cada simbolo.
    

    total = sum(frecuencias.values())

    probabilidades = {}

    for simbolo, cantidad in frecuencias.items():
        probabilidades[simbolo] = cantidad / total

    return probabilidades


def calcular_entropia(probabilidades):
    #Calcula la entropia de Shannon.

    entropia = 0

    for probabilidad in probabilidades.values():

        if probabilidad > 0:
            entropia -= probabilidad * log2(probabilidad)

    return entropia

#Muestra los resultados obtenidos
def mostrar_resultados(frecuencias, probabilidades, entropia):

    print("\nFrecuencias")
    print("-" * 40)

    for simbolo, cantidad in sorted(frecuencias.items()):
        print(f"{simbolo}: {cantidad}")

    print("\nProbabilidades")
    print("-" * 40)

    for simbolo, probabilidad in sorted(probabilidades.items()):
        print(f"{simbolo}: {probabilidad:.4f}")

    print("\nEntropia")
    print("-" * 40)
    print(f"{entropia:.6f} bits")

    print("\nComparacion entre dos mensajes")

    mensaje1 = input(
        "Ingrese el primer mensaje: "
    ).strip()

    mensaje2 = input(
        "Ingrese el segundo mensaje: "
    ).strip()

    comparar_mensajes(
        mensaje1,
        mensaje2
    )

#Programa principal
def main():

    print("=" * 45)
    print("CALCULO DE LA ENTROPIA DE SHANNON")
    print("=" * 45)

    datos = input(
        "Ingrese la secuencia de simbolos: "
    ).strip()

    if len(datos) == 0:
        print("\nError: la secuencia no puede estar vacia.")
        return

    frecuencias = calcular_frecuencias(datos)

    probabilidades = calcular_probabilidades(
        frecuencias
    )

    entropia = calcular_entropia(
        probabilidades
    )

    mostrar_resultados(
        frecuencias,
        probabilidades,
        entropia
    )


if __name__ == "__main__":
    main()