import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class Graph:
    """
    Graph class holds logic for creating custom undirected graphs 
    from number of vertices and edges specified by the user.
    It includes all algorithms used in the project:
    depth-first search brute force approach, algorithm
    developed by Robert Tarjan and one more algorithm that 
    was presented by Kaiwen Sun in Leetcode's 1992. problem,
    "Critical connections in a Network". It saves step-by-step
    execution of these algorithms, which are later used in 
    visualizing the execution of finding bridges.
    """

    def __init__(self, n, edges):
        """
        Generates a new graph with n as number of vertices and
        edges as a list of lists of edges, eg. edge between vertex
        labelled 0 and vertex labelled 1 is represented by [0, 1].
        It stores the detailed execution of algorithms implemented
        in the project.
        """
        self.n = n  # number of vertices
        self.edges = edges  # list of lists of edges
        self.visualization_data = []  # characteristics of each algorithm

    def make_dictionary_graph(self, edges):
        """
        Created a defaultdict dictionary representation of
        available neighbors from each vertex.
        {0: [1, 2], 1: [0], 2: [0]}) means that 0 is connected to 1 and 2,
        and 1 and 2 is also connected to 0.
        """
        dictionary_graph = defaultdict(list)
        for edge in edges:
            # edges are appended twice, because it is an undirected graph
            dictionary_graph[edge[0]].append(edge[1])
            dictionary_graph[edge[1]].append(edge[0])
        return dictionary_graph

    def dfs_brute_force(self):
        """
        A brute-force solution using depth-first search.
        For every edge (u, v) this edge is temporarily removed
        from the graph, and then using depth-first search it is
        checked if graph remains connected or not. Time complexity
        for this method is (O(E*(V+E)), so quadratic.
        Return bridges in a graph.
        """
        self.clear_visualization_data()

        def dfs(visited, graph, vertex):
            # Standalone depth-first search for traversing graphs.
            if vertex not in visited:
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    dfs(visited, graph, neighbor)
        bridges = []
        if len(self.edges) == 1:
            self.visualization_data.append([self.edges[0], True])
            return ([(tuple(self.edges[0]))])
        for i in range(len(self.edges)):
            removed_edge = self.edges[i]
            # Creates every possible combination of edges of length n - 1
            combination = (self.edges[:i] + self.edges[i+1:])
            graph = self.make_dictionary_graph(combination)
            visited = set()  # set for already visited vertices
            dfs(visited, graph, list(graph.keys())[0])
            if len(visited) != self.n:
                # Add removed to bridges if not all vertices were visited
                bridges.append(tuple(removed_edge))
                self.visualization_data.append([removed_edge, True])
            else:
                self.visualization_data.append([removed_edge, False])

        return bridges

    def tarjans_algorithm(self):
        """
        Implementation of Tarjan's bridge-finding algorithm.
        Uses disc (discovery time) and low (lowest vertex reachable)
        and time to use with disc. 
        Returns list of bridges in a graph.
        """
        self.clear_visualization_data()

        graph = self.make_dictionary_graph(self.edges)
        # initialize disc and low with zeros for every vertex
        disc = [0] * self.n
        low = [0] * self.n
        time = [1]
        bridges = []  # time counter

        def dfs(curr, prev):
            disc[curr] = low[curr] = time[0]
            self.visualization_data.append([time[0], disc.copy(),
                                            low.copy(), bridges.copy()])
            time[0] += 1  # timer counter increases
            for next in graph[curr]:
                if not disc[next]:
                    # recursive DFS calls on unvisited adjacent vertices to curr vertex
                    dfs(next, curr)
                    low[curr] = min(low[curr], low[next])  # cycle found
                elif next != prev:
                    low[curr] = min(low[curr], disc[next])
                # if after backtracking low[next] > disc[curr], edge (curr, next) is a bridge
                if low[next] > disc[curr]:
                    bridges.append((curr, next))
        dfs(0, -1)
        self.visualization_data.append([time[0], disc.copy(),
                                        low.copy(), bridges.copy()])
        return bridges

    def kaiwensun_bridges(self):
        """
        Algorithm created by Kaiwen Sun as a solution to 1192. Leetcode
        problem "Critical connections in a network". Algorithm was posted
        in the discussion forum with detailed explanation. I modified it to 
        fit the specifications of my project, but the idea behind it is thanks
        to Kaiwen Sun.
        The most important bit of this algorithms is that an edge is a bridge,
        if and only if is not in a cycle. It searches for any cycles in a graph
        and removes all edges in the cycles. The remaining edges are bridges.
        Returns list of bridges in a graph.
        """

        def sort_edges():
            """
            This code is taken from the same forum post from
            user "jordan34".
            Return sorted set of edges.
            From list of lists of edges: [[0, 1], [2, 0], [1, 3]]
            we get a set of sorted tuples: {(0, 1), (0, 2), (1, 3)}
            Used in deleting edges that are part of a cycle.
            """
            sorted_edges = set()
            for edge in self.edges:
                edge.sort()
                sorted_edges.add((edge[0], edge[1]))
            return sorted_edges

        self.clear_visualization_data()

        edges = sort_edges()
        rank = [-2] * self.n  # depth of a vertex in DFS
        graph = self.make_dictionary_graph(self.edges)

        def dfs(vertex, depth):
            # DFS is used to find if and edge is in a cycle.
            if rank[vertex] >= 0:
                # visiting (0<=rank<n), or visited (rank=n)
                return rank[vertex]
            rank[vertex] = depth  # assign current depth to rank[vertex]
            min_back_depth = self.n
            for neighbor in graph[vertex]:
                # check all adjacent vertices for currect vertex
                if rank[neighbor] == depth - 1:
                    # don't go to parent vertex
                    continue
                self.visualization_data.append([rank.copy(), edges.copy()])
                back_depth = dfs(neighbor, depth + 1)
                if back_depth <= depth:
                    # edge is in a cycle
                    edges.discard(tuple(sorted((vertex, neighbor))))
                    self.visualization_data.append([rank.copy(), edges.copy()])
                min_back_depth = min(min_back_depth, back_depth)

            return min_back_depth  # minimal rank DFS finds

        dfs(0, 0)  # starting vertex has rank 0
        return list(edges)

    def get_visualization_data(self):
        # returns step-by-step visualization of each algorithm
        return self.visualization_data

    def clear_visualization_data(self):
        # clears any data in visualization_data for new algorithm
        self.visualization_data = []
