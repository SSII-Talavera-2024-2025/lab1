import heapq

class Frontera:
    def __init__(self):
        # Cola interna que almacenará los nodos ordenados por prioridad (valor, luego ID)
        self._elementos = []

    def agregar_nodo(self, nodo):
        """
        Añade un nodo a la frontera respetando la prioridad.
        Ordena por nodo.valor y en caso de empate, por nodo.ID.
        """
        prioridad = (nodo.valor, nodo.ID)
        heapq.heappush(self._elementos, (prioridad, nodo))

    def extraer_nodo(self):
        """
        Extrae el nodo con menor valor (mayor prioridad).
        Retorna None si la frontera está vacía.
        """
        if self.esta_vacia():
            return None
        # heapq devuelve (prioridad, nodo), extraemos solo el nodo
        return heapq.heappop(self._elementos)[1]

    def esta_vacia(self):
        """
        Verifica si la frontera no contiene nodos.
        """
        return len(self._elementos) == 0

    def cantidad(self):
        """
        Devuelve cuántos nodos hay en la frontera.
        """
        return len(self._elementos)
