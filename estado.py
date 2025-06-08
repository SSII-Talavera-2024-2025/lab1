import hashlib

class Estado:
    def __init__(self, nodo_actual, lugares_por_visitar):
        self.nodo_actual = nodo_actual
        self.lugares_por_visitar = sorted(lugares_por_visitar)  # ordenamos la lista como se exige

    def __str__(self):
        # Representación en formato estándar, sin espacios
        return f"({self.nodo_actual},{self.lugares_por_visitar})"

    def id_estado(self):
        # Genera el ID MD5 del estado como cadena
        estado_str = str(self)
        return hashlib.md5(estado_str.encode()).hexdigest()

    def sucesores(self, adjacency_list):
        sucesores = []
        vecinos = adjacency_list.get(self.nodo_actual, [])
        for vecino, costo in sorted(vecinos, key=lambda x: x[0]):  # orden por ID del nodo destino
            if vecino in self.lugares_por_visitar:
                nuevos_lugares = [n for n in self.lugares_por_visitar if n != vecino]
            else:
                nuevos_lugares = list(self.lugares_por_visitar)
            nuevo_estado = Estado(vecino, nuevos_lugares)
            accion = f"{self.nodo_actual}->{vecino}"
            sucesores.append((accion, nuevo_estado, costo))
        return sucesores

    def es_objetivo(self):
        return len(self.lugares_por_visitar) == 0


    
