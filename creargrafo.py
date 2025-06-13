import xml.sax
from nodo import Nodo
from arista import Arista
import sys

class Grafo(xml.sax.ContentHandler):
    def __init__(self):
        self.dirigido = ""  # Indica si el grafo es dirigido o no
        self.distancia_minima = sys.float_info.max  # Guardamos la distancia más corta
        self.nodos = []         # Lista de objetos Nodo
        self.aristas = []       # Lista de objetos Arista
        self.adyacencias = []   # Matriz de adyacencias como diccionario por nodo
        self.clave_actual = ""  # Etiqueta XML 'data' que estamos procesando

    def startElement(self, tag, attrs):
        if tag == "graph":
            self.dirigido = attrs["edgedefault"]
        
        if tag == "node":
            self.nodos.append(Nodo())
            self.nodos[-1].id = int(attrs["id"])
        
        if tag == "edge":
            # Solo creamos adyacencias al encontrar la primera arista
            if not self.aristas:
                self.adyacencias = [{} for _ in range(len(self.nodos))]
            self.aristas.append(Arista())
            arista = self.aristas[-1]
            arista.id = int(attrs["id"])
            arista.origen = int(attrs["source"])
            arista.destino = int(attrs["target"])
            
            # Añadimos la arista al mapa de adyacencias
            origen = arista.origen
            destino = arista.destino
            if destino in self.adyacencias[origen]:
                self.adyacencias[origen][destino].append(len(self.aristas) - 1)
            else:
                self.adyacencias[origen][destino] = [len(self.aristas) - 1]

        if tag == "data":
            self.clave_actual = attrs["key"]

    def endElement(self, tag):
        if tag == "data":
            self.clave_actual = ""

    def characters(self, content):
        # Guardamos coordenadas y distancia según la clave XML
        if self.clave_actual == "d5":
            self.nodos[-1].x = content
        elif self.clave_actual == "d6":
            self.nodos[-1].y = content
        elif self.clave_actual == "d8":
            self.nodos[-1].longitud = content
        elif self.clave_actual == "d9":
            self.nodos[-1].latitud = content
        elif self.clave_actual == "d17":
            try:
                distancia = float(content)
                self.aristas[-1].distancia = distancia
                self.distancia_minima = min(self.distancia_minima, distancia)
            except ValueError:
                print(f"Error: No se pudo convertir distancia '{content}' a float")
