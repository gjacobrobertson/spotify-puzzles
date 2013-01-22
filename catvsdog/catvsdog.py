import sys
from collections import deque


class Vertex(object):
    def __init__(self, title):
        self.title = title.rstrip()
        self.adjacencies = set([])

    def is_free(self, matching):
        for edge in matching:
            if self in edge:
                return False
        return True

    def __repr__(self):
        return self.title


class HopcroftKarp(object):
    def __init__(self):
        self.left = set([])
        self.right = set([])

    def add_edge(self, u, v):
        if (u in self.left and v in self.right) or (u in self.right and v in self.left):
            u.adjacencies.add(v)
            v.adjacencies.add(u)

    def breadth_first_search(self, root, visit_fn, transition_fn):
        for vertex in self.left | self.right:
            vertex.prev = None
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

    def depth_first_search(self, root, visit_fn, transition_fn):
        for vertex in self.left | self.right:
            vertex.prev = None
        stack = [root]
        visited = set([])
        while len(stack) > 0:
            vertex = stack.pop()
            visited.add(vertex)
            if visit_fn(vertex):
                return True

            for adj in transition_fn(vertex):
                if adj not in visited:
                    adj.prev = vertex
                    stack.append(adj)

        return False

    def _find_layering(self, matching):
        for vertex in self.left | self.right:
            vertex.layer = -1

        def visit(vertex):
            if vertex.prev is not None:
                vertex.layer = vertex.prev.layer + 1
            else:
                vertex.layer = 0

            if vertex in self.right and vertex.is_free(matching):
                self._max_layer = vertex.layer

            return False

        def transition(vertex):
            if vertex in self.left:
                return [adj for adj in vertex.adjacencies if adj.layer == -1 and frozenset([vertex, adj]) not in matching]
            if vertex in self.right:
                return [adj for adj in vertex.adjacencies if adj.layer == -1 and frozenset([vertex, adj]) in matching]

        for vertex in self.left:
            if vertex.is_free(matching):
                self.breadth_first_search(vertex, visit, transition)

    def _find_augmenting_paths(self, matching):
        self._find_layering(matching)
        paths = []

        for vertex in self.left | self.right:
            vertex.used = False

        def visit(vertex):
            if vertex.layer == 0:
                vertex.used = True
                while vertex.prev is not None:
                    vertex.prev.used = True
                    self._path.add(frozenset([vertex, vertex.prev]))
                    vertex = vertex.prev
                return True
            else:
                return False

        def transition(vertex):
            if vertex in self.left:
                return [adj for adj in vertex.adjacencies if not adj.used and frozenset([vertex, adj]) in matching and adj.layer == vertex.layer - 1]
            if vertex in self.right:
                return [adj for adj in vertex.adjacencies if not adj.used and frozenset([vertex, adj]) not in matching and adj.layer == vertex.layer - 1]

        for vertex in self.right:
            if vertex.layer == self._max_layer:
                self._path = set([])
                if self.depth_first_search(vertex, visit, transition):
                    paths.append(self._path)

        return paths

    def max_matching(self):
        matching = set([])
        paths = self._find_augmenting_paths(matching)
        while len(paths) > 0:
            for path in paths:
                matching ^= path
            paths = self._find_augmenting_paths(matching)
        return set([])

    def vertex_cover(self):
        matching = self.max_matching()
        self._cover = self.left.copy()

        def visit(vertex):
            if vertex in self.left:
                self._cover.remove(vertex)
            if vertex in self.right:
                self._cover.add(vertex)
            return False

        def transition(vertex):
            return [adj for adj in vertex.adjacencies if (vertex in self.left and frozenset([vertex, adj]) not in matching) or (vertex in self.right and frozenset([vertex, adj]) in matching)]

        for vertex in self.left:
            if vertex.is_free(matching):
                self.depth_first_search(vertex, visit, transition)

        return self._cover

    def independent_set(self):
        cover = self.vertex_cover()
        ind_set = set([])
        for vertex in self.left | self.right:
            if vertex not in cover:
                ind_set.add(vertex)
        return ind_set


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

        graph = HopcroftKarp()
        for j in range(v):
            vote = sys.stdin.readline()
            like, hate = [val.rstrip() for val in vote.split(' ')]

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
        print len(graph.independent_set())
