#!/usr/bin/python3
# arbol_busqueda.py - Representa un nodo en el árbol de búsqueda

class NodoBusqueda:
    def __init__(self, id, padre, estado, valor, profundidad, costo, heuristica, accion):
        # Identificador único del nodo (para desempates)
        self.id = id
        # Nodo padre desde el que se generó este nodo
        self.padre = padre
        # Estado del problema asociado a este nodo
        self.estado = estado
        # Valor total del nodo (según estrategia: g, f, profundidad, etc.)
        self.valor = valor
        # Nivel de profundidad en el árbol
        self.profundidad = profundidad
        # Costo acumulado desde el inicio (g(n))
        self.costo = costo
        # Valor heurístico del nodo (h(n))
        self.heuristica = heuristica
        # Acción que llevó a este estado desde el padre
        self.accion = accion

    def __str__(self):
        # Representación legible del nodo (útil para depuración)
        id_estado = self.estado.id_estado[-6:] if self.estado else "Ninguno"
        id_padre = self.padre.id if self.padre and self.padre.id is not None else "Ninguno"
        return f"[ID:{self.id}][Costo:{self.costo:.2f}, Estado:{self.estado}|{id_estado}, Padre:{id_padre}, Acción:{self.accion}, Profundidad:{self.profundidad}, H:{self.heuristica:.2f}, Valor:{self.valor}]"

    def __lt__(self, otro):
        # Define la comparación para ordenar nodos en la frontera
        # Si el valor es el mismo, usa el id como desempate
        if self.valor == otro.valor:
            return self.id < otro.id
        return self.valor < otro.valor

    def obtener_camino(self):
        # Reconstruye el camino desde el nodo actual hasta la raíz
        camino = []
        actual = self
        while actual.id is not None:
            camino.append(actual)
            actual = actual.padre
        return camino[::-1]  # Se invierte para que el camino vaya desde el inicio hasta aquí
