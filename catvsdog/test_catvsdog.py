import catvsdog
import unittest
import random
import itertools


class TestCatVsDog(unittest.TestCase):
    def _random_graph(self, left, right, edges):
        graph = catvsdog.HopcroftKarp()
        for i in range(left):
            graph.left.add(catvsdog.Vertex('Left %d' % i))
        for i in range(right):
            graph.right.add(catvsdog.Vertex('Right %d' % i))
        for i in range(edges):
            graph.add_edge(random.sample(graph.left, 1)[0], random.sample(graph.right, 1)[0])
        return graph

    def _check_independence(self, graph, ind_set):
        ind_list = list(ind_set)
        for i in range(len(ind_list) - 1):
            for j in range(i + 1, len(ind_list)):
                if ind_list[i] in ind_list[j].adjacencies or ind_list[j] in ind_list[i].adjacencies:
                    return False
        return True

    def _check_maximality(self, graph, ind_set):
        #Verifies that the independent set is maximal. Does not verify that it is maximum.
        #TODO: Think of an efficient way to check that the ind_set is of maximum cardinality
        for vertex in graph.left | graph.right:
            if vertex not in ind_set:
                if self._check_independence(graph, ind_set | set([vertex])):
                    return False
        return True

    def random_tests(self, num_tests):
        for i in range(num_tests):
            left = random.randint(1, 100)
            right = random.randint(1, 100)
            edges = random.randint(0, 500)
            graph = self._random_graph(left, right, edges)
            ind_set = graph.independent_set()

            self.assertTrue(self._check_independence(graph, ind_set))
            self.assertTrue(self._check_maximality(graph, ind_set))

    def test_independent_set(self):
        u = catvsdog.Vertex('u')
        v = catvsdog.Vertex('v')
        graph = catvsdog.HopcroftKarp()
        graph.left.add(u)
        graph.right.add(v)

        ind_set = graph.independent_set()
        self.assertEqual(ind_set, set([u, v]))

        graph.add_edge(u, v)
        ind_set = graph.independent_set()
        self.assertEqual(len(ind_set), 1)

        self.random_tests(1000)


if __name__ == '__main__':
    unittest.main()
