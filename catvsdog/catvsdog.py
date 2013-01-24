import sys
from collections import deque


class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v
        self.capacity = w
    def __repr__(self):
        return "%s->%s:%s" % (self.source, self.sink, self.capacity)

class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}

    def add_vertex(self, vertex):
        self.adj[vertex] = []

    def get_edges(self, v):
        return self.adj[v]

    def add_edge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,w)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0

    def find_path(self, source, sink, path):
        prev = {}
        visited = {}
        queue = deque()
        queue.append(source)
        while len(queue) > 0:
            vertex = queue.popleft()
            visited[vertex] = True
            if vertex == sink:
                path = []
                while vertex in prev:
                    edge, residual = prev[vertex]
                    path.append((edge, residual))
                    vertex = edge.source

                return path

            for edge in self.get_edges(vertex):
                residual = edge.capacity - self.flow[edge]
                if residual > 0 and edge.sink not in visited:
                    queue.append(edge.sink)
                    prev[edge.sink] = (edge, residual)

        return None

    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            flow = min(res for edge,res in path)
            for edge,res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])
        return sum(self.flow[edge] for edge in self.get_edges(source))


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

        graph = FlowNetwork()
        graph.add_vertex('source')
        graph.add_vertex('sink')
        for j in range(v):
            vote = "%d %s" % (j, sys.stdin.readline().strip())
            graph.add_vertex(vote)

            like, hate = [val.strip() for val in vote.split(' ')[1:]]

            if like.startswith('C'):
                graph.add_edge('source', vote, 1)
            elif like.startswith('D'):
                graph.add_edge('sink', vote, 1)


            likes[like].add(vote)
            hates[hate].add(vote)

            for conflict in likes[hate]:
                graph.add_edge(vote, conflict, 1)
            for conflict in hates[like]:
                graph.add_edge(vote, conflict, 1)

        print v - graph.max_flow('source', 'sink')
