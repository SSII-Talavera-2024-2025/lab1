from creargrafo import parse_graphml

if __name__ == "__main__":
    # Cambia esto por el nombre de tu archivo
    file_path = 'CR_Capital.graphml'
    nodes, edges, adjacency_list = parse_graphml(file_path)

    with open("prueba.txt", "w", encoding="utf-8") as f:
        f.write("NODOS:\n")
        for node_id, info in nodes.items():
            f.write(f"{node_id}: OSMID={info['osmid']}, Lon={info['lon']}, Lat={info['lat']}\n")

        f.write("\nARISTAS:\n")
        for edge in edges:
            f.write(f"{edge['source']} -> {edge['target']} (Longitud: {edge['length']})\n")

        f.write("\nLISTA DE ADYACENCIA:\n")
        for node, neighbors in adjacency_list.items():
            f.write(f"{node}: {neighbors}\n")
  # imprimir resultados



        