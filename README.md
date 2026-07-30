# Taller 3 - Programación Discreta

Repositorio correspondiente al Taller 3 de la asignatura **Matemáticas Discretas I** de la **Universidad Nacional de Colombia**.

El proyecto implementa en **Python** los diez ejercicios propuestos en el taller, organizados en las siguientes categorías:

- **Criptografía** --> César, RSA, MPC
- **Grafos** --> Dijkstra, cierre de estación, coloreo
- **Álgebra de Boole** --> tablas de verdad, simplificación por Karnaugh
- **Información y cómputo cuántico** --> entropía de Shannon, simulador de un qubit

## Integrantes
- Jair Gómez Narváez
- Aimer Esteban Garcia Rojas

## Lenguaje y herramientas

- **Lenguaje:** Python 3.
- **Librerías:** Solo la biblioteca estándar, incluyendo `csv`, `heapq`, `math`, `os`, `random`, `sys`, `tkinter`, `itertools`. Ver `requirements.txt`.
- **Control de versiones:** Git.
- **Editor:** Visual Studio Code.

## Cómo ejecutar

Los programas están pensados para correr directo desde la raíz del repositorio. La mayoría tiene un menú interactivo que arranca al ejecutar el archivo.

### Ejercicios individuales

```bash
python src/cripto/cesar.py
python src/cripto/rsa.py
python src/cripto/mpc.py
python src/grafos/dijkstra.py
python src/grafos/cierre.py
python src/grafos/coloreo.py
python src/boole/tablas.py
python src/boole/simplificacion.py
python src/informacion/shannon.py
python src/cuantica/simulador.py
```

### Editor visual de grafos Dijkstra

El editor visual `src/grafos/dijkstra_visual.py` abre una ventana con un lienzo donde se puede armar un grafo personalizado. Su objetivo es producir un archivo CSV que después podrá ser utilizado en los ejercicios 4, 5 y 6.

**Cómo acceder:**

- Directamente desde la terminal:

  ```bash
  python src/grafos/dijkstra_visual.py
  ```

- O desde el menú del ejercicio 4: al ejecutar `python src/grafos/dijkstra.py`, la opción 3 "Abrir interfaz gráfica" abre el editor.

**Cómo se usa:**

1. La barra superior tiene los modos de trabajo. Se cambia con los botones:
   - **Agregar vértice** — clic en el lienzo para colocar un vértice; te pide el nombre en un cuadro de diálogo.
   - **Agregar arista** — clic en un vértice y luego en otro; te pide el peso en un cuadro de diálogo.
   - **Calcular ruta** — clic en el origen y luego en el destino, aplica Dijkstra sobre lo que haya en el editor y resalta el camino más corto.
   - **Guardar CSV** — escribe el grafo en `src/grafos/datos/grafo_personalizado.csv` y, junto a él, las posiciones de cada vértice en `src/grafos/datos/grafo_personalizado_pos.csv`. Guardar las posiciones permite que al volver a abrir el grafo con **Cargar CSV** los vértices queden exactamente donde se dejaron, en vez de reacomodarse automáticamente.
   - **Cargar CSV** — recupera el último grafo guardado usando las posiciones guardadas; los vértices nuevos que no tengan posición se acomodan solos en círculo.
   - **Reiniciar** — borra todo para empezar uno nuevo.

2. Una vez guardado, el grafo queda disponible para los demás ejercicios.

**En qué ejercicios se aplica:**

- **Ejercicio 4 — Dijkstra (`src/grafos/dijkstra.py`):** la opción 3 del menú "Abrir interfaz gráfica" lanza el editor visual.
- **Ejercicio 5 — Cierre (`src/grafos/cierre.py`):** al elegir la opción 2 del menú principal, ofrece cargar el grafo personalizado desde el CSV guardado.
- **Ejercicio 6 — Coloreo (`src/grafos/coloreo.py`):** al elegir la opción 2 del menú principal, carga directamente el grafo personalizado.

En los tres casos, si el archivo `grafo_personalizado.csv` no existe todavía, el programa avisa y sugiere crearlo desde el editor.

### Pruebas

Cada ejercicio tiene su archivo de pruebas en `tests/`. Todos se pueden ejecutar directamente desde cualquier carpeta (agregan las rutas del proyecto internamente):

```bash
python tests/test_cesar.py
python tests/test_mpc.py
python tests/test_rsa.py
python tests/test_dijkstra.py
python tests/test_cierre.py
python tests/test_coloreo.py
python tests/test_tablas.py
python tests/test_simplificacion.py
python tests/test_shannon.py
python tests/test_qubit.py
```

## Ejercicios desarrollados

| # | Ejercicio | Módulo | Tests |
|---|-----------|--------|-------|
| 1 | Cifrado César | `src/cripto/cesar.py` | `tests/test_cesar.py` |
| 2 | RSA de juguete | `src/cripto/rsa.py` | `tests/test_rsa.py` |
| 3 | MPC básico | `src/cripto/mpc.py` | `tests/test_mpc.py` |
| 4 | Dijkstra (ruta más corta) | `src/grafos/dijkstra.py` | `tests/test_dijkstra.py` |
| 5 | Cierre de una estación | `src/grafos/cierre.py` | `tests/test_cierre.py` |
| 6 | Coloreo de grafos | `src/grafos/coloreo.py` | `tests/test_coloreo.py` |
| 7 | Tablas de verdad | `src/boole/tablas.py` | `tests/test_tablas.py` |
| 8 | Simplificación booleana | `src/boole/simplificacion.py` | `tests/test_simplificacion.py` |
| 9 | Entropía de Shannon | `src/informacion/shannon.py` | `tests/test_shannon.py` |
| 10 | Simulador de un qubit | `src/cuantica/simulador.py` | `tests/test_qubit.py` |
