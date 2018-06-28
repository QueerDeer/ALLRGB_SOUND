import itertools
import random
import collections

# Represent a vertex as an arbitrary immutable object, and a graph as an
# adjacency list, specifically as a dictionary mapping vertices to lists
# of adjacent vertices.


def grid_graph(*size):
    """Return grid graph with the given dimensions.
    """
    def neighbors(vertex):
        neighborhood = []
        for i in range(len(size)):
            for dx in (-1, 1):
                w = list(vertex)
                w[i] = w[i] + dx
                if 0 <= w[i] < size[i]:
                    neighborhood.append(tuple(w))
        return neighborhood
    return {v: neighbors(v) for v in itertools.product(*map(range, size))}


def random_spanning_tree(graph):
    """Return uniform random spanning tree of undirected graph.
    """
    root = random.choice(list(graph))
    parent = {root: None}
    tree = set([root])
    for vertex in graph:

        # Take random walk from a vertex to the tree.
        v = vertex
        while v not in tree:
            neighbor = random.choice(graph[v])
            parent[v] = neighbor
            v = neighbor

        # Erase any loops in the random walk.
        v = vertex
        while v not in tree:
            tree.add(v)
            v = parent[v]
    return parent


def tree_to_graph(tree):
    """Convert predecessor vector tree to directed graph and its root.
    """
    graph = {v: [] for v in tree}
    root = None
    for vertex in tree:
        parent = tree[vertex]
        if parent is not None:
            graph[parent].append(vertex)
        else:
            root = vertex
    return graph, root


def bfs(graph, root):
    """Iterate breadth-first over vertices in graph starting with root.
    """
    queue = collections.deque([root])
    visited = set()
    while len(queue) > 0:
        vertex = queue.popleft()
        if vertex not in visited:
            yield vertex
            visited.add(vertex)
            for neighbor in graph[vertex]:
                queue.append(neighbor)
