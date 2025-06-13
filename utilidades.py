
import math

def calcular_valor(estrategia, nodo, profundidad, costo, heuristica):
    # Calcula el valor de prioridad según la estrategia
    if estrategia == "bfs":
        return profundidad
    elif estrategia == "dfs":
        return 1 / (profundidad + 1)
    elif estrategia == "coste_uniforme":
        return costo
    elif estrategia == "A":
        return costo + heuristica
    return -1

