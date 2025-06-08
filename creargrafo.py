import xml.sax

class GraphMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        # Elemento XML actual que se está procesando
        self.current_element = ''
        # Mapa que relaciona IDs de keys con nombres de atributos
        self.key_map = {}
        # Diccionarios temporales para atributos del nodo y la arista actuales
        self.node_attrs = {}
        self.edge_attrs = {}
        # Diccionario final de nodos, lista de aristas y lista de adyacencia
        self.nodes = {}
        self.edges = []
        self.adjacency_list = {}
        # Variables de control para datos que se están leyendo
        self.data_key = ''
        self.node_id = ''
        self.edge_id = ''
        self.in_node = False
        self.in_edge = False
        self.in_data = False
        self.data_value = ''

    def startElement(self, name, attrs):
        # Método llamado al encontrar el inicio de un elemento XML
        self.current_element = name

        if name == 'key':
            # Guardamos la relación entre el id de la key y el nombre del atributo
            key_id = attrs.get('id')
            attr_name = attrs.get('attr.name')
            if key_id and attr_name:
                self.key_map[key_id] = attr_name

        elif name == 'node':
            # Estamos entrando en un nodo: inicializamos variables
            self.in_node = True
            self.node_id = attrs.get('id')
            self.node_attrs = {'id': self.node_id}

        elif name == 'edge':
            # Estamos entrando en una arista: guardamos id, origen y destino
            self.in_edge = True
            self.edge_id = attrs.get('id')
            source = attrs.get('source')
            target = attrs.get('target')
            self.edge_attrs = {'id': self.edge_id, 'source': source, 'target': target}

        elif name == 'data':
            # Estamos dentro de un elemento <data>: guardamos el key y preparamos para leer valor
            self.in_data = True
            self.data_key = attrs.get('key')
            self.data_value = ''

    def characters(self, content):
        # Método que se llama cuando se encuentran caracteres de texto dentro de un elemento
        if self.in_data:
            # Acumulamos el contenido del dato
            self.data_value += content

    def endElement(self, name):
        # Método llamado al cerrar un elemento XML
        if name == 'data':
            # Finaliza la lectura de un dato: guardamos el valor en el atributo correspondiente
            self.in_data = False
            attr_name = self.key_map.get(self.data_key, self.data_key)
            value = self.data_value.strip()
            if self.in_node:
                # Si estamos dentro de un nodo, asignamos el atributo al nodo
                self.node_attrs[attr_name] = value
            elif self.in_edge:
                # Si estamos dentro de una arista, asignamos el atributo a la arista
                self.edge_attrs[attr_name] = value
            self.data_value = ''

        elif name == 'node':
            # Se cierra un nodo: extraemos sus atributos y lo añadimos a la colección de nodos
            self.in_node = False
            node_id = self.node_attrs.get('id')
            osmid = self.node_attrs.get('osmid_original', '')
            try:
                # Intentamos convertir latitud y longitud a float
                lon = float(self.node_attrs.get('lon', ''))
                lat = float(self.node_attrs.get('lat', ''))
                # Guardamos el nodo en el diccionario con su osmid y coordenadas
                self.nodes[node_id] = {'osmid': osmid, 'lon': lon, 'lat': lat}
                # Inicializamos lista vacía de adyacencia para este nodo
                self.adjacency_list[node_id] = []
            except ValueError:
                # Si no se pueden convertir coordenadas, ignoramos el nodo
                pass

        elif name == 'edge':
            # Se cierra una arista: extraemos atributos y la añadimos a la lista de aristas
            self.in_edge = False
            source = self.edge_attrs.get('source')
            target = self.edge_attrs.get('target')
            try:
                length = float(self.edge_attrs.get('length', '0'))
            except ValueError:
                length = 0.0
            # Añadimos la arista con origen, destino y longitud
            self.edges.append({'source': source, 'target': target, 'length': length})
            # Actualizamos la lista de adyacencia añadiendo el nodo destino y longitud a la lista del nodo origen
            if source in self.adjacency_list:
                self.adjacency_list[source].append((target, length))

def parse_graphml(file_path):
    # Función que crea el parser SAX, asigna el manejador personalizado y parsea el archivo
    parser = xml.sax.make_parser()
    handler = GraphMLHandler()
    parser.setContentHandler(handler)
    parser.parse(file_path)
    # Devuelve nodos, aristas y lista de adyacencia extraídos
    return handler.nodes, handler.edges, handler.adjacency_list
