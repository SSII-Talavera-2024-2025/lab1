import xml.sax

# Clase que maneja el contenido del archivo GraphML mientras se parsea.
class GraphMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        # Atributos principales
        self.nodes = {}         # Para almacenar los nodos
        self.edges = []         # Lista para almacenar las aristas
        self.current_node = None	 # Nodo actual
        self.current_edge = None 	# Arista actual
        self.adj_list = {}       # Para la lista de adyacencia
       

    # Método llamado cuando se inicia un nuevo elemento XML
    def startElement(self, name, attrs):
        # Si el elemento es un nodo, inicializamos la estructura del nodo actual
        if name == "node":
            node_id = attrs["id"] # captura el id
            self.current_node = {
                "id": node_id,
                "osm_id": None,  
                "lon": None,     
                "lat": None      
            }
        
        elif name == "edge":	# Si es una arista, inicializamos la estructura de la arista actual
            source = attrs["source"] # Nodo de origen
            target = attrs["target"] # Nodo de destino
            self.current_edge = {
                "source": source,
                "target": target,
                "length": None    
            }
        
        elif name == "data" and self.current_node is not None:	# Si es y pertenece 'data'  a un nodo actual, se procesa el contenido
            key = attrs["key"]
            if key == "d4":      # Clave para id del nodo
                self.current_node["osm_id"] = ""
            elif key == "d8":    # Clave para la longitud
                self.current_node["lon"] = ""
            elif key == "d9":                   self.current_node["lat"] = ""
        # Si el elemento es 'data' y pertenece a una arista actual, se procesa el contenido
        elif name == "data" and self.current_edge is not None:
            key = attrs["key"]
            if key == "d17":     
                self.current_edge["length"] = ""

   
    def characters(self, content):  	# Método para capturar el contenido entre las etiquetas
        if self.current_node is not None:
            # Asigna el contenido al campo correspondiente para el nodo y la arista actual
            if self.current_node["osm_id"] is not None:
                self.current_node["osm_id"] += content
            elif self.current_node["lon"] is not None:
                self.current_node["lon"] += content
            elif self.current_node["lat"] is not None:
                self.current_node["lat"] += content
        elif self.current_edge is not None:
            if self.current_edge["length"] is not None:
                self.current_edge["length"] += content

    
    def endElement(self, name):	# Método cuando se termina de procesar un elemento
        if name == "node":
            # Cuando se cierra un nodo, se agrega al diccionario de nodos
            node_id = self.current_node["id"]
            self.nodes[node_id] = self.current_node
            self.adj_list[node_id] = []  	# Inicializa una lista vacía para las aristas del nodo en la lista de adyacencia
            self.current_node = None    	 # Reinicia el nodo actual
        elif name == "edge":
            # Cuando se cierra una arista, se agrega a la lista de aristas y a la lista de adyacencia
            source = self.current_edge["source"]
            target = self.current_edge["target"]
            length = self.current_edge["length"]
            self.edges.append((source, target, length))   	# Agrega la arista a la lista de aristas
            self.adj_list[source].append((target, length)) 	# Agrega el destino y longitud en la lista de adyacencia
            self.current_edge = None                       # Reinicia la arista actual
        elif name == "data":
            # Ajusta campos en caso de valores vacíos (para evitar errores)
            if self.current_node is not None:
                if self.current_node["osm_id"] == "":
                    self.current_node["osm_id"] = None
                elif self.current_node["lon"] == "":
                    self.current_node["lon"] = None
                elif self.current_node["lat"] == "":
                    self.current_node["lat"] = None
            elif self.current_edge is not None and self.current_edge["length"] == "":
                self.current_edge["length"] = None

# Función para parsear un archivo GraphML y devolver la lista de adyacencia y los nodos
def parse_graphml(file_path):
    parser = xml.sax.make_parser()        # Crea un nuevo parser SAX
    handler = GraphMLHandler()            # Crea una instancia del manejador de eventos
    parser.setContentHandler(handler)     # Asigna el manejador al parser
    parser.parse(file_path)               # Inicia el parsing del archivo
    return handler.adj_list, handler.nodes	 # Retorna la lista de adyacencia y los nodos

# Uso del parser
file_path = r"C:\Users\oussa\Desktop\TERCERO\TERCERO\PRIMER CUATRI\SSI\CR_Capital.xml"
adj_list, nodes = parse_graphml(file_path)

# Mostrar la lista de adyacencia y la información de nodos
print("Lista de Adyacencia:")
for source, targets in adj_list.items():
    print(f"{source}: {targets}")

print("\nInformación de Nodos:")
for node_id, data in nodes.items():
    print(f"{node_id}: {data}")