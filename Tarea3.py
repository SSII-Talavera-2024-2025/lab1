import hashlib
import heapq
import xml.etree.ElementTree as ET

# Clase Nodo
class Nodo:
    contador_id = 0

    def __init__(self, estado, padre=None, accion=None, costo=0, heuristica=0):
        self.id = Nodo.contador_id
        Nodo.contador_id += 1
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.profundidad = padre.profundidad + 1 if padre else 0
        self.costo = costo
        self.heuristica = heuristica
        self.valor = 0  # Este valor se asignará según la estrategia

    def camino(self):
        nodo, camino = self, []
        while nodo:
            camino.append(nodo)
            nodo = nodo.padre
        return list(reversed(camino))

    def __repr__(self):
        estado_md5 = hashlib.md5(str(self.estado).encode()).hexdigest()[-6:]
        padre_id = self.padre.id if self.padre else None
        return f"[{self.id}][{self.costo:.2f},{estado_md5},{padre_id},{self.accion},{self.profundidad},{self.heuristica:.2f},{self.valor:.2f}]"

# Clase Frontera
class Frontera:
    def __init__(self):
        self.elementos = []  # Usamos un heap para mantener orden

    def insertar(self, nodo):
        heapq.heappush(self.elementos, (nodo.valor, nodo.id, nodo))

    def extraer(self):
        return heapq.heappop(self.elementos)[2] if self.elementos else None

    def vacia(self):
        return len(self.elementos) == 0

# Conjunto de Estados Visitados
class EstadosVisitados:
    def __init__(self):
        self.visitados = set()

    def agregar(self, estado):
        self.visitados.add(estado)

    def contiene(self, estado):
        return estado in self.visitados

# Función Algoritmo de Búsqueda
def algoritmo_busqueda(problema, estrategia, profundidad_maxima):
    frontera = Frontera()
    visitados = EstadosVisitados()

    nodo_inicial = Nodo(estado=problema.estado_inicial, costo=0, heuristica=0)
    frontera.insertar(nodo_inicial)

    while not frontera.vacia():
        nodo_actual = frontera.extraer()
        print(f"Expandiendo nodo: {nodo_actual}")

        if problema.es_objetivo(nodo_actual.estado):
            print("\nSolución encontrada:\n")
            for nodo in nodo_actual.camino():
                print(nodo)
            return nodo_actual.camino()

        if not visitados.contiene(nodo_actual.estado):
            visitados.agregar(nodo_actual.estado)
            for sucesor, costo, accion in problema.sucesores(nodo_actual.estado):
                print(f"Generando sucesor: Acción={accion}, Estado={sucesor}, Costo={costo}")
                nuevo_nodo = Nodo(
                    estado=sucesor,
                    padre=nodo_actual,
                    accion=accion,
                    costo=nodo_actual.costo + costo
                )

                if estrategia == "Anchura":
                    nuevo_nodo.valor = nuevo_nodo.profundidad
                elif estrategia == "Profundidad":
                    nuevo_nodo.valor = 1 / (nuevo_nodo.profundidad + 1)
                elif estrategia == "Costo Uniforme":
                    nuevo_nodo.valor = nuevo_nodo.costo

                frontera.insertar(nuevo_nodo)
        else:
            print(f"Se ignora nodo {nodo_actual} porque ya fue visitado.")

    print("No se encontró solución después de agotar la frontera.")
    return None

# Clase Problema
class Problema:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nodos = {}
        self.aristas = []
        self.estado_inicial = None
        self.estado_objetivo = None
        self.cargar_datos()

    def cargar_datos(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        # Namespaces en el archivo XML
        ns = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

        # Cargar nodos
        for nodo in root.findall('.//graphml:node', ns):
            nodo_id = nodo.attrib['id']
            self.nodos[nodo_id] = {
                'id': nodo_id,
                'data': {data.attrib['key']: data.text for data in nodo.findall('graphml:data', ns)}
            }

        # Cargar aristas
        for arista in root.findall('.//graphml:edge', ns):
            source = arista.attrib['source']
            target = arista.attrib['target']
            data = {data.attrib['key']: data.text for data in arista.findall('graphml:data', ns)}
            self.aristas.append({'source': source, 'target': target, 'data': data})

        # Establecer estado inicial y objetivo (puedes ajustarlo según el problema)
        self.estado_inicial = list(self.nodos.keys())[0]
        self.estado_objetivo = list(self.nodos.keys())[-1]

    def es_objetivo(self, estado):
        return estado == self.estado_objetivo

    def sucesores(self, estado):
        sucesores = []
        for arista in self.aristas:
            if arista['source'] == estado:
                sucesor = arista['target']
                costo = float(arista['data'].get('length', 1))  # Usar 'length' como costo si está disponible
                accion = f"{arista['source']}->{arista['target']}"
                sucesores.append((sucesor, costo, accion))
        return sucesores

# Ejecución del algoritmo
file_path = "/home/ice/Escritorio/SSI-24-25/CR_Capital.graphML.xml"
problema = Problema(file_path)

# Ejecutar con diferentes estrategias
print("\n--- Búsqueda en Anchura ---\n")
algoritmo_busqueda(problema, estrategia="Anchura", profundidad_maxima=50)

print("\n--- Búsqueda en Profundidad ---\n")
algoritmo_busqueda(problema, estrategia="Profundidad", profundidad_maxima=50)

print("\n--- Búsqueda de Costo Uniforme ---\n")
algoritmo_busqueda(problema, estrategia="Costo Uniforme", profundidad_maxima=50)
