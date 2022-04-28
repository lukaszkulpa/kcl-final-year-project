from graph import Graph
import unittest
import time
import sys

sys.setrecursionlimit(6000)  # Python's default recursion limit is 1000.


class Testing(unittest.TestCase):
    """
    Testing class uses unit testing to check if bridges found by all
    three algorithm: brute-force depth first search, Tarjan's algorithm
    and algorithm presented by Kaiwen Sun return correct answers.
    """

    # Test graph with one vertex and no edges.
    def test_one_vertex_graph(self):
        graph = Graph(1, [])
        brute_force_bridges = graph.dfs_brute_force()
        tarjans_bridges = graph.tarjans_algorithm()
        kaiwensun_bridges = graph.kaiwensun_bridges()
        self.assertEqual(brute_force_bridges, [])
        self.assertEqual(tarjans_bridges, [])
        self.assertEqual(kaiwensun_bridges, [])

    # Test custom graph with 4 vertices
    def test_custom_four_vertex_graph(self):
        graph = Graph(4, [[0, 1], [1, 2], [2, 0], [2, 3]])
        brute_force_bridges = graph.dfs_brute_force()
        tarjans_bridges = graph.tarjans_algorithm()
        kaiwensun_bridges = graph.kaiwensun_bridges()
        self.assertEqual(brute_force_bridges, [(2, 3)])
        self.assertEqual(tarjans_bridges, [(2, 3)])
        self.assertEqual(kaiwensun_bridges, [(2, 3)])

    # Graph is build of edges where every edge is a bridge.
    def test_all_bridges_graph(self):
        edges = []
        bridges = []
        vertices = 3000
        for i in range(vertices-1):
            edges.append([i, i + 1])
            bridges.append((i, i + 1))
        graph = Graph(vertices, edges)
        brute_force_bridges = graph.dfs_brute_force()
        tarjans_bridges = graph.tarjans_algorithm()
        kaiwensun_bridges = graph.kaiwensun_bridges()
        # check if a and b have the same elements, regardless of their order
        self.assertCountEqual(brute_force_bridges, bridges)
        self.assertCountEqual(tarjans_bridges, bridges)
        self.assertCountEqual(kaiwensun_bridges, bridges)

    # There are no bridges in a graph
    def test_no_bridge_graph(self):
        edges = []
        bridges = []
        vertices = 3000
        for i in range(vertices - 1):
            edges.append([i, i + 1])
        edges.append([vertices - 1, 0])
        graph = Graph(vertices, edges)
        brute_force_bridges = graph.dfs_brute_force()
        tarjans_bridges = graph.tarjans_algorithm()
        kaiwensun_bridges = graph.kaiwensun_bridges()
        self.assertEqual(brute_force_bridges, bridges)
        self.assertEqual(tarjans_bridges, bridges)
        self.assertEqual(kaiwensun_bridges, bridges)


if __name__ == '__main__':
    unittest.main()
