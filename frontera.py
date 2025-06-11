import heapq

class Frontera:
    def __init__(self):
        self._elementos = []

    def insertar(self, nodo):   # Cambié agregar_nodo -> insertar
        prioridad = (nodo.valor, nodo.ID)
        heapq.heappush(self._elementos, (prioridad, nodo))

    def extraer(self):          # Cambié extraer_nodo -> extraer
        if self.esta_vacia():
            return None
        return heapq.heappop(self._elementos)[1]

    def esta_vacia(self):
        return len(self._elementos) == 0

    def cantidad(self):
        return len(self._elementos)
