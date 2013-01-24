import catvsdog
import unittest
import random
import itertools
import time


class TestCatVsDog(unittest.TestCase):
    def test_cat_vs_dog(self):
        graph = catvsdog.FlowNetwork()
        graph.add_vertex('source')
        graph.add_vertex('sink')

        left = set([])
        right = set([])
        for i in range(500):
            graph.add_vertex(str(i))
            coin = random.choice([True, False])
            if coin:
                left.add(str(i))
            else:
                right.add(str(i))

        for l in left:
            for r in right:
                coin = random.choice([True, False])
                if coin:
                    graph.add_edge(l, r, 1)

        for l in left:
            graph.add_edge('source', l, 1)
        for r in right:
            graph.add_edge(r, 'sink', 1)

        print "STARTING"
        _t0 = time.time()
        print graph.max_flow('source', 'sink')
        print time.time() - _t0


if __name__ == '__main__':
    unittest.main()
