from state import Estado, sucesores
from graph import load_graph_from_graphml
from search_algorithm import algoritmo_busqueda

def main():
    input_file = "CR_Capital.graphml"
    nodes, adjacency_list = load_graph_from_graphml(input_file)

    nodo_inicial = "673"
    nodos_a_visitar = ["775","1225", "951"]
    estado_inicial = Estado(nodo_inicial, nodos_a_visitar)

    print("🟢 Estado inicial:", estado_inicial)
    print("🔑 ID del estado:", estado_inicial.id())
    print("🌟 ¿Es objetivo?:", estado_inicial.es_objetivo())


    print("\n🚀 Ejecutando algoritmo de búsqueda...")
    solucion = algoritmo_busqueda(
        estado_inicial,
        adjacency_list,
        funcion_sucesores=sucesores,
        estrategia="anchura",
        profundidad_max=100
    )

    if solucion:
        print("\n✅ Camino solución:")
        for paso in solucion:
            print(paso)
    else:
        print("\n❌ No se encontró solución.")

if __name__ == "__main__":
    main()
