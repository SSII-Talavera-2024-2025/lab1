# estado.py - Define un estado en la búsqueda (nodo actual y nodos por visitar)

import hashlib
from creargrafo import Grafo

class Estado:
    def __init__(self, nodo_actual, nodos_por_visitar):
        self.nodo_actual = nodo_actual
        self.nodos_por_visitar = sorted(nodos_por_visitar)  # Ordenamos para que sea consistente
        # Generar un identificador único con MD5
        cadena_estado = f"({self.nodo_actual},{self.nodos_por_visitar})".replace(" ", "")
        self.id_estado = hashlib.md5(cadena_estado.encode()).hexdigest()
        self.representacion = cadena_estado

    def __str__(self):
        return self.representacion

    def obtener_sucesores(self, grafo):
        """Devuelve los estados sucesores basados en los nodos vecinos."""
        sucesores = []
        vecinos = grafo.adyacencias[int(self.nodo_actual)]
        ids_vecinos = sorted(vecinos.keys())

        for id_vecino in ids_vecinos:
            for indice_arista in vecinos[id_vecino]:
                # Copiar la lista de nodos por visitar
                nuevos_nodos_por_visitar = self.nodos_por_visitar.copy()
                # Si el vecino es un nodo objetivo, lo quitamos de la lista
                if id_vecino in nuevos_nodos_por_visitar:
                    nuevos_nodos_por_visitar.remove(id_vecino)
                # Crear un nuevo estado
                nuevo_estado = Estado(id_vecino, nuevos_nodos_por_visitar)
                # Obtener la distancia de la arista
                distancia_arista = grafo.aristas[indice_arista].distancia
                # Añadir sucesor: [nodo_actual, nuevo_estado, costo]
                sucesores.append([self.nodo_actual, nuevo_estado, distancia_arista])

        return sucesores

    
