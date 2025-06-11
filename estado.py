import hashlib  # Módulo para generar hashes MD5 únicos, útil para identificar estados

class Estado:
    def __init__(self, nodo_actual, lugares_por_visitar):
        self.nodo_actual = nodo_actual  # Nodo en el que se encuentra actualmente el agente
        self.lugares_por_visitar = list(lugares_por_visitar)  # Lista ordenada de lugares pendientes de visitar

    def __str__(self):
        # Devuelve una representación en cadena del estado, sin espacios
        # Por ejemplo: (A,['B','C'])
        return f"({self.nodo_actual},{self.lugares_por_visitar})"

    def id_estado(self):
        # Genera un identificador único MD5 a partir del string del estado
        # Útil para evitar visitar estados repetidos en algoritmos de búsqueda
        estado_str = str(self)  # Convierte el estado a string
        return hashlib.md5(estado_str.encode()).hexdigest()  # Genera y devuelve el hash MD5

    def sucesores(self, adjacency_list):
        # Genera los estados sucesores a partir de los vecinos del nodo actual
        sucesores = []  # Lista donde guardaremos los sucesores
        vecinos = adjacency_list.get(self.nodo_actual, [])  # Obtenemos los vecinos del nodo actual

        # Recorremos los vecinos ordenados por ID de destino
        for vecino, costo in sorted(vecinos, key=lambda x: x[0]):
            # Si el vecino es uno de los lugares por visitar, lo eliminamos en el nuevo estado
            if vecino in self.lugares_por_visitar:
                nuevos_lugares = [n for n in self.lugares_por_visitar if n != vecino]
            else:
                nuevos_lugares = list(self.lugares_por_visitar)  # Si no, mantenemos la lista igual

            # Creamos un nuevo estado a partir del vecino visitado
            nuevo_estado = Estado(vecino, nuevos_lugares)
            accion = f"{self.nodo_actual}->{vecino}"  # Acción realizada (por ejemplo, "A->B")
            sucesores.append((accion, nuevo_estado, costo))  # Añadimos tupla con acción, estado nuevo y coste

        return sucesores  # Devolvemos todos los sucesores posibles

    def es_objetivo(self):
        # Comprueba si el estado es objetivo: no quedan lugares por visitar
        return len(self.lugares_por_visitar) == 0

    
