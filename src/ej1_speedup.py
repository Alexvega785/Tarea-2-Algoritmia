"""Ejercicio 1: speedup del método Monte Carlo para estimar pi con 1, 2, 4 y 8 procesos."""
import os
import random
import time
from multiprocessing import Pool

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
N_TOTAL = 8_000_000          # muestras totales (se mantiene fijo: escalamiento fuerte)
PROCESOS = [1, 2, 4, 8]


def contar_aciertos(args):
    """Cuenta cuántos puntos aleatorios caen dentro del cuarto de círculo unitario."""
    n, semilla = args
    rng = random.Random(semilla)
    dentro = 0
    for _ in range(n):
        x, y = rng.random(), rng.random()
        if x * x + y * y <= 1.0:
            dentro += 1
    return dentro


def estimate_pi(n_total, n_procesos):
    """Reparte el trabajo entre n_procesos y devuelve (pi_estimado, tiempo_en_segundos)."""
    trozo = n_total // n_procesos
    tareas = [(trozo, 1000 + i) for i in range(n_procesos)]
    inicio = time.perf_counter()
    with Pool(n_procesos) as pool:
        aciertos = sum(pool.map(contar_aciertos, tareas))
    tiempo = time.perf_counter() - inicio
    return 4.0 * aciertos / (trozo * n_procesos), tiempo


def main():
    tiempos = {}
    print(f"CPUs disponibles: {os.cpu_count()}")
    for p in PROCESOS:
        pi_est, t = estimate_pi(N_TOTAL, p)
        tiempos[p] = t
        print(f"{p} procesos: pi ≈ {pi_est:.5f}  tiempo = {t:.3f} s")

    speedup = [tiempos[1] / tiempos[p] for p in PROCESOS]
    eficiencia = [s / p for s, p in zip(speedup, PROCESOS)]
    for p, s, e in zip(PROCESOS, speedup, eficiencia):
        print(f"p={p}: speedup={s:.2f}  eficiencia={e:.2f}")

    plt.figure(figsize=(7, 4.5))
    plt.plot(PROCESOS, speedup, "o-", label="Speedup medido")
    plt.plot(PROCESOS, PROCESOS, "k--", label="Speedup ideal")
    plt.xlabel("Número de procesos")
    plt.ylabel("Speedup = T1 / Tp")
    plt.title("Speedup de estimate_pi (Monte Carlo)")
    plt.xticks(PROCESOS)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    os.makedirs(SALIDA, exist_ok=True)
    plt.savefig(os.path.join(SALIDA, "speedup_plot.png"), dpi=150)


if __name__ == "__main__":
    main()
