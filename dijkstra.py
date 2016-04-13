# dijkstra's algorithm
"""
1. Assign to every node a distance value. Set it to zero for our initial node 
   and to infinity for all other nodes.
 
2. Mark all nodes as unvisited. Set initial node as current.
 
3. For current node, consider all its unvisited neighbors and calculate their 
   tentative distance (from the initial node). For example, if current node 
   (A) has distance of 6, and an edge connecting it with another node (B) 
   is 2, the distance to B through A will be 6+2=8. If this distance is less 
   than the previously recorded distance (infinity in the beginning, zero 
   for the initial node), overwrite the distance.
 
4. When we are done considering all neighbors of the current node, mark it as 
   visited. A visited node will not be checked ever again; its distance 
   recorded now is final and minimal.
 
5. If all nodes have been visited, finish. Otherwise, set the unvisited node 
   with the smallest distance (from the initial node) as the next "current 
   node" and continue from step 3.
 
 - source: wikipedia http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
 - Ref: http://forrst.com/posts/Dijkstras_algorithm_in_Python-B4U
"""

SIZE = 9

## WARNING: xmlrpc doesn't accept set, non string in dico's key
def _int(n):
    return int(n[0])*SIZE + int(n[1])

class Graph(object):
    """
    A simple undirected, weighted graph
    """
    def __init__(self, s):
        SIZE = s
        self.nodes = []
        self.edges = tuple([[] for i in range(s ** 2)]) # tuple of lists or coord
        # self.distances = {} # not needed: distances = 1

    def clone(self):
        clone_graph = Graph(SIZE)
        clone_graph.nodes = self.nodes.copy()
        clone_graph.edges = tuple([l.copy() for l in (self.edges)])
        return clone_graph

    def add_node(self, value):
        self.nodes.append(value)

#    def rm_node(self, value):
#        self.nodes.remove(value)

    def __str__(self):
        graph_str = ""
        for i in range(SIZE):
            for j in range(SIZE):
                index = (i*SIZE) + j
                graph_str += "o"
                if (i, j+1) in self.edges[index]:
                    graph_str += "--"
                else:
                    graph_str += "  "
            graph_str += "\n"
            for j in range(SIZE):
                index = (i*SIZE) + j
                if (i + 1, j) in self.edges[index]:
                    graph_str += "|"
                else:
                    graph_str += " "
                DR = (i + 1, j + 1) in self.edges[index]
                UR = index + SIZE < SIZE ** 2 and (i, j + 1) in self.edges[index + SIZE]
                UL = index + 1 + SIZE < SIZE ** 2 and (i, j) in self.edges[index + 1 + SIZE]
                DL = index + 1 < SIZE ** 2 and (i + 1, j) in self.edges[index + 1]
                if DR:
                    if UR:
                        graph_str += "X"
                    else:
                        graph_str += "\\"
                elif UR:
                    graph_str += "/"
                else:
                    graph_str += " "
                if UL:
                    if DL:
                        graph_str += "X"
                    else:
                        graph_str += "\\"
                elif DL:
                    graph_str += "/"
                else:
                    graph_str += " "
            graph_str += "\n"
        return graph_str

    def add_edge(self, from_node, to_node):
        self._add_edge(from_node, to_node)

    def add_both_edges(self, from_node, to_node):
        self._add_edge(from_node, to_node)
        self._add_edge(to_node, from_node)
        return [(from_node, to_node), (to_node, from_node)]

    def _add_edge(self, from_node, to_node):
        self.edges[_int(from_node)].append(to_node)

    def has_edge(self, from_node, to_node):
        return to_node in self.edges[_int(from_node)]

    def rm_both_edges(self, node1, node2, check=False):
        """
        Remove edges from node1 to node2 and from node2 to node1
        """
        if check and not node2 in self.edges[_int(node1)]:
            return False
        self.rm_edge(node1, node2)
        self.rm_edge(node2, node1)
        return [(node1, node2), (node2, node1)]

    def rm_edge(self, from_node, to_node):
        self.edges[_int(from_node)].remove(to_node)

def _dijkstra(graph, initial_node):
    visited = {initial_node: 0}
    current_node = initial_node
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        cur_wt = visited[min_node]

        for edge in graph.edges[_int(min_node)]:
            wt = cur_wt + 1 # dist = 1
            if edge not in visited or wt < visited[edge]:
                visited[edge] = wt
                path[edge] = min_node

    return visited, path

def _shortest_path(graph, initial_node, goal_x, goal_y, dijkstra_result):
    distances, paths = dijkstra_result
    goal_node = (goal_x, goal_y)
    route = [goal_node]

    while goal_node != initial_node:
        goal_node = paths[goal_node]
        # if we go a second time on the goal line, it's not the best path: skip
        if goal_node[0] == goal_x:
            return False
        route.append(goal_node)

    route.pop() # the first state is not needed
    route.reverse()
    return route

# exception: coord of the opponent
def shortest_path_to_line(graph, initial_node, goal_x, line_size, exception):
    best_route_len = line_size ** 2
    best_route = []
    routes = 0
    dijkstra_result = _dijkstra(graph, initial_node)
    has_except = False
    for y in range(line_size):
        if exception == (goal_x, y):
            has_except = True
            continue
        try:
            route = _shortest_path(graph, initial_node, goal_x, y, dijkstra_result)
        except KeyError: # try to access to a blocked edge
            continue
        if not route:
            continue
        routes += 1
        route_len = len(route)
        if route_len < best_route_len:
            best_route_len = route_len
            best_route = route
    # there is only one route but the opponent is on the goal of this route: ----|O|----
    if routes == 0 and has_except:
        try:
            route = _shortest_path(graph, initial_node, goal_x, exception[1], dijkstra_result)
        except KeyError: # try to access to a blocked edge
            return 0, []
        if route:
            return 1, route
    return routes, best_route
