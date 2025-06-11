# problema.py

class Problema:
    def __init__(self, estado_inicial, adjacency_list, es_objetivo_func, heuristica_func=None):
        self.estado_inicial = estado_inicial
        self.adjacency_list = adjacency_list
        self.es_objetivo_func = es_objetivo_func
        self.heuristica_func = heuristica_func

    def es_objetivo(self, estado):
        return self.es_objetivo_func(estado)

    def calcular_heuristica(self, estado):
        if self.heuristica_func is not None:
            return self.heuristica_func(estado)
        return 0

    def obtener_sucesores(self, estado):
        return estado.sucesores(self.adjacency_list)
