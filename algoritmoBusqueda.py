from frontera import Frontera
from nodo import Nodo
from conjuntoestadosvisitados import ConjuntoEstadosVisitados

def calcular_valor(estrategia, profundidad, costo, heuristica):
    if estrategia == 'anchura':
        return profundidad
    elif estrategia == 'profundidad':
        return 1 / (profundidad + 1)
    elif estrategia == 'costo_uniforme':
        return costo
    #elif estrategia == 'a_estrella':
        #return costo + heuristica
    else:
        return 0

def AlgoritmoBusqueda(problema, estrategia, profundidad_maxima):
    Nodo.contador_id = 0  # Reinicia contador de IDs (si tu clase Nodo lo usa)

    frontera = Frontera()
    visitados = ConjuntoEstadosVisitados()

    heuristica_inicial = problema.heuristica_func(problema.estado_inicial)
    valor_inicial = calcular_valor(estrategia, 0, 0.0, heuristica_inicial)

    nodo_inicial = Nodo(
        estado=problema.estado_inicial,
        padre=None,
        accion=None,
        profundidad=0,
        costo=0.0,
        heuristica=heuristica_inicial,
        valor=valor_inicial
    )

    frontera.insertar(nodo_inicial)
    visitados.agregar(problema.estado_inicial)

    while not frontera.esta_vacia():
        nodo = frontera.extraer()

        if problema.es_objetivo_func(nodo.estado):
            return nodo.camino()

        if nodo.profundidad < profundidad_maxima:
            sucesores = nodo.estado.sucesores(problema.adjacency_list)
            for accion, estado_suc, costo_suc in sucesores:
                if not visitados.contiene(estado_suc):
                    nueva_profundidad = nodo.profundidad + 1
                    nuevo_costo = nodo.costo + float(costo_suc)
                    nueva_heuristica = problema.heuristica_func(estado_suc)
                    nuevo_valor = calcular_valor(estrategia, nueva_profundidad, nuevo_costo, nueva_heuristica)

                    nodo_hijo = Nodo(
                        estado=estado_suc,
                        padre=nodo,
                        accion=accion,
                        profundidad=nueva_profundidad,
                        costo=nuevo_costo,
                        heuristica=nueva_heuristica,
                        valor=nuevo_valor
                    )

                    frontera.insertar(nodo_hijo)
                    visitados.agregar(estado_suc)

    return None
