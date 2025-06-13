#!/usr/bin/python3
# busqueda.py - Implementa el algoritmo de búsqueda A*

import heapq
from arbol_busqueda import NodoBusqueda
from utilidades import calcular_valor, heuristica_euclidea, heuristica_arco_minimo

def realizar_busqueda(planificador, estrategia, limite_profundidad, tipo_heuristica):
    # Inicializar estructuras principales
    camino = []              # Lista que almacenará los nodos recorridos hasta encontrar la solución
    frontera = []            # Cola de prioridad (heap) con los nodos por expandir
    heapq.heapify(frontera)  # Inicializa la frontera como un heap
    explorados = {}          # Diccionario para registrar estados ya visitados
    id_nodo = 0              # Contador de ID para los nodos del árbol de búsqueda
    objetivo_encontrado = False  # Flag para detener la búsqueda si se encuentra la solución

    # Calcular la heurística inicial según el tipo elegido, si no se usa A*
    heuristica_inicial = 0
    if tipo_heuristica == "euclidea" and estrategia != "a":
        heuristica_inicial = heuristica_euclidea(planificador, -1, planificador.estado_inicial)
    elif tipo_heuristica == "arco_minimo" and estrategia != "a":
        heuristica_inicial = heuristica_arco_minimo(planificador.grafo, planificador.estado_inicial)

    # Crear nodo raíz ficticio (sin estado) para facilitar la referencia en el árbol
    raiz = NodoBusqueda(None, None, None, 0, 0, 0, 0, None)
    
    # Crear nodo inicial con el estado inicial del problema
    nodo_inicial = NodoBusqueda(
        id_nodo,
        raiz,
        planificador.estado_inicial,
        calcular_valor(estrategia, None, 0, 0, heuristica_inicial),  # f(n)
        0,  # profundidad
        0,  # coste acumulado
        heuristica_inicial,  # h(n)
        None  # acción
    )
    heapq.heappush(frontera, nodo_inicial)  # Insertar en la frontera
    id_nodo += 1

    # Bucle principal de búsqueda
    while frontera and not objetivo_encontrado:
        actual = heapq.heappop(frontera)  # Extrae el nodo con menor valor (según la estrategia)
        camino.append(actual)             # Guarda el nodo expandido

        # Verificar si el nodo actual contiene un estado objetivo
        if planificador.es_objetivo(actual.estado):
            objetivo_encontrado = True
        else:
            # Expandir el nodo solo si no ha superado la profundidad máxima y no se ha explorado ya
            if actual.profundidad <= limite_profundidad and actual.estado.id_estado not in explorados:
                explorados[actual.estado.id_estado] = actual.estado
                sucesores = actual.estado.obtener_sucesores(planificador.grafo)

                # Crear nodos para cada sucesor del estado actual
                for nodo_origen, nuevo_estado, costo in sucesores:
                    h = 0
                    if tipo_heuristica == "euclidea":
                        h = heuristica_euclidea(planificador, heuristica_inicial, nuevo_estado)
                    elif tipo_heuristica == "arco_minimo":
                        h = heuristica_arco_minimo(planificador.grafo, nuevo_estado)
                    
                    accion = f"{nodo_origen}->{nuevo_estado.nodo_actual}"  # Descripción de la acción tomada

                    # Crear el nuevo nodo del árbol de búsqueda
                    nuevo_nodo = NodoBusqueda(
                        id_nodo,
                        actual,
                        nuevo_estado,
                        calcular_valor(estrategia, None, actual.profundidad + 1, actual.costo + float(costo), h),
                        actual.profundidad + 1,
                        actual.costo + float(costo),
                        h,
                        accion
                    )
                    id_nodo += 1
                    heapq.heappush(frontera, nuevo_nodo)  # Insertar en la frontera

    # Si se encuentra el objetivo, se reconstruye el camino. Si no, devuelve una lista vacía.
    return actual.obtener_camino() if objetivo_encontrado else []
