import matplotlib.pyplot as plt
import timeit
from functools import partial
import random
from collections import defaultdict
# from memory_profiler import profile
import sys

sys.setrecursionlimit(11000)  # Python default recursion limit is 1000.

"""
This python script is used to measure time and memory usage by algorithms
implemented in the project.
Most of the functions (make_dicionary_graph(), sort_edges() and all algorithms)
are reimplemented in this file due to the fact that they were also 
responsible for adding data to visualization_data, which would
significantly alter time and memory usage.
Time results for different input are shown as a matplotlib graph for
every algorithm
Memory usage is measured using python module, called memory_profiler.
https://pypi.org/project/memory-profiler/
Decorator @profile is commented out because it affects drawing graphs.
It can be easily reverted, but only time or memory can be measured at once.
"""


def generate_edges(n):
    """
    Generated graph with n vertices, where every edge is a bridge.
    """
    edges = []
    vertices = n
    for i in range(vertices - 1):
        edges.append([i, i + 1])
    return edges


def make_dictionary_graph(edges):
    dictionary_graph = defaultdict(list)
    for edge in edges:
        dictionary_graph[edge[0]].append(edge[1])
        dictionary_graph[edge[1]].append(edge[0])
    return dictionary_graph


def sort_edges(edges):
    sorted_edges = set()
    for edge in edges:
        edge.sort()
        sorted_edges.add((edge[0], edge[1]))
    return sorted_edges


# @profile
def dfs_brute_force(n):
    edges = generate_edges(n)

    def dfs(visited, graph, vertex):
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in graph[vertex]:
                dfs(visited, graph, neighbor)
    bridges = []
    for i in range(len(edges)):
        removed_edge = edges[i]
        combination = (edges[:i] + edges[i+1:])
        graph = make_dictionary_graph(combination)
        visited = set()
        dfs(visited, graph, list(graph.keys())[0])
        if len(visited) != n:
            bridges.append(tuple(removed_edge))


# @profile
def tarjans_algorithm(n):
    edges = generate_edges(n)
    graph = make_dictionary_graph(edges)
    disc, low, time, bridges = [0] * n, [0] * n, [1], []

    def dfs(curr, prev):
        disc[curr] = low[curr] = time[0]
        time[0] += 1
        for next in graph[curr]:
            if not disc[next]:
                dfs(next, curr)
                low[curr] = min(low[curr], low[next])
            elif next != prev:
                low[curr] = min(low[curr], disc[next])
            if low[next] > disc[curr]:
                bridges.append((curr, next))
    dfs(0, -1)


# @profile
def kaiwensun_bridges(n):
    edges = generate_edges(n)
    edges = sort_edges(edges)
    rank = [-2] * n
    graph = make_dictionary_graph(edges)

    def dfs(vertex, depth):
        if rank[vertex] >= 0:
            return rank[vertex]
        rank[vertex] = depth
        min_back_depth = n
        for neighbor in graph[vertex]:
            if rank[neighbor] == depth - 1:
                continue
            back_depth = dfs(neighbor, depth + 1)
            if back_depth <= depth:
                edges.discard(tuple(sorted((vertex, neighbor))))
            min_back_depth = min(min_back_depth, back_depth)
        return min_back_depth
    dfs(0, 0)


def plot_function(function, n_min, n_max, interval, tests, color):
    """
    This function was based on the code by Mahesh Venkitachalam.
    https://electronut.in/plotting-algorithmic-time-complexity-of-a-function-using-python/
    Plots function of input vs time taken to complete algorithm.
    function - function used
    n_min - lowest input value
    n_max - highest input value
    interval - subsequent increments for every execution
    tests - number of test for every function
    color - specifies color for each algorithm
    """
    x = []  # x-axis data, input size
    y = []  # y-axis data, time (s) taken to complete algorithm
    for i in range(n_min, n_max, interval):
        n = i
        timer_test = timeit.Timer(partial(function, n))
        t = timer_test.timeit(number=tests)
        x.append(i)
        y.append(t)
    plt.plot(x, y, color, label=function.__name__)
    plt.legend(loc="upper left")
    plt.xlabel("number of verices")
    plt.ylabel("time (s)")


# call main
if __name__ == '__main__':
    plot_function(dfs_brute_force, 1, 1000, 10, 10, "og")
    plot_function(tarjans_algorithm, 1, 1000, 10, 10, "or")
    plot_function(kaiwensun_bridges, 1, 1000, 10, 10, "ob")
    plt.show()  # Show final plot
    # used for memory profilling functions
    # dfs_brute_force(500)
    # tarjans_algorithm(500)
    # kaiwensun_bridges(500)
