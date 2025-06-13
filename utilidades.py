import math

def calcular_valor(estrategia, nodo, profundidad, costo, heuristica):
    # Devuelve el valor para ordenar nodos según la estrategia elegida
    if estrategia == "bfs":
        return profundidad  # Prioridad por nivel (anchura)
    elif estrategia == "dfs":
        return 1 / (profundidad + 1)  # Prioridad a nodos más profundos (profundidad inversa)
    elif estrategia == "coste_uniforme":
        return costo  # Prioridad según costo acumulado
    elif estrategia == "A":
        return costo + heuristica  # Suma costo + heurística (A*)
    return -1  # En caso de estrategia desconocida

def heuristica_euclidea(planificador, heuristica_base, estado):
    # Calcula la heurística Euclídea usada en la Tarea 4:
    # min(D1, D2) * k, donde D1 es distancia mínima entre objetivos, 
    # D2 es distancia actual a objetivos y k es nodos pendientes
    grafo = planificador.grafo
    D1 = planificador.D1
    nodos_por_visitar = estado.nodos_por_visitar
    nodo_actual = int(estado.nodo_actual)
    k = len(nodos_por_visitar)

    if k == 0:
        return 0  # Ya no quedan nodos por visitar

    # Calcular D2: mínima distancia del nodo actual a los nodos pendientes
    D2 = float('inf')
    for nodo in nodos_por_visitar:
        dist = distancia_entre_nodos(grafo, nodo_actual, nodo)
        D2 = min(D2, dist)

    return min(D1, D2) * k

def distancia_entre_nodos(grafo, nodo_a, nodo_b):
    # Calcula distancia Euclídea entre dos nodos del grafo
    x1, y1 = float(grafo.nodos[nodo_a].x), float(grafo.nodos[nodo_a].y)
    x2, y2 = float(grafo.nodos[nodo_b].x), float(grafo.nodos[nodo_b].y)
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def heuristica_arco_minimo(grafo, estado):
    # Heurística simple: distancia mínima encontrada en el grafo 
    # multiplicada por la cantidad de nodos que faltan visitar
    return grafo.distancia_minima * len(estado.nodos_por_visitar)
