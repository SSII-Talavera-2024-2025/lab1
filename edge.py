class Edge:
    def __init__(self, source, target, length=0.0): # Initialize an Edge object with source, target, and length
        self.source = source
        self.target = target
        self.length = length

    def __repr__(self):
        return f"Edge(source={self.source}, target={self.target}, length={self.length})" # String representation of the Edge object