#!/usr/bin/python3
# arbol_busqueda.py - Representa un nodo en el árbol de búsqueda

class NodoBusqueda:
    def __init__(self, id, padre, estado, valor, profundidad, costo, heuristica, accion):
        self.id = id
        self.padre = padre
        self.estado = estado
        self.valor = valor
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = heuristica
        self.accion = accion

    def __str__(self):
        id_estado = self.estado.id_estado[-6:] if self.estado else "Ninguno"
        id_padre = self.padre.id if self.padre and self.padre.id is not None else "Ninguno"
        return f"[ID:{self.id}][Costo:{self.costo:.2f}, Estado:{self.estado}|{id_estado}, Padre:{id_padre}, Acción:{self.accion}, Profundidad:{self.profundidad}, H:{self.heuristica:.2f}, Valor:{self.valor}]"

    def __lt__(self, otro):
        if self.valor == otro.valor:
            return self.id < otro.id
        return self.valor < otro.valor

    def obtener_camino(self):
        camino = []
        actual = self
        while actual.id is not None:
            camino.append(actual)
            actual = actual.padre
        return camino[::-1]