from xml.sax import handler, make_parser
from collections import defaultdict

class GraphHandler(handler.ContentHandler):
    def __init__(self):
        super().__init__()
        self.graph = defaultdict(list)
        self.nodes = {}
        self.current_node_id = None
        self.current_edge = {}
        self.capture_data = False
        self.buffer = ""
        self.node_attrs = {}
        self.edge_attrs = {}

    def startElement(self, name, attrs):
        if name == 'node':
            self.current_node_id = attrs['id']
            self.node_attrs = {}
        elif name == 'edge':
            self.current_edge = {
                'source': attrs['source'],
                'target': attrs['target']
            }
            self.edge_attrs = {}
        elif name == 'data':
            self.capture_data = True
            self.buffer = ""
            self.current_key = attrs.get('key', '')
    
    def characters(self, content):
        if self.capture_data:
            self.buffer += content.strip()
    
    def endElement(self, name):
        if name == 'data':
            self.capture_data = False
            # Nodo
            if self.current_node_id is not None:
                if self.current_key == 'd4':
                    self.node_attrs['id_osm'] = self.buffer
                elif self.current_key == 'd8':
                    self.node_attrs['lon'] = float(self.buffer)
                elif self.current_key == 'd9':
                    self.node_attrs['lat'] = float(self.buffer)
            # Arista
            elif self.current_edge:
                if self.current_key == 'd17':  # longitud
                    self.edge_attrs['length'] = float(self.buffer)
        elif name == 'node':
            self.nodes[self.current_node_id] = self.node_attrs
            self.current_node_id = None
        elif name == 'edge':
            source = self.current_edge['source']
            target = self.current_edge['target']
            length = self.edge_attrs.get('length', 0.0)
            self.graph[source].append((target, length))
            self.current_edge = {}

def load_graph_from_graphml(file_path):
    parser = make_parser()
    handler = GraphHandler()
    parser.setContentHandler(handler)
    with open(file_path, 'r', encoding='utf-8') as f:
        parser.parse(f)
    return handler.nodes, handler.graph
nodes, adjacency_list = load_graph_from_graphml("CR_Capital.xml")