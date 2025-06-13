import math
import xml.sax
from creargrafo import Grafo
from estado import Estado

class Problema:
    def __init__(self, archivo_xml, nodo_inicio, nodos_objetivo):
        self.archivo_xml = archivo_xml
        self.estado_inicial = Estado(nodo_inicio, nodos_objetivo)
        self.grafo = Grafo()
        
        # Parseamos el XML para construir el grafo
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        parser.setContentHandler(self.grafo)
        parser.parse(self.archivo_xml)

        # Calculamos la distancia mínima entre nodos objetivo (D1)
        self.D1 = self.calcular_D1(nodos_objetivo)

    def calcular_D1(self, nodos_objetivo):
        # Distancia euclídea mínima entre pares de nodos objetivo
        if len(nodos_objetivo) < 2:
            return float('inf')  # Si hay menos de 2, no tiene sentido calcular
        distancia_minima = float('inf')
        for i in range(len(nodos_objetivo)):
            for j in range(i + 1, len(nodos_objetivo)):
                x1, y1 = float(self.grafo.nodos[nodos_objetivo[i]].x), float(self.grafo.nodos[nodos_objetivo[i]].y)
                x2, y2 = float(self.grafo.nodos[nodos_objetivo[j]].x), float(self.grafo.nodos[nodos_objetivo[j]].y)
                dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                distancia_minima = min(distancia_minima, dist)
        return distancia_minima
    
    def es_objetivo(self, estado):
        # Verifica si ya visitamos todos los nodos objetivo
        return len(estado.nodos_por_visitar) == 0
