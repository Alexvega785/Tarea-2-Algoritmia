"""Ejercicio 4: recocido simulado (simulated annealing) con vecindario 2-opt para el TSP."""
import math
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ej3_tsp_local import dos_opt, longitud_ruta

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")


def recocido_simulado(ciudades, rng, t_inicial=1.0, enfriamiento=0.999, iteraciones=20000):
    """Devuelve (mejor_ruta, historial_costo_actual, historial_mejor_costo)."""
    n = len(ciudades)
    ruta = list(range(n))
    rng.shuffle(ruta)
    costo = longitud_ruta(ruta, ciudades)
    mejor_ruta, mejor_costo = ruta[:], costo
    hist_actual, hist_mejor = [costo], [mejor_costo]
    t = t_inicial
    for _ in range(iteraciones):
        i, j = sorted(rng.sample(range(n), 2))
        vecino = ruta[:i] + ruta[i:j + 1][::-1] + ruta[j + 1:]   # movimiento 2-opt aleatorio
        costo_vecino = longitud_ruta(vecino, ciudades)
        delta = costo_vecino - costo
        # acepta si mejora; si empeora, acepta con probabilidad exp(-delta / T)
        if delta < 0 or rng.random() < math.exp(-delta / t):
            ruta, costo = vecino, costo_vecino
            if costo < mejor_costo:
                mejor_ruta, mejor_costo = ruta[:], costo
        t *= enfriamiento
        hist_actual.append(costo)
        hist_mejor.append(mejor_costo)
    return mejor_ruta, hist_actual, hist_mejor


def main():
    rng = random.Random(11)
    ciudades = [(rng.random(), rng.random()) for _ in range(30)]

    ruta_2opt = dos_opt(random.Random(1).sample(range(30), 30), ciudades)
    costo_2opt = longitud_ruta(ruta_2opt, ciudades)

    plt.figure(figsize=(9, 4.5))
    finales = []
    for corrida in range(3):
        _, actual, mejor = recocido_simulado(ciudades, random.Random(100 + corrida))
        finales.append(mejor[-1])
        plt.plot(actual, alpha=0.35, linewidth=0.8)
        plt.plot(mejor, linewidth=1.8, label=f"Mejor costo, corrida {corrida + 1}")
    plt.axhline(costo_2opt, color="k", linestyle="--", label=f"2-opt solo ({costo_2opt:.2f})")
    plt.xlabel("Iteración")
    plt.ylabel("Longitud de la ruta")
    plt.title("Recocido simulado con 2-opt")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    os.makedirs(SALIDA, exist_ok=True)
    plt.savefig(os.path.join(SALIDA, "annealing_curves.png"), dpi=150)

    print(f"2-opt (búsqueda local): {costo_2opt:.3f}")
    print("Recocido simulado (3 corridas): " + ", ".join(f"{c:.3f}" for c in finales))


if __name__ == "__main__":
    main()
