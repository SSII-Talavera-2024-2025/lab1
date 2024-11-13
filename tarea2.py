import xml.etree.ElementTree as ET
import hashlib

class Grafo:
    def __init__(self):
        self.nodos = {}
        self.arcos = []

    def agregar_nodo(self, id_nodo, lat, lon):
        self.nodos[id_nodo] = {'lat': lat, 'lon': lon}

    def agregar_arco(self, origen, destino, atributos):
        self.arcos.append({'origen': origen, 'destino': destino, **atributos})

    def obtener_sucesores(self, id_nodo):
        return sorted([arco['destino'] for arco in self.arcos if arco['origen'] == id_nodo])

    def __str__(self):
        return f"Grafo con {len(self.nodos)} nodos y {len(self.arcos)} arcos."

class Estado:
    def __init__(self, nodo_actual, nodos_por_visitar, grafo):
        self.nodo_actual = nodo_actual
        self.nodos_por_visitar = sorted(nodos_por_visitar)
        self.grafo = grafo
        self.id = self.generar_id_estado()

    def generar_id_estado(self):
        estado_str = f"({self.nodo_actual},[{','.join(map(str, self.nodos_por_visitar))}])"
        return hashlib.md5(estado_str.encode()).hexdigest()

    def calcular_sucesores(self):
        sucesores = []
        for nodo_destino in self.grafo.obtener_sucesores(self.nodo_actual):
            nueva_lista_por_visitar = [n for n in self.nodos_por_visitar if n != nodo_destino]
            nuevo_estado = Estado(nodo_destino, nueva_lista_por_visitar, self.grafo)
            accion = f"{self.nodo_actual}->{nodo_destino}"
            costo = 1
            sucesores.append((accion, nuevo_estado, costo))
        return sucesores

    def __str__(self):
        return f"Estado(nodo_actual={self.nodo_actual}, nodos_por_visitar={self.nodos_por_visitar}, id={self.id})"

def parsear_grafo(file_path):
    arbol = ET.parse(file_path)
    raiz = arbol.getroot()
    ns = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    grafo = Grafo()
    claves = {}
    
    for key in raiz.findall('graphml:key', ns):
        claves[key.get('id')] = key.get('attr.name')
    
    for nodo in raiz.findall('graphml:graph/graphml:node', ns):
        id_nodo = nodo.get('id')
        lat = None
        lon = None
        for data in nodo.findall('graphml:data', ns):
            if claves[data.get('key')] == 'Latitude':
                lat = data.text
            elif claves[data.get('key')] == 'Longitude':
                lon = data.text
        grafo.agregar_nodo(id_nodo, lat, lon)
    
    for arco in raiz.findall('graphml:graph/graphml:edge', ns):
        origen = arco.get('source')
        destino = arco.get('target')
        atributos = {}
        for data in arco.findall('graphml:data', ns):
            clave = claves[data.get('key')]
            atributos[clave] = data.text
        grafo.agregar_arco(origen, destino, atributos)
    
    return grafo

file_path = r"C:\Users\oussa\Desktop\TERCERO\TERCERO\PRIMER CUATRI\SSI\CR_Capital.xml"
grafo = parsear_grafo(file_path)
print(grafo)

nodo_inicial = '2'
nodos_por_visitar = ['11', '40', '50', '300']
estado_inicial = Estado(nodo_inicial, nodos_por_visitar, grafo)

sucesores = estado_inicial.calcular_sucesores()
print(f"Estado inicial: {estado_inicial}")

for accion, nuevo_estado, costo in sucesores:
    visitado_relevante = "!!! Aquí visitamos un nodo que queríamos" if nuevo_estado.nodo_actual in nodos_por_visitar else ""
    print(f"({accion}, ({nuevo_estado.nodo_actual},{nuevo_estado.nodos_por_visitar}), costo({estado_inicial.nodo_actual},{nuevo_estado.nodo_actual})) {visitado_relevante}")
