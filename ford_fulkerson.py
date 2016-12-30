#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict
import os

DEBUG = False
MIN_BW = 0.01


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
        return self.edges.get((u, v), None)

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

        # deep traverse
        if 's' == current and self.pref_g:
            order = self.gen_g()
        elif current.find("_") > 0 and current in self.pref_cover:
            dic = self.pref_cover[current]
            order = [i[0] for i in sorted(dic.iteritems(), key=lambda (node, v): (v, self.get_edge(current, node) and -1 * ( self.get_edge(current, node).capacity - self.flow[self.get_edge(current, node)] or 1e6)))]
        else:
            order = [i[1] for i in sorted(
                [(edge.capacity - self.flow[edge], edge.sink)
                for edge in self.get_adjacent_edges(current)],
                reverse=True)]

        for sink in order:
            edge = self.get_edge(current, sink)
            if not edge:
                continue
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
                print "residuals: %s, path: %s, min: %s" % (residuals, path, flow)
            if flow < MIN_BW:
                break
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])

        self.topology_flow()
        return sum(self.flow[edge] for edge in self.get_adjacent_edges(source))

    def topology_flow(self):
        print 'topology flow, format: source -> sink: (flow/capability):'
        for edge in self.flow:
            if self.flow[edge] > 0.0:
                print "%s->%s: (%s/%s)" % (edge.source, edge.sink,
                                           self.flow[edge], edge.capacity)

    def init_prefer(self, g_order, dic_cover):
        """
        group: k2 > k6
        cover: g1r1: n1 > n2
            quality: http://10.4.22.135:9877/multiping/quality?str=20161229
        price: n1 < n2
        bottom_bw: n1: 0.4, n2: 0.2
            dynamic calculate
        """
        self.pref_g = []
        dic = defaultdict(lambda: defaultdict(int))
        for edge in self.adj['s']:
            g,r = edge.sink.split('_', 1)
            dic[g][r] = edge.capacity
        for g in g_order:
            lst = sorted(dic[g].iteritems(), reverse=True, key=lambda (k, v): v)
            self.pref_g.append((g, lst))
        if DEBUG:
            print 'self.pref_g:', self.pref_g

        self.pref_cover = dic_cover
        #  self.pref_node = {}

    def gen_g(self):
        if not self.pref_g:
            return
        for (g, lst) in self.pref_g:
            for (r, capacity) in  lst:
                yield "%s_%s" %(g, r)


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
    dic_gr = {'g1r1': 0.8, 'g1r2': 0.2, 'g2r1': 0.1, 'g2r2': 0.4}
    dic_n = {'n1': (0, 1.5), 'n2': (0, 0.8)}
    dic_cover = {'g1r1': {'n1':1, 'n2':2},
            'g1r2': {'n1':1},
            'g2r1': {'n1':1},
            'g2r2': {'n2':1}
            }
    solve_cdn(dic_n, dic_gr, dic_cover)


def init_node():
    """
    SELECT name, minBandwidthThreshold, maxBandwidthThreshold,unitPrice FROM cdn_center_resource_new.rs_node where chName like '%电信%节点';
    """
    dic_n = {}
    with open(os.sep.join((os.environ['HOME'], "bak/node_CT.csv"))) as f:
        f.readline()  # head
        for l in f:
            l = l.strip().split(',')
            node = 'cdn' + l[0]
            minbw = float(l[1]) / 1000
            maxbw = float(l[2]) / 1000
            dic_n[node] = ((minbw, maxbw))
    print 'len(dic_n):', len(dic_n)
    return dic_n


def init_gr():
    dic_gr = defaultdict(float)
    with open(os.sep.join((os.environ['HOME'], "bak/grn_CT.csv"))) as f:
        for l in f:
            l = l.strip().split(',')
            gr, bw = l[0], float(l[2])
            dic_gr[gr] += bw
    print 'len(dic_gr):', len(dic_gr)
    return dic_gr


def init_cover():
    """
    SELECT
    dispDomain, rs_region.enName, rs_node.name, rs_cover.cross_relative_level
FROM
    rs_dispgroup
        JOIN
    rs_dispgroup_node ON (rs_dispgroup_node.groupId = rs_dispgroup.id)
        JOIN
    rs_cover ON (rs_cover.node_id = rs_dispgroup_node.nodeId)
        JOIN
    rs_node ON (rs_node.id = rs_cover.node_id)
        JOIN
    rs_region ON (rs_cover.region_line_id = rs_region.id)
WHERE
    cross_relative_level IS NOT NULL
        AND rs_node.status = 1
        AND rs_dispgroup.status = 1
        AND dispDomain REGEXP 'k(2|3|5|6|125).gslb'
        AND rs_cover.cross_relative_level <= rs_dispgroup.crossLevel;
    """
    dic_cover = defaultdict(lambda: defaultdict(int))
    with open(os.sep.join((os.environ['HOME'], "bak/cover_CT.csv"))) as f:
        f.readline()
        for l in f:
            l = l.strip().split(',')
            if not l[1].endswith('_CT'):
                continue
            gr, node, level = '%s_%s' % (l[0].split('.', 1)[0], l[1]), "cdn" + l[2], int(l[3])
            dic_cover[gr][node] = level
    print 'len(dic_cover):', len(dic_cover)
    return dic_cover


def solve_cdn(dic_n, dic_gr, dic_cover):
    g = FlowNetwork()
    g_order = ['k2', 'k6', 'k135', 'k5', 'k3']
    for gr, bw in dic_gr.iteritems():
        g.add_edge('s', gr, bw)
    for node, (_, maxbw) in dic_n.iteritems():
        g.add_edge(node, 't', maxbw)
    # set capability by availability
    for gr in dic_cover:
        for node in dic_cover[gr]:
            if not g.get_edge("s", gr) or not g.get_edge(node, "t"):
                continue
            cap = min(
                g.get_edge("s", gr).capacity, g.get_edge(node, "t").capacity)
            if DEBUG:
                print "link %s -->%s, cap: %s" % (gr, node, cap)
            g.add_edge(gr, node, cap)

    g.init_prefer(g_order, dic_cover)
    res = g.max_flow('s', 't')
    print 'max_flow:', res


if __name__ == "__main__":
    #test()
    #sim_cdn()
    solve_cdn(init_node(), init_gr(), init_cover())
