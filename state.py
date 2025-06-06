import hashlib

class Estado:
    def __init__(self, current_node, nodes_to_visit):
        self.current_node = str(current_node)
        self.nodes_to_visit = sorted(map(str, nodes_to_visit))

    def __str__(self):
        return f"({self.current_node},[{','.join(self.nodes_to_visit)}])"

    def id(self):
        state_str = str(self)
        return hashlib.md5(state_str.encode()).hexdigest()

    def es_objetivo(self):
        return len(self.nodes_to_visit) == 0

    def __eq__(self, other):
        return isinstance(other, Estado) and self.current_node == other.current_node and self.nodes_to_visit == other.nodes_to_visit

    def __hash__(self):
        return hash(self.id())

def sucesores(estado, graph):
    current = estado.current_node
    remaining = estado.nodes_to_visit.copy()

    vecinos = graph.get(current, [])
    # ✅ Orden numérico correcto de los nodos destino
    vecinos_ordenados = sorted(vecinos, key=lambda x: int(x[0]))

    successors = []

    for neighbor, cost in vecinos_ordenados:
        new_remaining = [n for n in remaining if n != neighbor]
        new_estado = Estado(neighbor, new_remaining)
        action = f"{current}->{neighbor}"
        successors.append((action, new_estado, cost))

    return successors

