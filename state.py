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
    # Eliminamos el nodo actual porque ya lo visitamos
    if current in remaining:
        remaining.remove(current)

    adjacents = sorted([target for target, _ in graph.get(current, [])])
    successors = []

    for neighbor in adjacents:
        # En cada sucesor, los nodos pendientes serán 'remaining' (sin el current)
        new_estado = Estado(neighbor, remaining)
        action = f"{current}->{neighbor}"
        cost = next((length for tgt, length in graph[current] if tgt == neighbor), 1.0)
        successors.append((action, new_estado, cost))

    return successors