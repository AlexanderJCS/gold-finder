import math
import networkx as nx


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def gen_network(points):
    g = nx.Graph()
    g.add_nodes_from(points)
    
    # connect every vertex to every other vertex
    for i, point1 in enumerate(points):
        for j, point2 in enumerate(points[i + 1:], start=i + 1):
            g.add_edge(points[i], points[j], weight=dist(point1, point2))
    
    # return the MST of the network for later analysis
    return nx.minimum_spanning_tree(g)
    

def density(points: list[tuple[int, int]]) -> float:
    """
    Finds the density of a set of points using the minimum spanning tree of the network of the points, using distance as
    weight.
    
    :param points: The points of the gold particles (list of tuples)
    :return: A density score, where a higher score means a higher density. 0 = no density, infinity = infinite density
    """
    
    if len(points) in (0, 1):  # return infinity since there is an infinite density with infinitely small area
        return float("inf")
    
    network = gen_network(points)
    total_weight = sum(network.edges[edge]["weight"] for edge in network.edges)
    return len(points) / total_weight
