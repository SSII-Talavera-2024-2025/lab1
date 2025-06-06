from collections import deque
from state import Estado

class Nodo:
    contador_id = 0

    def __init__(self, estado, padre=None, accion=None, costo=0, profundidad=0, heuristica=0, valor=0):
        self.id = Nodo.contador_id
        Nodo.contador_id += 1
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo = costo
        self.profundidad = profundidad
        self.heuristica = heuristica
        self.valor = valor

    def camino(self):
        nodo, camino = self, []
        while nodo:
            camino.append(nodo)
            nodo = nodo.padre
        return list(reversed(camino))

    def __str__(self):
        return f"[{self.id}][{self.costo},{self.estado.id()[-6:]},{self.padre.id if self.padre else None},{self.accion},{self.profundidad},{self.heuristica},{self.valor}]"

class Frontera:
    def __init__(self):
        self.lista = []

    def insertar(self, nodo):
        self.lista.append(nodo)
        self.lista.sort(key=lambda n: (n.valor, n.id))

    def extraer(self):
        return self.lista.pop(0)

    def esta_vacia(self):
        return len(self.lista) == 0

def algoritmo_busqueda(estado_inicial, graph, funcion_sucesores, estrategia="anchura", profundidad_max=20):
    frontera = Frontera()
    visitados = set()
    nodo_inicial = Nodo(estado_inicial, costo=0, profundidad=0)

    if estrategia == "anchura":
        nodo_inicial.valor = nodo_inicial.profundidad
    elif estrategia == "profundidad":
        nodo_inicial.valor = 1 / (nodo_inicial.profundidad + 1)
    elif estrategia == "costo":
        nodo_inicial.valor = nodo_inicial.costo

    frontera.insertar(nodo_inicial)

    while not frontera.esta_vacia():
        nodo_actual = frontera.extraer()

        if nodo_actual.estado.es_objetivo():
            return nodo_actual.camino()

        if nodo_actual.estado.id() in visitados:
            continue

        if nodo_actual.profundidad > profundidad_max:
            continue

        visitados.add(nodo_actual.estado.id())

        sucesores_estado = funcion_sucesores(nodo_actual.estado, graph)

        for accion, nuevo_estado, costo in sucesores_estado:
            nuevo_costo = nodo_actual.costo + costo
            nueva_profundidad = nodo_actual.profundidad + 1
            nuevo_nodo = Nodo(
                estado=nuevo_estado,
                padre=nodo_actual,
                accion=accion,
                costo=nuevo_costo,
                profundidad=nueva_profundidad
            )

            if estrategia == "anchura":
                nuevo_nodo.valor = nueva_profundidad
            elif estrategia == "profundidad":
                nuevo_nodo.valor = 1 / (nueva_profundidad + 1)
            elif estrategia == "costo":
                nuevo_nodo.valor = nuevo_costo

            frontera.insertar(nuevo_nodo)

    return None
