from creargrafo import parse_graphml
from estado import Estado
from problema import Problema
from algoritmoBusqueda import AlgoritmoBusqueda

def es_objetivo(estado):
    """Determina si el estado es objetivo."""
    return estado.es_objetivo()

def heuristica_ejemplo(estado):
    """
    Calcula una heurística simple.
    En este caso, el número de lugares por visitar.
    """
    return len(estado.lugares_por_visitar)

if __name__ == "__main__":
    # Carga del grafo desde el archivo .graphml
    nodes, edges, adjacency_list = parse_graphml('CR_Capital.graphml')

    # Definir el estado inicial (ejemplo: nodo '863' con objetivos)
    estado_inicial = Estado('1259', ['56', '1207', '379'])
    print("Estado inicial:", estado_inicial)
    print("ID del estado inicial:", estado_inicial.id_estado()) 

    # Verificación de si el estado ya cumple el objetivo
    if estado_inicial.es_objetivo():
        print("El estado inicial ya cumple el objetivo (todos los nodos visitados).")   
    else:
        print("El estado inicial aún no cumple el objetivo (quedan nodos por visitar).")

    # Definición del problema
    problema = Problema(
        estado_inicial=estado_inicial,
        adjacency_list=adjacency_list,
        es_objetivo_func=es_objetivo,
        heuristica_func=heuristica_ejemplo
    )

    # Selección de la estrategia de búsqueda
    estrategia = 'costo_uniforme'  # 'anchura', 'profundidad', 'a_estrella'

    # Límite de profundidad
    profundidad_maxima = 600    

    # Ejecución del algoritmo de búsqueda
    solucion = AlgoritmoBusqueda(problema, estrategia, profundidad_maxima)

    # Presentación de resultados
    if solucion:
        print("\nCamino solución encontrado:")
        for nodo in solucion:
                print(nodo)
    else:
        print("\nNo se encontró una solución dentro de la profundidad máxima permitida.")
