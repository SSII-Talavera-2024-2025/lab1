#!/usr/bin/python3
# busqueda.py - Implementa el algoritmo de búsqueda A*

import heapq
from arbol_busqueda import NodoBusqueda
from utilidades import calcular_valor, heuristica_euclidea, heuristica_arco_minimo

def realizar_busqueda(planificador, estrategia, limite_profundidad, tipo_heuristica):
    # Inicializar las estructuras
    camino = []
    frontera = []
    heapq.heapify(frontera)
    explorados = {}
    id_nodo = 0
    objetivo_encontrado = False

    # Calcular la heurística inicial
    heuristica_inicial = 0
    if tipo_heuristica == "euclidea" and estrategia != "A":
        heuristica_inicial = heuristica_euclidea(planificador, -1, planificador.estado_inicial)
    elif tipo_heuristica == "arco_minimo" and estrategia != "A":
        heuristica_inicial = heuristica_arco_minimo(planificador.grafo, planificador.estado_inicial)

    # Nodo raíz ficticio
    raiz = NodoBusqueda(None, None, None, 0, 0, 0, 0, None)
    
    # Nodo inicial
    nodo_inicial = NodoBusqueda(
        id_nodo, raiz, planificador.estado_inicial,
        calcular_valor(estrategia, None, 0, 0, heuristica_inicial),
        0, 0, heuristica_inicial, None
    )
    heapq.heappush(frontera, nodo_inicial)
    id_nodo += 1

    while frontera and not objetivo_encontrado:
        actual = heapq.heappop(frontera)
        camino.append(actual)

        if planificador.es_objetivo(actual.estado):
            objetivo_encontrado = True
        else:
            if actual.profundidad <= limite_profundidad and actual.estado.id_estado not in explorados:
                explorados[actual.estado.id_estado] = actual.estado
                sucesores = actual.estado.obtener_sucesores(planificador.grafo)

                for nodo_origen, nuevo_estado, costo in sucesores:
                    h = 0
                    if tipo_heuristica == "euclidea":
                        h = heuristica_euclidea(planificador, heuristica_inicial, nuevo_estado)
                    elif tipo_heuristica == "arco_minimo":
                        h = heuristica_arco_minimo(planificador.grafo, nuevo_estado)
                    
                    accion = f"{nodo_origen}->{nuevo_estado.nodo_actual}"
                    nuevo_nodo = NodoBusqueda(
                        id_nodo, actual, nuevo_estado,
                        calcular_valor(estrategia, None, actual.profundidad + 1, actual.costo + float(costo), h),
                        actual.profundidad + 1, actual.costo + float(costo), h, accion
                    )
                    id_nodo += 1
                    heapq.heappush(frontera, nuevo_nodo)

    return actual.obtener_camino() if objetivo_encontrado else []