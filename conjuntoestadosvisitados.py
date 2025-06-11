class ConjuntoEstadosVisitados:
    def __init__(self):
        self.estados = {}

    def agregar(self, estado):
        self.estados[estado.id_estado()] = True

    def contiene(self, estado):
        return estado.id_estado() in self.estados
