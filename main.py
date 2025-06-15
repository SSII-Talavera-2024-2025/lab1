#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Autor: Daniel Tomas Gallego - Implementación personal para resolver un problema de búsqueda en grafos
# Fecha: Junio 2025

from problema import Problema
from algoritmoBusqueda import realizar_busqueda

def validar_estrategia(estrategia):
    # Asegura que la estrategia elegida esté entre las permitidas
    estrategias_validas = {'bfs', 'dfs', 'coste_uniforme', 'A'}
    if estrategia not in estrategias_validas:
        raise ValueError(f"Estrategia no válida: '{estrategia}'. Debe ser una de: {', '.join(estrategias_validas)}")

def validar_heuristica(tipo_heuristica):
    # Validamos que la heurística esté entre las esperadas
    heuristicas_validas = {'euclidea', 'arco_minimo'}
    if tipo_heuristica not in heuristicas_validas:
        raise ValueError(f"Tipo de heurística no válido: '{tipo_heuristica}'. Debe ser una de: {', '.join(heuristicas_validas)}")

if __name__ == "__main__":
    # Configuración del problema
    archivo_grafo = 'CAMPUS_VIRTUAL.graphxml'
    nodo_inicio = '911'
    nodos_objetivo = [630, 937, 425]
    estrategia = 'dfs'  # soporta bfs, dfs, coste_uniforme Y A
    tipo_heuristica = 'arco_minimo'  # Puede ser 'euclidea' o 'arco_minimo'
    limite_profundidad = 1000

    # Validaciones antes de ejecutar
    validar_estrategia(estrategia)
    validar_heuristica(tipo_heuristica)

    # Creamos el problema y lanzamos la búsqueda
    planificador = Problema(archivo_grafo, nodo_inicio, nodos_objetivo)
    camino_solucion = realizar_busqueda(planificador, estrategia, limite_profundidad, tipo_heuristica)

    # Mostramos el camino si se encontró uno
    if not camino_solucion:
        print("No encontré un camino válido :(")
    else:
        for nodo in camino_solucion:
            print(nodo)
