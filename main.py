from state import Estado, sucesores
from graph import load_graph_from_graphml

def main():
    input_file = "CR_Capital.graphml"
    nodes, adjacency_list = load_graph_from_graphml(input_file)

    # ✅ Creamos un estado inicial real
    nodo_inicial = "1042"
    nodos_a_visitar = ["11", "40", "50", "300"]  # Usa nodos reales del grafo si puedes

    estado = Estado(nodo_inicial, nodos_a_visitar)

    print("🟢 Estado inicial:", estado)
    print("🔑 ID del estado:", estado.id())
    print("🎯 ¿Es objetivo?:", estado.es_objetivo())

    print("\n🔁 Sucesores desde el grafo real:")
    sucesores_generados = sucesores(estado, adjacency_list)

    for accion, nuevo_estado, coste in sucesores_generados:
        print(f"  Acción: {accion}, Estado nuevo: {nuevo_estado}, Costo: {coste}")

if __name__ == "__main__":
    main()