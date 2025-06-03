class Node:
    def __init__(self, id, id_osm=None, lon=None, lat=None):
        self.id = id
        self.id_osm = id_osm
        self.lon = lon
        self.lat = lat

    def __repr__(self):
        return f"Node(id={self.id}, id_osm={self.id_osm}, lon={self.lon}, lat={self.lat})"
