from math import sqrt
from random import random


#Multiplica una matriz 2x2 por un vector
def multiplicar_matriz_vector(matriz, vector):

    return [
        matriz[0][0] * vector[0] + matriz[0][1] * vector[1],
        matriz[1][0] * vector[0] + matriz[1][1] * vector[1]
    ]


#Aplica una compuerta cuantica
def aplicar_compuerta(estado, compuerta):

    return multiplicar_matriz_vector(
        compuerta,
        estado
    )


#Calcula las probabilidades de medir 0 y 1
def calcular_probabilidades(estado):

    p0 = abs(estado[0]) ** 2
    p1 = abs(estado[1]) ** 2

    return p0, p1


#Simula varias mediciones
def simular_mediciones(estado, cantidad=1000):

    p0, p1 = calcular_probabilidades(
        estado
    )

    mediciones = {
        0: 0,
        1: 0
    }

    for _ in range(cantidad):

        if random() < p0:
            mediciones[0] += 1
        else:
            mediciones[1] += 1

    return mediciones


#Devuelve las compuertas cuanticas
def obtener_compuertas():

    raiz2 = sqrt(2)

    return {

        "X": [
            [0, 1],
            [1, 0]
        ],

        "Z": [
            [1, 0],
            [0, -1]
        ],

        "H": [
            [1 / raiz2, 1 / raiz2],
            [1 / raiz2, -1 / raiz2]
        ]
    }

#Muestra el estado del qubit
def mostrar_estado(estado):

    print("\nEstado del qubit")
    print("-" * 40)
    print(f"|0> : {estado[0]:.6f}")
    print(f"|1> : {estado[1]:.6f}")


#Muestra las probabilidades
def mostrar_probabilidades(estado):

    p0, p1 = calcular_probabilidades(
        estado
    )

    print("\nProbabilidades")
    print("-" * 40)
    print(f"P(0): {p0:.6f}")
    print(f"P(1): {p1:.6f}")


#Muestra el resultado de las mediciones
def mostrar_mediciones(mediciones):

    total = mediciones[0] + mediciones[1]

    print("\nMediciones")
    print("-" * 40)
    print(f"0: {mediciones[0]} ({mediciones[0] / total:.2%})")
    print(f"1: {mediciones[1]} ({mediciones[1] / total:.2%})")


#Programa principal
def main():

    print("=" * 45)
    print("SIMULADOR BASICO DE UN QUBIT")
    print("=" * 45)

    compuertas = obtener_compuertas()

    estado = [1, 0]

    mostrar_estado(estado)

    print("\nCompuertas disponibles: X Z H")

    secuencia = input(
        "Ingrese las compuertas separadas por espacio: "
    ).upper().split()

    for nombre in secuencia:

        if nombre not in compuertas:
            print(f"\nError: la compuerta {nombre} no existe.")
            return

        estado = aplicar_compuerta(
            estado,
            compuertas[nombre]
        )

    mostrar_estado(estado)

    mostrar_probabilidades(estado)

    mediciones = simular_mediciones(
        estado
    )

    mostrar_mediciones(
        mediciones
    )


if __name__ == "__main__":
    main()