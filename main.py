from creargrafo import parse_graphml
from estado import Estado

if __name__ == "__main__":
    nodes, edges, adjacency_list = parse_graphml('CR_Capital.graphml')
    
    estado_inicial = Estado('70', ['68', '40', '50', '300'])
    
    with open("prueba2.txt", "w", encoding="utf-8") as f:
        f.write(f"Estado inicial: {estado_inicial}\n")
        f.write(f"ID del estado inicial: {estado_inicial.id_estado()}\n")

        if estado_inicial.es_objetivo():
            f.write("El estado inicial ya cumple el objetivo (todos los nodos visitados).\n")
        else:
            f.write("El estado inicial aún no cumple el objetivo (quedan nodos por visitar).\n")

        sucesores = estado_inicial.sucesores(adjacency_list)
        f.write("\nSucesores:\n")
        for accion, estado, costo in sucesores:
            f.write(f"{accion}: {estado} con costo {costo}\n")
