#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict

DEBUG = False


class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v
        self.capacity = w

    def __repr__(self):
        return "%s->%s: %s" % (self.source, self.sink, self.capacity)


class FlowNetwork(object):
    def __init__(self):
        self.adj = defaultdict(lambda: set())
        self.edges = {}
        self.flow = {}

    def get_adjacent_edges(self, u):
        return self.adj[u]

    def get_edge(self, u, v):
        return self.edges[(u, v)]

    def add_edge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u, v, w)
        redge = Edge(v, u, 0)  # zero if reverse
        edge.redge = redge
        redge.redge = edge
        self.adj[u].add(edge)
        self.adj[v].add(redge)
        self.edges[(u, v)] = edge
        self.flow[edge] = 0.0
        self.flow[redge] = 0.0

    def find_path(self, current, target, path):
        if DEBUG:
            print 'find augument path: current point: %s ... -> %s, path: %s' % (
                current, target, path)
        if current == target:
            return path
        for edge in self.get_adjacent_edges(current):  # deep traverse
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and edge not in path and (
                    not path or edge.sink != path[0].source):  # avoid circle
                result = self.find_path(edge.sink, target, path + [edge])
                if result != None:
                    return result

    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            if DEBUG:
                print "residuals: %s, path: %s, min: %s" % (residuals, path,
                                                            flow)
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])

        self.topology_flow()
        return sum(self.flow[edge] for edge in self.get_adjacent_edges(source))

    def topology_flow(self):
        print 'topology flow, format: source -> sink: (flow/capability):'
        for edge in self.flow:
            if edge.capacity > 0.0:
                print "%s->%s: (%s/%s)" % (edge.source, edge.sink,
                                           self.flow[edge], edge.capacity)


def test():
    g = FlowNetwork()
    g.add_edge('s', 'o', 3)
    g.add_edge('s', 'p', 3)
    g.add_edge('o', 'p', 2)
    g.add_edge('o', 'q', 3)
    g.add_edge('p', 'r', 2)
    g.add_edge('r', 't', 3)
    g.add_edge('q', 'r', 4)
    g.add_edge('q', 't', 2)
    res = g.max_flow('s', 't')
    print 'max_flow:', res


def sim_cdn():
    g = FlowNetwork()
    g.add_edge('s', 'g1r1', 0.8)
    g.add_edge('s', 'g1r2', 0.2)
    g.add_edge('s', 'g2r1', 0.1)
    g.add_edge('s', 'g2r2', 0.4)
    g.add_edge('n1', 't', 1.5)
    g.add_edge('n2', 't', 0.8)
    # set capability by availability
    for a, b in (("g1r1", "n1"), ("g1r1", "n2"), ("g1r2", "n1"), ("g2r1", "n1"),
                 ("g2r2", "n2")):
        cap = min(g.get_edge("s", a).capacity, g.get_edge(b, "t").capacity)
        if DEBUG:
            print "link gr: %s, n: %s, cap: %s" % (a, b, cap)
        g.add_edge(a, b, cap)
    res = g.max_flow('s', 't')
    print 'max_flow:', res


if __name__ == "__main__":
    #test()
    sim_cdn()
