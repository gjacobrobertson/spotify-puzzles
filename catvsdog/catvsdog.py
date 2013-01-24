import sys
from collections import deque

class HopcroftKarp(object):
    def __init__(self):
        self.adj = {'nil': set()}
        self.pair_left = {}
        self.pair_right = {}
        self.left = set([])
        self.right = set([])
        self.dist = {}

    def add_left(self, v):
        self.left.add(v)
        self.adj[v] = set()

    def add_right(self, v):
        self.right.add(v)
        self.adj[v] = set()

    def add_edge(self, u, v):
        if (u in self.left and v in self.right) or (u in self.right and v in self.left):
            self.adj[u].add(v)
            self.adj[v].add(u)

    def BFS(self):
        queue = deque()
        for v in self.left:
            if self.pair_left[v] == 'nil':
                self.dist[v] = 0
                queue.append(v)
            else:
                self.dist[v] = float('inf')

        self.dist['nil'] = float('inf')
        while len(queue) > 0:
            v = queue.popleft()
            for u in self.adj[v]:
                if self.dist[self.pair_right[u]] == float('inf'):
                    self.dist[self.pair_right[u]] = self.dist[v] + 1
                    queue.append(self.pair_right[u])

        return self.dist['nil'] != float('inf')

    def DFS(self, v):
        if v != 'nil':
            for u in self.adj[v]:
                if self.dist[self.pair_right[u]] == self.dist[v] + 1:
                    if self.DFS(self.pair_right[u]):
                        self.pair_right[u] = v
                        self.pair_left[v] = u
                        return True
            self.dist[v] = float('inf')
            return False
        return True

    def max_matching(self):
        for v in self.left | self.right | set(['nil']):
            self.pair_left[v] = 'nil'
            self.pair_right[v] = 'nil'
        matching = 0
        while self.BFS():
            for v in self.left:
                if self.pair_left[v] == 'nil':
                    if self.DFS(v):
                        matching += 1
        return matching


if __name__ == '__main__':
    test_cases = int(sys.stdin.readline())
    for i in range(test_cases):
        c, d, v = [int(val) for val in sys.stdin.readline().split(' ')]
        likes = {}
        hates = {}
        votes = set()
        for i in range(1, c + 1):
            likes['C%d' % i] = set([])
            hates['C%d' % i] = set([])
        for i in range(1, d + 1):
            likes['D%d' % i] = set([])
            hates['D%d' % i] = set([])

        graph = HopcroftKarp()
        for j in range(v):
            vote = sys.stdin.readline().strip()
            if vote not in votes:
                votes.add(vote)
                like, hate = [val for val in vote.split(' ')]

                likes[like].add(vote)
                hates[hate].add(vote)

                if vote.startswith('C'):
                    graph.add_left(vote)
                if vote.startswith('D'):
                    graph.add_right(vote)

                for conflict in likes[hate]:
                    graph.add_edge(vote, conflict)
                for conflict in hates[like]:
                    graph.add_edge(vote, conflict)
        print v - graph.max_matching()
