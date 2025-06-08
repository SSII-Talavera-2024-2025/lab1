class Nodo:
    contador_id = -1  # contador global para asignar ID único a cada nodo

    def __init__(self, estado, padre=None, accion=None, profundidad=0, costo=0.0, heuristica=0.0, estrategia='anchura'):
        Nodo.contador_id += 1
        self.id = Nodo.contador_id  # ID único incremental
        self.padre = padre          # Nodo padre
        self.estado = estado        # Estado asociado
        self.accion = accion        # Acción que generó este nodo
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = heuristica
        self.valor = self.calcula_valor(estrategia)

    def calcula_valor(self, estrategia):
        if estrategia == 'anchura':
            return self.profundidad
        elif estrategia == 'profundidad':
            return 1 / (self.profundidad + 1)
        elif estrategia == 'costo_uniforme':
            return self.costo
        else:
            return self.costo  # valor por defecto

    def camino(self):
        nodo, camino = self, []
        while nodo:
            camino.append(nodo)
            nodo = nodo.padre
        camino.reverse()
        return camino

    def __str__(self):
        estado_id = self.estado.id_estado()[-6:]
        id_padre = self.padre.id if self.padre else None
        return f"[{self.id}][{self.costo},{estado_id},{id_padre},{self.accion},{self.profundidad},{self.heuristica},{self.valor}]"

    def __lt__(self, otro):
        if self.valor == otro.valor:
            return self.id < otro.id
        return self.valor < otro.valor