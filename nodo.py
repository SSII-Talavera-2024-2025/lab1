class Nodo:
    contador_id = 0  # Contador estático para IDs únicos

    def __init__(self, estado, padre=None, accion=None, costo=0.0, profundidad=0, heuristica=0.0, valor=0.0):
        self.ID = Nodo.contador_id
        Nodo.contador_id += 1
        
        self.estado = estado
        self.padre = padre
        self.accion = accion  # Aquí accion parece ser el nodo destino (ID)
        self.costo = costo
        self.profundidad = profundidad
        self.heuristica = heuristica
        self.valor = valor
        
        # Asignar un ID incremental único
    def estado_hash(self):
        # Devuelve los últimos 6 caracteres del hash MD5 del estado
        return self.estado.id_estado()[-6:]
    
    def __str__(self):
        padre_id = self.padre.ID if self.padre is not None else 'None' 

        return (f"[{self.ID}][{self.costo:.2f},{self.estado},{self.estado_hash()},{padre_id},{self.accion},"
                f"{self.profundidad},{self.heuristica},{self.valor:.2f}]")

    def camino(self):
        nodo, camino = self, []
        while nodo:
            camino.append(nodo)
            nodo = nodo.padre
        camino.reverse()
        return camino

    def __lt__(self, otro):
        if self.valor == otro.valor:
            return self.ID < otro.ID
        return self.valor < otro.valor

