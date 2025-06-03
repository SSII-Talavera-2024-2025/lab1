from xml.sax import handler, make_parser
from collections import defaultdict
from node import Node
from edge import Edge
from utils import safe_float

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
            if self.current_node_id is not None:
                if self.current_key == 'd4':
                    self.node_attrs['id_osm'] = self.buffer
                elif self.current_key == 'd8':
                    self.node_attrs['lon'] = safe_float(self.buffer)
                elif self.current_key == 'd9':
                    self.node_attrs['lat'] = safe_float(self.buffer)
            elif self.current_edge:
                if self.current_key == 'd17':
                    self.edge_attrs['length'] = safe_float(self.buffer)

        elif name == 'node':
            node = Node(
                id=self.current_node_id,
                id_osm=self.node_attrs.get('id_osm'),
                lon=self.node_attrs.get('lon'),
                lat=self.node_attrs.get('lat')
            )
            self.nodes[self.current_node_id] = node
            self.current_node_id = None

        elif name == 'edge':
            source = self.current_edge['source']
            target = self.current_edge['target']
            length = self.edge_attrs.get('length', 0.0)
            edge = Edge(source, target, length)
            self.graph[source].append((target, length))
            self.current_edge = {}

def load_graph_from_graphml(file_path):
    parser = make_parser()
    handler = GraphHandler()
    parser.setContentHandler(handler)
    with open(file_path, 'r', encoding='utf-8') as f:
        parser.parse(f)
    return handler.nodes, handler.graph
