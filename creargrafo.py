import xml.sax  # Importamos el módulo SAX para analizar XML basado en eventos

class GraphMLHandler(xml.sax.ContentHandler):  # Clase manejadora que define cómo procesar los eventos del XML
    def __init__(self):  # Constructor de la clase
        self.current_element = ''  # Elemento XML actual que se está procesando
        self.key_map = {}  # Diccionario para mapear keys a nombres de atributos
        self.node_attrs = {}  # Atributos temporales del nodo actual
        self.edge_attrs = {}  # Atributos temporales de la arista actual
        self.nodes = {}  # Diccionario final de nodos
        self.edges = []  # Lista final de aristas
        self.adjacency_list = {}  # Lista de adyacencias: diccionario con ID de nodo y sus vecinos
        self.data_key = ''  # Identificador del dato que se está leyendo
        self.node_id = ''  # ID del nodo actual
        self.edge_id = ''  # ID de la arista actual
        self.in_node = False  # Flag para saber si estamos dentro de un nodo
        self.in_edge = False  # Flag para saber si estamos dentro de una arista
        self.in_data = False  # Flag para saber si estamos dentro de un dato <data>
        self.data_value = ''  # Valor temporal del contenido del <data>

    def startElement(self, name, attrs):  # Método llamado al inicio de cada elemento XML
        self.current_element = name  # Guardamos el nombre del elemento actual
        if name == 'key':  # Si es una etiqueta <key>, mapeamos su id a un nombre de atributo
            key_id = attrs.get('id')
            attr_name = attrs.get('attr.name')
            if key_id and attr_name:
                self.key_map[key_id] = attr_name
        elif name == 'node':  # Si empieza un nodo
            self.in_node = True
            self.node_id = attrs.get('id')  # Guardamos el ID del nodo
            self.node_attrs = {'id': self.node_id}  # Inicializamos atributos del nodo
        elif name == 'edge':  # Si empieza una arista
            self.in_edge = True
            self.edge_id = attrs.get('id')  # Guardamos el ID de la arista
            source = attrs.get('source')
            target = attrs.get('target')
            self.edge_attrs = {'id': self.edge_id, 'source': source, 'target': target}
        elif name == 'data':  # Si empieza un dato dentro de <node> o <edge>
            self.in_data = True
            self.data_key = attrs.get('key')  # Guardamos qué key representa el dato
            self.data_value = ''  # Reiniciamos el contenido

    def characters(self, content):  # Método llamado al leer texto dentro de un elemento <data>
        if self.in_data:
            self.data_value += content  # Acumulamos texto del dato (puede venir en fragmentos)

    def endElement(self, name):  # Método llamado al final de un elemento XML
        if name == 'data':  # Terminó un bloque <data>
            self.in_data = False
            attr_name = self.key_map.get(self.data_key, self.data_key)  # Convertimos key en nombre legible
            value = self.data_value.strip()
            if self.in_node:  # Si estamos procesando un nodo
                self.node_attrs[attr_name] = value
            elif self.in_edge:  # Si es una arista
                self.edge_attrs[attr_name] = value
            self.data_value = ''  # Limpiamos el contenido leído
        elif name == 'node':  # Terminamos de procesar un nodo
            self.in_node = False
            node_id = self.node_attrs.get('id')
            osmid = self.node_attrs.get('osmid_original', '')
            lon = self.node_attrs.get('lon', '')
            lat = self.node_attrs.get('lat', '')
            self.nodes[node_id] = {'osmid': osmid, 'lon': lon, 'lat': lat}  # Guardamos info del nodo
            self.adjacency_list[node_id] = []  # Inicializamos su lista de vecinos
        elif name == 'edge':  # Terminamos de procesar una arista
            self.in_edge = False
            source = self.edge_attrs.get('source')
            target = self.edge_attrs.get('target')
            length = self.edge_attrs.get('length', '0')  # Usamos 0 si no hay longitud
            self.edges.append({'source': source, 'target': target, 'length': length})  # Añadimos a la lista de aristas
            if source in self.adjacency_list:  # Comprobamos si el nodo fuente ya tiene adyacencias
                self.adjacency_list[source].append((target, float(length)))  # Añadimos destino con coste
            else:
                self.adjacency_list[source] = [(target, float(length))]  # Creamos nueva lista de adyacencia

def parse_graphml(file_path):  # Función para parsear el fichero .graphml
    parser = xml.sax.make_parser()  # Creamos el parser SAX
    handler = GraphMLHandler()  # Instanciamos el manejador personalizado
    parser.setContentHandler(handler)  # Asignamos el manejador al parser
    parser.parse(file_path)  # Procesamos el fichero
    return handler.nodes, handler.edges, handler.adjacency_list  # Devolvemos resultado