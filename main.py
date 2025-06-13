#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Autor: [Tu Nombre] - Implementación personal para resolver un problema de búsqueda en grafos
# Fecha: Junio 2025
from problema import Problema
from algoritmoBusqueda import realizar_busqueda

if __name__ == "__main__":
    # Configuración del problema
    archivo_grafo = 'CAMPUS_VIRTUAL.graphxml'
    nodo_inicio = '911'
    nodos_objetivo = [630, 937, 425]
    estrategia = 'dfs'  # Usamos A, pero también soporta bfs, dfs, coste_uniforme
    tipo_heuristica = 'euclidea'  # Puede ser 'euclidea' o 'arco_minimo'
    limite_profundidad = 1000

    # Crear el planificador y buscar la solución
    planificador = Problema(archivo_grafo, nodo_inicio, nodos_objetivo)
    camino_solucion = realizar_busqueda(planificador, estrategia, limite_profundidad, tipo_heuristica)

    # Mostrar el resultado
    if not camino_solucion:
        print("No encontré un camino válido :(")
    else:
        for nodo in camino_solucion:
            print(nodo)