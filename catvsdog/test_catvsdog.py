import catvsdog
import unittest
import random
import itertools
import time


class TestCatVsDog(unittest.TestCase):
    def _random_graph(self, n):
        graph = catvsdog.WeightedBipartiteGraph()
        for i in range(n):
            coin = random.choice([True,False])
            if coin:
                graph.left.add(catvsdog.Vertex('Left %d' % i))
            else:
                graph.right.add(catvsdog.Vertex('Right %d' % i))

        i = 0
        for l in graph.left:
            for r in graph.right:
                coin = random.choice([True,False])
                if coin:
                    i += 1
                    graph.add_edge(l, r)
        print i
        return graph

    def random_tests(self, num_tests):
        for i in range(num_tests):
            n = random.randint(0, 500)
            graph = self._random_graph(n)
            print "GRAPH"
            _t0 = time.time()
            matching = graph.matching()
            print time.time() - _t0


    def test_independent_set(self):
        u = catvsdog.Vertex('u')
        v = catvsdog.Vertex('v')
        graph = catvsdog.WeightedBipartiteGraph()
        graph.left.add(u)
        graph.right.add(v)

        matching = graph.matching()
        self.assertEqual(matching, set([]))

        graph.add_edge(u, v, 1)
        matching = graph.matching()
        self.assertEqual(matching, set([frozenset([u, v])]))

        self.random_tests(1)


if __name__ == '__main__':
    unittest.main()
