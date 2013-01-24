import sys
from collections import deque


class Vertex(object):
    def __init__(self, title):
        self.title = title
        self.adjacencies = {}
        self.flow = {}
        self.prev = None

    def __repr__(self):
        return self.title


class WeightedBipartiteGraph(object):
    def __init__(self):
        self.left = set([])
        self.right = set([])

    def add_edge(self, u, v, w=1):
        if (u in self.left and v in self.right) or (u in self.right and v in self.left):
            u.adjacencies[v] = w
            v.adjacencies[u] = w

    def breadth_first_search(self, root, visit_fn, transition_fn):
        root.prev = None
        queue = deque()
        queue.append(root)
        visited = set([])
        while len(queue) > 0:
            vertex = queue.popleft()
            visited.add(vertex)
            if visit_fn(vertex):
                return True

            for adj in transition_fn(vertex):
                if adj not in visited:
                    adj.prev = vertex
                    queue.append(adj)

        return False

    def matching(self):
        s = Vertex('source')
        self.right.add(s)


        t = Vertex('terminal')
        self.left.add(t)

        for l in self.left:
            self.add_edge(s, l)

        for r in self.right:
            self.add_edge(r, t)

        self._max_flow(s, t)

        self.left.remove(t)
        self.right.remove(s)

        matching = set([])
        for l in self.left:
            for r in l.adjacencies:
                if l.flow[r] > 0:
                    matching.add(frozenset([l, r]))

        return matching

    def _max_flow(self, s, t):
        for vertex in self.left | self.right:
            vertex.flow = {}
            for adj in vertex.adjacencies:
                vertex.flow[adj] = 0

        def visit(vertex):
            if vertex == t:
                return True

        def transition(vertex):
            return [adj for adj in vertex.adjacencies if vertex.adjacencies[adj] - vertex.flow[adj] > 0]

        while self.breadth_first_search(s, visit, transition):
            vertex = t
            min_residual = sys.maxint
            while vertex.prev is not None:
                residual = vertex.prev.adjacencies[vertex] - vertex.prev.flow[vertex]
                if residual < min_residual:
                    min_residual = residual
                vertex = vertex.prev

            vertex = t
            while vertex.prev is not None:
                vertex.prev.flow[vertex] += min_residual
                vertex.flow[vertex.prev] -= min_residual
                vertex = vertex.prev


if __name__ == '__main__':
    test_cases = int(sys.stdin.readline())
    for i in range(test_cases):
        c, d, v = [int(val) for val in sys.stdin.readline().split(' ')]
        likes = {}
        hates = {}
        for i in range(1, c + 1):
            likes['C%d' % i] = set([])
            hates['C%d' % i] = set([])
        for i in range(1, d + 1):
            likes['D%d' % i] = set([])
            hates['D%d' % i] = set([])

        graph = WeightedBipartiteGraph()
        for j in range(v):
            vote = sys.stdin.readline().strip()
            like, hate = [val.strip() for val in vote.split(' ')]

            vertex = Vertex(vote)

            likes[like].add(vertex)
            hates[hate].add(vertex)

            if vote.startswith('C'):
                graph.left.add(vertex)
            if vote.startswith('D'):
                graph.right.add(vertex)

            for conflict in likes[hate]:
                graph.add_edge(vertex, conflict)
            for conflict in hates[like]:
                graph.add_edge(vertex, conflict)
        print v - len(graph.matching())
