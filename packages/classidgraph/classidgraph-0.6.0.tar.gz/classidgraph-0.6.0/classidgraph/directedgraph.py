import numpy as np
import typing
from directedgraph import Vertex

print(1)

class DirectedEdge:
    """
    Represents a Directed Edge connecting two Vertices in a Directed Graph.

    Attributes:
        source_keys : (str, str)     "Class" and "Id" keys of the source.
        goal_keys : (str, str):      "Class" and "Id" keys of the goal.

        edge_vector (numpy.ndarray): Optional vector representation of the directed edge.
    """

    def __init__(self, source_keys: (str, str), goal_keys: (str, str)):
        """
        Initialize a Directed Edge object.

        Args:
            source (str,str):  Class and Id - keys for the Source Node.
            goal   (str,str):  Class and Id - keys for the the Goal Node.
        """

        # set both leys
        self.source_keys : (str, str) = source_keys
        self.goal_keys   : (str, str) = goal_keys
        
        # the use of edge vector is optional
        self.edge_vector = np.array([])

class Vertex:
    """
    Represents a vertex in a directed graph.

    Attributes:
        cl (str): Class of the vertex, part of the unique key.
        id (str): Unique identifier within the class, part of the unique key.
        text (str): Optional textual description of the vertex.
        vector (numpy.ndarray): Optional vector representation of the vertex, typically used for embedding.

    Args:
        cl (str): Class of the Vertex.
        id (str): Unique identifier of the vertex.
        text (str): Textual description of the vertex. Default is an empty string.
        vector (iterable, optional): Initial value for the vector representation. Default is None, which creates an empty numpy array.
    """

    def __init__(self, cl: str, id: str, text: str = "", vector=None):
        self.cl = cl
        self.id = id
        self.text = text
        self.vector = np.array(vector) if vector is not None else np.array([])
        self.incoming_edges = {}
        self.outgoing_edges = {}

    def add_incoming_edge(self, edge : DirectedEdge):
        """
        Add an incoming Edge.

        Args:
            edge  (Edge): The incoming Edge to be added.
        """

        cl, id = edge.source_keys
        if cl not in self.incoming_edges:
            self.incoming_edges[cl] = {}
        self.incoming_edges[cl][id] = edge

    def add_outgoing_edge(self, edge : DirectedEdge):
        """
        Add an outgoing edge.

        Args:
            edge  (DirectedEdge): The Edge to be added.
        """

        cl, id = edge.goal_keys
        if cl not in self.outgoing_edges:
            self.outgoing_edges[cl] = {}
        self.outgoing_edges[cl][id] = edge


class DirectedGraph:
    """
    Represents a Directed Gaph containing Vertices and Directed Edges.

    Attributes:
        vertices (dict): Dictionary storing Vertix objects.
        edges (dict): Dictionary storing Edge object.
    """

    def __init__(self):
        """
        Initialize a DirectedGraph object.
        """
        self.vertices = {}
        self.edges = {}

    def add(self, cl : str, id : str):
        vertex = Vertex(cl = cl, id = id)
        self.add_v(vertex)

    def add_v(self, vertex : Vertex):
        """
        Add a node to the graph.

        Args:
            node (Node): The node object to be added.
        """
        if vertex.cl not in self.vertices:
            self.vertices[vertex.cl] = {}
        self.vertices[vertex.cl][vertex.id] = vertex

    def add_directed_edge(self, source_keys : (str, str), goal_keys : (str, str) ):
        """
        Add a Directed Edge between two Vertics in the graph.

        Args:
            source_keys ( (str,str) ): The keys for Source Vertex.
            goal_keys   ( (str,str)) : The keys for Goal Vertex.
        """

        edge = DirectedEdge(source_keys = source_keys, goal_keys = goal_keys)
        s_cl, s_id = source_keys
        g_cl, g_id = goal_keys

        if s_cl in self.vertices and s_id in self.vertices[s_cl]:
            self.vertices[s_cl][s_id].add_outgoing_edge(edge)

        if g_cl in self.vertices and g_id in self.vertices[g_cl]:
            self.vertices[g_cl][g_id].add_incoming_edge(edge)

        self.edges[ (source_keys, goal_keys) ] = edge

    def connect(self, source : Vertex, goal : Vertex):
        """
        Create a Dircted Edge between the "source" Vertex to the "goal" Vertex.

        Args:
            source (Vertex): The keys for Source Vertex.
            goal   (Vertex) : The keys for Goal Vertex.
        """

        source_keys = (source.cl, source.id)
        goal_keys   = (goal.cl, goal.id)
        self.edges[ (source_keys, goal_keys) ] = DirectedEdge(source_keys, goal_keys)


    def get_v(self, cl : str, id : str):
        vertices = self.vertices[cl]
        vertex = vertices[id]

        return vertex

def main():
    print("")

    o = DirectedGraph();

    for letter in [ "a", "b", "c" ]:
        cl = "field"
        for digit in [ "1", "2", "3" ]:
            id = letter + digit
            o.add(cl = cl, id = id)

    a1 = o.get_v("field", "a1")
    a2 = o.get_v("field", "a2")

    o.connect(a1, a2)
    
    print(len(o.vertices))

if __name__ == "__main__":
    main()