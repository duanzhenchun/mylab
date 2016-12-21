#!/usr/bin/env python
# encoding: utf-8

DEBUG = False

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
        redge = Edge(v,u,0) # zero if reverse
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0

    def find_path(self, current, target, path):
        if DEBUG: print 'find augument path:  %s ... -> %s, path: %s' %(current, target, path)
        if current == target:
            return path
        for edge in self.get_edges(current): # deep traverse
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and edge not in path and (not path or edge.sink != path[0].source): # avoid circle
                result = self.find_path( edge.sink, target, path + [edge])
                if result != None:
                    return result

    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            if DEBUG: print "residuals: %s, path: %s, min: %s" %(residuals, path, flow)
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])
        self.show_current_flow()
        return sum(self.flow[edge] for edge in self.get_edges(source))

    def show_current_flow(self):
        print 'maximum flow topology:'
        for edge in self.flow:
            if edge.capacity > 0:
                print "edge: %s, flow: %d" %(edge, self.flow[edge])

def test():
    g = FlowNetwork()
    [g.add_vertex(v) for v in "sopqrt"]
    g.add_edge('s','o',3)
    g.add_edge('s','p',3)
    g.add_edge('o','p',2)
    g.add_edge('o','q',3)
    g.add_edge('p','r',2)
    g.add_edge('r','t',3)
    g.add_edge('q','r',4)
    g.add_edge('q','t',2)
    res = g.max_flow('s','t')
    print 'max_flow:', res

if __name__ == "__main__":
    test()
