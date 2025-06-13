
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

def heuristica_euclidea(planificador, heuristica_base, estado):
    # Heurística euclídea según la Tarea 4: min(D1, D2) * k
    grafo = planificador.grafo
    D1 = planificador.D1  # Distancia mínima entre nodos objetivo (precalculada)
    nodos_por_visitar = estado.nodos_por_visitar
    nodo_actual = int(estado.nodo_actual)
    k = len(nodos_por_visitar)

    if k == 0:
        return 0

    # Calcular D2: distancia mínima entre nodo_actual y nodos por visitar
    D2 = float('inf')
    for nodo in nodos_por_visitar:
        dist = distancia_entre_nodos(grafo, nodo_actual, nodo)
        D2 = min(D2, dist)

    return min(D1, D2) * k

def distancia_entre_nodos(grafo, nodo_a, nodo_b):
    # Distancia euclídea entre dos nodos
    x1, y1 = float(grafo.nodos[nodo_a].x), float(grafo.nodos[nodo_a].y)
    x2, y2 = float(grafo.nodos[nodo_b].x), float(grafo.nodos[nodo_b].y)
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def heuristica_arco_minimo(grafo, estado):
    # Heurística de arco mínimo: A1 * k
    return grafo.distancia_minima * len(estado.nodos_por_visitar)