"""Ejercicio 5: aproximación del TSP con el árbol de expansión mínima (MST).
Razón de aproximación = longitud(ruta MST) / longitud(ruta óptima), en 100 instancias de 9 ciudades."""
import itertools
import math
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")


def matriz_distancias(ciudades):
    n = len(ciudades)
    return [[math.hypot(ciudades[i][0] - ciudades[j][0], ciudades[i][1] - ciudades[j][1])
             for j in range(n)] for i in range(n)]


def mst_prim(d):
    """Árbol de expansión mínima con Prim. Devuelve lista de adyacencia."""
    n = len(d)
    en_arbol = {0}
    ady = {i: [] for i in range(n)}
    while len(en_arbol) < n:
        u, v = min(((u, v) for u in en_arbol for v in range(n) if v not in en_arbol),
                   key=lambda e: d[e[0]][e[1]])
        ady[u].append(v)
        ady[v].append(u)
        en_arbol.add(v)
    return ady


def ruta_mst(d):
    """Recorrido en preorden del MST (atajos): 2-aproximación para el TSP métrico."""
    ady = mst_prim(d)
    ruta, visto = [], set()

    def dfs(u):
        visto.add(u)
        ruta.append(u)
        for v in ady[u]:
            if v not in visto:
                dfs(v)
    dfs(0)
    return ruta


def longitud(ruta, d):
    return sum(d[ruta[i]][ruta[(i + 1) % len(ruta)]] for i in range(len(ruta)))


def optimo_fuerza_bruta(d):
    """Mejor ruta probando todas las permutaciones (fijando la ciudad 0): (n-1)! rutas."""
    n = len(d)
    return min(longitud((0,) + p, d) for p in itertools.permutations(range(1, n)))


def main():
    rng = random.Random(2024)
    razones = []
    for _ in range(100):
        ciudades = [(rng.random(), rng.random()) for _ in range(9)]
        d = matriz_distancias(ciudades)
        razones.append(longitud(ruta_mst(d), d) / optimo_fuerza_bruta(d))

    print(f"Razón de aproximación: promedio={sum(razones)/100:.3f}  "
          f"mínima={min(razones):.3f}  máxima={max(razones):.3f}  (cota teórica: 2)")

    plt.figure(figsize=(7, 4.5))
    plt.hist(razones, bins=15, edgecolor="black")
    plt.axvline(sum(razones) / 100, color="r", linestyle="--", label="Promedio")
    plt.xlabel("Longitud ruta MST / longitud óptima")
    plt.ylabel("Número de instancias")
    plt.title("Razón de aproximación MST (100 instancias, 9 ciudades)")
    plt.legend()
    plt.tight_layout()
    os.makedirs(SALIDA, exist_ok=True)
    plt.savefig(os.path.join(SALIDA, "mst_histogram.png"), dpi=150)


if __name__ == "__main__":
    main()
