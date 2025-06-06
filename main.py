from graph import load_graph_from_graphml

def main():
    input_file = "CR_Capital.graphml"
    output_file = "pruebaT1.txt"

    nodes, adjacency_list = load_graph_from_graphml(input_file)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Todos los nodos:\n")
        for node_id, node in nodes.items():
            f.write(f"Nodo {node_id}: {node}\n")

        f.write("\nTodas las conexiones:\n")
        for source, edges in adjacency_list.items():
            for target, length in edges:
                f.write(f"{source} -> {target} (longitud: {length:.2f})\n")

    print(f"Resultado guardado en {output_file}")

if __name__ == "__main__":
   main()
