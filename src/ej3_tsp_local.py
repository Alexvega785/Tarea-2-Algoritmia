"""Ejercicio 3: búsqueda local 2-opt para el TSP."""
import math
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")


def distancia(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def longitud_ruta(ruta, ciudades):
    """Longitud total del ciclo cerrado."""
    return sum(distancia(ciudades[ruta[i]], ciudades[ruta[(i + 1) % len(ruta)]])
               for i in range(len(ruta)))


def dos_opt(ruta, ciudades):
    """2-opt: invierte segmentos mientras alguna inversión acorte la ruta (primera mejora)."""
    ruta = ruta[:]
    n = len(ruta)
    mejoro = True
    while mejoro:
        mejoro = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue  # mismas aristas del ciclo
                a, b = ciudades[ruta[i]], ciudades[ruta[i + 1]]
                c, d = ciudades[ruta[j]], ciudades[ruta[(j + 1) % n]]
                # cambia las aristas (a,b) y (c,d) por (a,c) y (b,d)
                if distancia(a, c) + distancia(b, d) < distancia(a, b) + distancia(c, d) - 1e-12:
                    ruta[i + 1:j + 1] = reversed(ruta[i + 1:j + 1])
                    mejoro = True
    return ruta


def main():
    rng = random.Random(7)
    n_ciudades, n_instancias = 30, 20
    antes, despues = [], []
    for _ in range(n_instancias):
        ciudades = [(rng.random(), rng.random()) for _ in range(n_ciudades)]
        ruta = list(range(n_ciudades))
        rng.shuffle(ruta)
        antes.append(longitud_ruta(ruta, ciudades))
        despues.append(longitud_ruta(dos_opt(ruta, ciudades), ciudades))

    mejora = [100 * (a - d) / a for a, d in zip(antes, despues)]
    print(f"Mejora promedio de 2-opt: {sum(mejora)/len(mejora):.1f}%")

    x = range(1, n_instancias + 1)
    plt.figure(figsize=(9, 4.5))
    plt.bar([i - 0.2 for i in x], antes, width=0.4, label="Ruta aleatoria inicial")
    plt.bar([i + 0.2 for i in x], despues, width=0.4, label="Después de 2-opt")
    plt.xlabel("Instancia (30 ciudades)")
    plt.ylabel("Longitud de la ruta")
    plt.title("TSP: mejora lograda por 2-opt")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    os.makedirs(SALIDA, exist_ok=True)
    plt.savefig(os.path.join(SALIDA, "tsp_improvements.png"), dpi=150)


if __name__ == "__main__":
    main()
