"""Ejercicio 2: mochila 0/1 con heurística voraz por menor peso vs. solución óptima (programación dinámica)."""
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")


def knapsack_greedy_peso(pesos, valores, capacidad):
    """Voraz: ordena por menor peso y mete cada objeto mientras quepa."""
    orden = sorted(range(len(pesos)), key=lambda i: pesos[i])
    peso_total = valor_total = 0
    for i in orden:
        if peso_total + pesos[i] <= capacidad:
            peso_total += pesos[i]
            valor_total += valores[i]
    return valor_total


def knapsack_optimo(pesos, valores, capacidad):
    """Programación dinámica: valor máximo posible (referencia para comparar)."""
    dp = [0] * (capacidad + 1)
    for p, v in zip(pesos, valores):
        for c in range(capacidad, p - 1, -1):
            dp[c] = max(dp[c], dp[c - p] + v)
    return dp[capacidad]


def main():
    rng = random.Random(42)
    n_instancias, n_objetos = 30, 20
    voraz, optimo = [], []
    for _ in range(n_instancias):
        pesos = [rng.randint(1, 30) for _ in range(n_objetos)]
        valores = [rng.randint(1, 100) for _ in range(n_objetos)]
        capacidad = sum(pesos) // 3
        voraz.append(knapsack_greedy_peso(pesos, valores, capacidad))
        optimo.append(knapsack_optimo(pesos, valores, capacidad))

    razones = [v / o for v, o in zip(voraz, optimo)]
    print(f"Razón voraz/óptimo: promedio={sum(razones)/len(razones):.3f}  "
          f"mínima={min(razones):.3f}  máxima={max(razones):.3f}")
    print(f"Instancias donde el voraz fue óptimo: {sum(1 for r in razones if r == 1)} de {n_instancias}")

    x = range(1, n_instancias + 1)
    plt.figure(figsize=(9, 4.5))
    plt.bar([i - 0.2 for i in x], optimo, width=0.4, label="Óptimo (DP)")
    plt.bar([i + 0.2 for i in x], voraz, width=0.4, label="Voraz (menor peso)")
    plt.xlabel("Instancia")
    plt.ylabel("Valor total en la mochila")
    plt.title("Mochila: heurística voraz vs. óptimo")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    os.makedirs(SALIDA, exist_ok=True)
    plt.savefig(os.path.join(SALIDA, "knapsack_comparison.png"), dpi=150)


if __name__ == "__main__":
    main()
