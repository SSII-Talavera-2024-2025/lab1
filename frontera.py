import heapq

class Frontera:
    def __init__(self):
        # Lista que mantiene los nodos ordenados según prioridad (valor y ID)
        self._cola_prioridad = []

    def agregar(self, nodo):
        """
        Inserta un nodo en la frontera.
        Se ordena primero por valor y luego por ID para desempates.
        """
        heapq.heappush(self._cola_prioridad, (nodo.valor, nodo.ID, nodo))

    def sacar(self):
        """
        Extrae y retorna el nodo con la prioridad más alta (menor valor).
        Retorna None si la frontera está vacía.
        """
        if self.esta_vacia():
            return None
        return heapq.heappop(self._cola_prioridad)[2]

    def esta_vacia(self):
        """Indica si la frontera está vacía."""
        return len(self._cola_prioridad) == 0

    def tamano(self):
        """Devuelve el número de nodos en la frontera."""
        return len(self._cola_prioridad)
